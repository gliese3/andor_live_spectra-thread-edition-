import sys
from PyQt5 import QtCore, QtWidgets, QtGui, QtTest

import numpy as np
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib_additional import MplCanvas

from scipy.signal import savgol_filter

import andor_camera

from interface import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    stop_signal = QtCore.pyqtSignal(bool)
    def __init__(self, *args, **kwargs):        

        # from compiled file
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("Andor real time spectrum")
        
        # set icon
        self.setWindowIcon(QtGui.QIcon("images/live-streaming.png"))
        
#================================ CONNECTIONS =================================

        self.live_but.clicked.connect(self.onLive)
        self.save_data_action.triggered.connect(self.onSaveData)

#================================ /CONNECTIONS ================================

        # TIMERS
        self.camera_temp_timer = QtCore.QTimer()
        self.camera_temp_timer.timeout.connect(self.updateCameraTemp)
        
        self.cool_timer = QtCore.QTimer()
        self.cool_timer.timeout.connect(self.checkCameraTemp) # initial cooling
        
        self.elapsed_timer = QtCore.QElapsedTimer()

        # VARIABLES
        self.annotations = []
         
        # INIT PROCEDURE 
        try:
            self.camera = andor_camera.AndorCamera()
        except Exception as e:
            print(e)
            QtWidgets.QMessageBox.critical(self, "Camera", "Camera connection problem.")
            return
        else:

            # cool camera to -80C
            self.cameraCoolDown()
            
            # adjust camera
            try:
                self.setCameraSettings()
            except Exception as e:
                print(e)
                QtWidgets.QMessageBox.critical(self, "Camera", "Error applying settings.")
                return
            
            # start camera temp timer
            self.camera_temp_timer.start(500)
        
        # open window in maximized size
        self.showMaximized()
        
        # arrange plot widget elements on GUI
        # plot init
        self.canvas = MplCanvas(self) # canvas to plot
        toolbar = NavigationToolbar(self.canvas, self) # navigation toolbar
        
        # arrange matplotlib elements in gui
        self.plot_layout.addWidget(toolbar)
        self.plot_layout.addWidget(self.canvas)
        
#=================================== SLOTS ====================================
    
    def onLive(self):
        but_text = self.live_but.text()
        if but_text == "Live":
            self.live_but.setText("Stop")
            self.camera.SetExposureTime(self.exposure_time_spBox.value())
            self.camera.SetShutter(1, 1, 0, 0) # open
            
            # reset plot
            self.canvas.fig.clear()
            self.canvas.axs = self.canvas.fig.add_subplot(1, 1, 1)
            self.canvas.axs.set_title("Real time Andor spectrum")
            self.canvas.axs.set_xlabel("Wavelength, nm", fontweight="bold")
            self.canvas.axs.set_ylabel("Intensity, a.u.", fontweight="bold")
            self.canvas.axs.grid()
            self.canvas.axs.set_ylim(0, 1.1)
            self.canvas.fig.set_tight_layout(True)
            
            self.x_data = np.linspace(self.start_wavelen_spBox.value(),
                                 self.end_wavelen_spBox.value(),
                                 512) # matrix h-resolution
            
            self.y_data = self.getImageNoThread()
            
            # smooth the data if needed
            if self.smooth_data_chBox.isChecked():
                self.y_data  = savgol_filter(self.y_data , 20, 2)
                
            # normalize data
            max_imag_val = max(self.y_data)
            self.y_data = np.flip(self.y_data) / max_imag_val # flip because of the camera
            
            # prepare main plot
            self.canvas.axs.plot(self.x_data, self.y_data, alpha=0.5, label="Initial static")
            self.update_plot, = self.canvas.axs.plot(self.x_data, self.y_data, alpha=0.5, label="Last dynamic")
            self.canvas.axs.legend()
            
            # prepare peaks plot
            max_val = max(self.y_data)
            max_idx = np.where(self.y_data == max_val)[0][0] # find max index
            peak_coord= np.transpose([self.x_data[max_idx], self.y_data[max_idx]])
            self.canvas.axs.plot(self.x_data[max_idx], self.y_data[max_idx], "bo") # static first plot
            self.canvas.axs.annotate(text=f"λ = {round(peak_coord[0], 1)} nm",
                                    xy=peak_coord, 
                                    xycoords='data',
                                    xytext=(-80, 20),
                                    textcoords='offset points',
                                    size=10,
                                    va="center",
                                    bbox=dict(boxstyle="round4",
                                            fc="tab:blue",
                                            alpha=0.3),
                                    arrowprops=dict(arrowstyle="->",
                                                    connectionstyle="angle3,angleA=0,angleB=-90"),
                                    zorder=100)
            
            # updating plot
            self.peaks_plot, = self.canvas.axs.plot(self.x_data[max_idx], self.y_data[max_idx], "ro")
            
            # draw everything
            self.canvas.draw()
            
            self.getCameraImage()
            
            # start elapsed timer
            self.elapsed_timer.start()
            
            # stop timer. Now thread is showing temp.
            self.camera_temp_timer.stop()
            
            self.exposure_time_spBox.valueChanged.connect(self.worker.changeCameraExposure)
            
        elif but_text == "Stop":
            
            self.stop_signal.emit(True)
            self.live_but.setText("Live")
        
        
    def updatePlot(self, y_data):
        self.y_data = y_data["data"]
        
        # smooth the data if needed
        if self.smooth_data_chBox.isChecked():
            self.y_data  = savgol_filter(self.y_data , 20, 2)
        
        # normalize data
        max_imag_val = max(self.y_data)
        self.y_data = np.flip(self.y_data) / max_imag_val # flip because of the camera
        
        # main plot
        self.update_plot.set_data(self.x_data, self.y_data) # normalize array
        
        if self.show_peaks_chBox.isChecked():
            # peaks plot
            self.peaks_plot.set_visible(True)
            max_val = max(self.y_data)
            max_idx = np.where(self.y_data == max_val) # find max index
            self.peaks_plot.set_data(self.x_data[max_idx], self.y_data[max_idx])

            # annotations plot
            peaks_array = np.transpose([self.x_data[max_idx], self.y_data[max_idx]])
            
            # clear old annotations for proper new plot
            if self.annotations:
                for ann in self.annotations:
                    ann.remove()
                self.annotations = []
            
            for peak_coord in peaks_array:
                ann = self.canvas.axs.annotate(text=f"λ = {round(peak_coord[0], 1)} nm",
                                    xy=peak_coord, 
                                    xycoords='data',
                                    xytext=(20, 20),
                                    textcoords='offset points',
                                    size=10,
                                    va="center",
                                    bbox=dict(boxstyle="round4",
                                            fc="tab:red",
                                            alpha=0.3),
                                    arrowprops=dict(arrowstyle="->",
                                                    connectionstyle="angle3,angleA=0,angleB=-90"),
                                    zorder=100)
                self.annotations.append(ann)
        else:
            # clear old annotations for proper new plot
            if self.annotations:
                for ann in self.annotations:
                    ann.remove()
                self.annotations = []
                self.peaks_plot.set_visible(False)
                
        # update elapsed lab value
        elap_time = round(self.elapsed_timer.elapsed() / 1000 / 60, 1) # in min
        self.elapsed_timer_lab.setText(f"Live time duration: {elap_time} min")    
        self.canvas.draw()
        
        
    def updateCameraTemp(self):
        self.camera.GetTemperature()
        current_temp = float(self.camera._temperature)
        self.cam_temp_value.setText(f"{current_temp}")


    def onSaveData(self):
        save_file_name = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            caption="Save data to file",
            filter="*.csv")[0]

        if not save_file_name: # no file name
            return
        
        np.savetxt(save_file_name, np.transpose([self.x_data, self.y_data]), fmt="%1.3f", delimiter="\t")
        
        
    def setCameraExposure(self):
        self.camera.SetExposureTime(self.exposure_time_spBox.value())
        print("Set new value.")
        
    def threadStop(self):
        self.camera.SetShutter(1, 2, 0, 0) # close
        self.cam_max_value_lab.setText("-")

#=================================== /SLOTS ====================================

#================================= FUNCTIONS ===================================

    def cameraCoolDown(self):
        self.camera.SetCoolerMode(1)
        self.camera.CoolerON()
        self.camera.SetTemperature(-80)
        
        self.camera.GetTemperature()
        current_temp = float(self.camera._temperature)
        
        if current_temp > -70:
            self.cool_timer.start(1000)
        else:
            self.statusbar.showMessage(f"Temperature is stable. Ready to start!", 3000)
            self.live_but.setEnabled(True)
        
    
    def checkCameraTemp(self):
        self.camera.GetTemperature()
        QtTest.QTest.qWait(100)
        current_temp = float(self.camera._temperature)
        if current_temp > -70:
            self.statusbar.showMessage(f"Current temperature: {current_temp} °C. Wait for cooling.", 1000)
        else:
            self.statusbar.showMessage(f"Temperature is stable. Ready to start!", 3000)
            self.live_but.setEnabled(True)
            self.cool_timer.stop()
            
        
    def setCameraSettings(self):
        self.camera.GetTemperature()
        self.camera.SetPreAmpGain(1)
        self.camera.SetVSSpeed(1)
        self.camera.SetADChannel(0)
        self.camera.SetEMCCDGain(0)
        self.camera.SetAcquisitionMode(1) # single scan
        self.camera.SetNumberAccumulations(1)
        self.camera.SetReadMode(3) # single track
        self.camera.SetSingleTrack(284, 309, 1) # metrix ROI to capture
        self.camera.SetTriggerMode(0)
        self.camera.GetAcquisitionTimings()
        
        #? some pause
        slptm = int(self.camera._kinetic * 1000)
        QtTest.QTest.qWait(slptm  + 500)
    
    
    def getImageNoThread(self):
        self.camera.StartAcquisition()
        self.camera.WaitForAcquisition()
        image_data = np.asarray(self.camera.GetAcquiredData([]))
        max_imag_val = max(image_data)
        
        self.cam_max_value_lab.setText(str(max_imag_val)) # update current value
        
        return image_data
    
    
    def getCameraImage(self):
        self.worker = getCameraData_thread(self.camera,  self.cam_temp_value, self.cam_max_value_lab)
        self.worker.start()
        self.worker.finished.connect(self.threadStop)
        self.worker.transmit_data_signal.connect(self.updatePlot)
        self.stop_signal.connect(self.worker.stopLoop)
        
#================================= /FUNCTIONS ==================================


class getCameraData_thread(QtCore.QThread):
    transmit_data_signal = QtCore.pyqtSignal(dict)
    def __init__(self, camera,  cam_temp_value, cam_max_value_lab):
        super(QtCore.QThread, self).__init__()
        self.camera = camera
        self.stop = False
        self.cam_temp_value = cam_temp_value
        self.cam_max_value_lab = cam_max_value_lab
        self.old_exp = self.new_exp = 1 # init
        
    def run(self):
        while True:
            if self.old_exp != self.new_exp:
                self.camera.SetExposureTime(self.new_exp)
                self.old_exp = self.new_exp
            self.camera.StartAcquisition()
            self.camera.WaitForAcquisition()
            image_data = np.asarray(self.camera.GetAcquiredData([]))
            max_imag_val = max(image_data)
            self.cam_max_value_lab.setText(str(max_imag_val)) # update current value
            
            self.camera.GetTemperature()
            current_temp = float(self.camera._temperature)
            self.cam_temp_value.setText(f"{current_temp}")
            
            self.transmit_data_signal.emit({"data" : image_data})
            
            if self.stop:
                break
            
            
    def stopLoop(self, isTrue):
        self.stop = isTrue
        
        
    def changeCameraExposure(self, value):
        self.new_exp = value

        
app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()