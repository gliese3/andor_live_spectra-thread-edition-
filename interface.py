# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(969, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(216, 255, 196);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_9 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.line = QtWidgets.QFrame(self.frame)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.cam_max_value_lab = QtWidgets.QLabel(self.frame)
        self.cam_max_value_lab.setObjectName("cam_max_value_lab")
        self.horizontalLayout_6.addWidget(self.cam_max_value_lab)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.cam_temp_value = QtWidgets.QLabel(self.frame)
        self.cam_temp_value.setObjectName("cam_temp_value")
        self.horizontalLayout_7.addWidget(self.cam_temp_value)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addWidget(self.frame)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.start_wavelen_spBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.start_wavelen_spBox.setMinimumSize(QtCore.QSize(100, 0))
        self.start_wavelen_spBox.setMaximum(1000.0)
        self.start_wavelen_spBox.setProperty("value", 384.41)
        self.start_wavelen_spBox.setObjectName("start_wavelen_spBox")
        self.horizontalLayout_2.addWidget(self.start_wavelen_spBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.end_wavelen_spBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.end_wavelen_spBox.setMinimumSize(QtCore.QSize(100, 0))
        self.end_wavelen_spBox.setMaximum(1000.0)
        self.end_wavelen_spBox.setProperty("value", 709.96)
        self.end_wavelen_spBox.setObjectName("end_wavelen_spBox")
        self.horizontalLayout_3.addWidget(self.end_wavelen_spBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.exposure_time_spBox = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.exposure_time_spBox.setMinimumSize(QtCore.QSize(100, 0))
        self.exposure_time_spBox.setDecimals(1)
        self.exposure_time_spBox.setMinimum(0.1)
        self.exposure_time_spBox.setSingleStep(0.1)
        self.exposure_time_spBox.setProperty("value", 0.3)
        self.exposure_time_spBox.setObjectName("exposure_time_spBox")
        self.horizontalLayout_4.addWidget(self.exposure_time_spBox)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.show_peaks_chBox = QtWidgets.QCheckBox(self.groupBox)
        self.show_peaks_chBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.show_peaks_chBox.setText("")
        self.show_peaks_chBox.setChecked(True)
        self.show_peaks_chBox.setObjectName("show_peaks_chBox")
        self.horizontalLayout_8.addWidget(self.show_peaks_chBox)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.smooth_data_chBox = QtWidgets.QCheckBox(self.groupBox)
        self.smooth_data_chBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.smooth_data_chBox.setText("")
        self.smooth_data_chBox.setChecked(True)
        self.smooth_data_chBox.setObjectName("smooth_data_chBox")
        self.horizontalLayout_9.addWidget(self.smooth_data_chBox)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.verticalLayout_3.addWidget(self.groupBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setEnabled(False)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_3.addWidget(self.label_8)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.live_but = QtWidgets.QPushButton(self.centralwidget)
        self.live_but.setEnabled(False)
        self.live_but.setObjectName("live_but")
        self.horizontalLayout.addWidget(self.live_but)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.elapsed_timer_lab = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.elapsed_timer_lab.setFont(font)
        self.elapsed_timer_lab.setStyleSheet("color: rgb(255, 0, 0);")
        self.elapsed_timer_lab.setText("")
        self.elapsed_timer_lab.setObjectName("elapsed_timer_lab")
        self.horizontalLayout.addWidget(self.elapsed_timer_lab)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_10.addLayout(self.verticalLayout_3)
        self.plot_layout = QtWidgets.QVBoxLayout()
        self.plot_layout.setObjectName("plot_layout")
        self.horizontalLayout_10.addLayout(self.plot_layout)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.save_data_action = QtWidgets.QAction(MainWindow)
        self.save_data_action.setObjectName("save_data_action")
        self.menuFile.addAction(self.save_data_action)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_9.setText(_translate("MainWindow", "CURRENT VALUES"))
        self.label_5.setText(_translate("MainWindow", "Camera max value:"))
        self.cam_max_value_lab.setText(_translate("MainWindow", "-"))
        self.label_6.setText(_translate("MainWindow", "Camera temperature, °C:"))
        self.cam_temp_value.setText(_translate("MainWindow", "-"))
        self.groupBox.setTitle(_translate("MainWindow", "Control"))
        self.label.setText(_translate("MainWindow", "Start wavenegth, nm"))
        self.label_2.setText(_translate("MainWindow", "End wavelength, nm"))
        self.label_3.setText(_translate("MainWindow", "Exposure time, s"))
        self.label_7.setText(_translate("MainWindow", "Show peaks"))
        self.label_10.setText(_translate("MainWindow", "Smooth data"))
        self.label_8.setText(_translate("MainWindow", "ATTENTION! Before run, check for proper\n"
"monochromator position and grating selection."))
        self.live_but.setText(_translate("MainWindow", "Live"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.save_data_action.setText(_translate("MainWindow", "Save data"))