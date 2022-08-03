from time import sleep
import time
import sys
import os
from Library import acton_sp2150_lib
from Library import andor_camera
from Library import phaser
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
from datetime import datetime as dt
import matplotlib.pyplot as plt
import keyboard

class Spectra():
	def __init__(self,setting_dict,dspl):
		self.cur_time = dt.now()
		self.app = QtGui.QApplication(sys.argv)
		self.camera = andor_camera.AndorCamera()
		self.laser = phaser.obis("405")
		self.laser.start()
		self.laser.set_cw_power()
		self.camera_cooldown()
		#self.camera.GetTemperature()
		#cur_T = float(self.camera._temperature)
		#print cur_T
		self.get_aqu_setting(setting_dict)
		self.camera_setting(setting_dict)
		self.acton = acton_sp2150_lib.Acton(com = 4, grating = 2)
		`1	`
		self.dspl = dspl
		if self.dspl:
			self.ploto1 = pg.plot()
			self.ploto1.showGrid(x=True, y=True, alpha=1.)
			self.PL_curve = self.ploto1.plot(pen = pg.mkPen('r', width=1.5))
			self.PL_avg_curve = self.ploto1.plot(pen = pg.mkPen('b', width=1.5))
			self.PL_recovery = self.ploto1.plot(pen = pg.mkPen('g', width=1.5))

	def get_aqu_setting(self,dict):
		self.wlen_start = float(dict["wlen_start"])
		self.slit = 20  #default value
		self.avg_num = int(dict["avg_num"]) #numbr of scan for each stokes and antistokes emission
		self.laser_power = int(dict["power"]) #laser power
		self.stime = int(dict["time_interval"])
		self.exp_time = dict["exposure_time"]

	def camera_cooldown(self):
		self.camera.SetCoolerMode(1)
		self.camera.CoolerON()
		self.camera.SetTemperature(-80)

		#while self.camera.GetTemperature() is not 'DRV_TEMP_STABILIZED':
		self.camera.GetTemperature()
		cur_T = float(self.camera._temperature)
		print "current camera temperature",cur_T
		while  cur_T > -70:
			self.camera.GetTemperature()
			sleep(0.1)
			cur_T = float(self.camera._temperature)
			print "current Temperature is ", cur_T
			print "current status ", self.camera.GetTemperature()
			sleep(10)
		print "Temperature is stable now"
	def camera_setting(self,dict):

		self.numb_accum = 1
		self.kinetic_series_length = 1
		self.numb_prescans = 0
		self.em_gain = dict["gain"]
		self.em_gain_recovery = dict["recovery_gain"]
		self.aqu_mode = 1
		self.triggering = 0
		self.readmode = 3    #single track
		self.VSSpeed = 1     # 0.3 0.5 0.9 1.7 3.3
		self.VSAmplitude = 0 #0(Normal), +1, +2, +3, +4

		self.adc_chan = 0 
		self.HSSspeed = 0
		self.preamp_gain = 1 # 1.0 2.4 4.9

		self.image_left = 1
		self.image_right = 512
		self.image_bot = 1
		self.image_top = 512
		self.bin_row = dict["row_center"]
		self.bin_height = dict["row_height"]
		self.horizontal_binning = 1

		self.camera.SetShutter(1, 1, 0, 0)
		self.camera.GetTemperature()

		self.camera.SetPreAmpGain(self.preamp_gain)
		self.camera.SetVSSpeed(self.VSSpeed)
		self.camera.SetADChannel(self.adc_chan)
		 
		self.camera.SetEMCCDGain(self.em_gain)
		self.camera.SetAcquisitionMode(self.aqu_mode) # 1 - single scan
		self.camera.SetNumberAccumulations(self.numb_accum)
		self.camera.SetReadMode(self.readmode) # 0 - FVB, 3 - single track
		
		self.camera.SetSingleTrack(self.bin_row, self.bin_height, self.horizontal_binning)
		self.camera.SetExposureTime(self.exp_time)
		self.camera.SetTriggerMode(self.triggering)
		
		self.camera.GetAcquisitionTimings()
		#self.camera.StartAcquisition()
		slptm = float(self.camera._kinetic)
		print "sleeptime = ", slptm
		sleep(slptm+0.5)

	def create_folder(self):
		#self.dir_name = "data\\"+str(self.cur_time.year)+str(self.cur_time.month)+str(self.cur_time.day)+"_"+str(self.cur_time.hour)+str(self.cur_time.minute)
		self.dir_name = "C:/Users/Kuno Lab/Desktop/Shubin/Python_Script/data/"+str(self.cur_time.year)+str(self.cur_time.month)+str(self.cur_time.day)
		if os.path.exists(self.dir_name): #check if folder already exists
			pass
		else:
			os.makedirs(self.dir_name)

		self.dir_name = "C:/Users/Kuno Lab/Desktop/Shubin/Python_Script/data/"+str(self.cur_time.year)+str(self.cur_time.month)+str(self.cur_time.day)+"/"+measure_name
		if os.path.exists(self.dir_name): #check if folder already exists
			pass
		else:
			os.makedirs(self.dir_name)

	def camera_acquisition(self):
		self.camera.StartAcquisition()
		self.camera.WaitForAcquisition()
		self.current_data = self.camera.GetAcquiredData([])
		self.current_data = np.asarray(self.current_data)


# INTERESTING STUFF STARTS HERE


	def start_measuring(self, save = True):
		delta = np.abs(self.acton.k_calibr*512)
		#wlen_sp_start = int(self.wlen_start+0.5*self.acton.k_calibr_3*(1-512))-1
		w_cw = self.wlen_start+int(delta)/2
		grating = self.acton.get_grating()
		if grating != 2:
			print "Change to grating 2"
			self.acton.change_grating("2")
		self.acton.set_wavelength(w_cw, cw=True)
		cur_wlen = (np.arange(1,513,1)*self.acton.k_calibr+self.acton.b_calibr+self.acton.get_wavelength())
		self.camera.SetShutter(1,1,0,0)
		###get dark level
		print "measuring backgroud"
		self.laser.set_power(0)
		self.camera_acquisition()
		bckgnd = self.current_data
		sleep(1)

		PL_avg_data = np.zeros(len(bckgnd))
		original_curve = np.zeros(len(bckgnd))
		
		self.laser.set_power(self.laser_power)

		num_m=0
		while True:
			if num_m != 0:
				sleep(self.stime)
			
			for cur_scan_n in xrange(self.avg_num):
				self.camera_acquisition()
				cur_data = self.current_data - bckgnd
				PL_avg_data = (PL_avg_data*cur_scan_n + cur_data)/(cur_scan_n+1)

				if dspl:
					self.PL_avg_curve.setData(cur_wlen, PL_avg_data/max(PL_avg_data))
					self.PL_curve.setData(cur_wlen, original_curve/max(original_curve))
					QtCore.QCoreApplication.processEvents()
			if num_m == 0:
				num_m=1
				original_curve = PL_avg_data
				
			if keyboard.is_pressed("q"):
				break
		
		self.laser.set_power(0)
		
		self.camera.SetShutter(1,2,0,0)
		self.acton.close()
		self.laser.close()
			
if __name__ == "__main__":

	setting_dict = {"wlen_start":590, "avg_num":1, "power":20,"time_interval":0,"exposure_time":1, "gain":0, "recovery_gain":0, "row_center":250, "row_height":305}



	dspl = True
	save = True
	recovery = True
	st = time.time()
	PL = Spectra(setting_dict,dspl)
	PL.start_measuring(save)
	print time.time()-st