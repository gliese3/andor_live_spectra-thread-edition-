import serial
import atexit, string
from time import sleep
import time
class Acton():
	"""
	acton sp-2150
	1 - Mirror
	2 - 1200 gr/mm 500 nm blaze
	3 - 150 gr/mm 800 nm blaze
	"""
	def __init__(self,com=7, grating=1):
		self.zero_position = 254 #2021OCT20  255 position of the line when the monochromator is set to 0
		self.k_calibr = -0.640257 #2021OCT20 -0.637 #Jun/6/2019  #-0.0319#May/27/2019 -0.037302 #-0.0368919 #Slope of the calibration line with Hg-Ar lamp
		self.b_calibr =  546.06 - 384.62 #2021OCT20 546.1 - 384.13  # June/6/2019                  #785-773.53  #May/27/2019     496.5 - 486.849012 #514.5 - 505.1081127  #Andor iXon 33.605
		#Offset of the calibration line with Hg-Ar lamp
		self.delta_wlen = 2. # nm
		self.last_wlen=-1
		self.port_is_open = False
		self.grating = grating
		
		
			
		#self.power = power
		self.baud_rate = 9600
		self.port = '\\\\.\\COM'+str(com)
		self.ser = serial.Serial()
		self.ser.baudrate = self.baud_rate
		self.ser.port = self.port
		self.ser.timeout = 5.
		if self.ser.isOpen():
			self.ser.close()
			sleep(0.3)
		else:
			try:
				print("trying to open port ", com)
				self.ser.open()
			except serial.SerialException:
				print("port is already open...")	
		if self.ser.isOpen():
			self.port_is_open = True
		#self.ser.flushInput()
		
		self.ser.write("?GRATINGS \r")
		print (self.waitreply())
		
		print ("Current wavelength = ", self.get_wavelength())
		print ("Current grating = ", self.get_grating())
		
		#self.change_grating(self.grating)c
		#if verbose: print responce
		"""
		self.ser.write("MODEL\r")
		print (self.ser.read(20))
		
		print (self.ser.read(10))
		
		self.ser.write("?GRATING \r")
		print (self.ser.read(1000))
		
		self.ser.write("?GRATINGS \r")
		#print (self.ser.readlines(100,eol='\r'))
		print (self.ser.read(1000))
		
		self.ser.write("2 GRATING \r")
		print (self.ser.read(1000))
		
		print (self.get_wavelength())
		"""
		atexit.register(self.close)

				
	def get_wavelength(self):
		self.ser.write("?NM\r")
		reply = self.waitreply()
		self.last_wlen = float(str(reply.split()[1]))
		return self.last_wlen
	
	def change_grating(self,grating):
		self.ser.write(str(int(grating))+" GRATING"+"\r") 
		reply = self.waitreply()
		print ("change to grating",int(reply.strip().split()[0]))
				
	def get_grating(self):
		self.ser.write('?GRATING \r')
		reply = self.waitreply()
		self.grating = int(reply.strip().split()[1])
		return self.grating
	
	def get_slit(self):
		print ("Slit is not motorized in Acton spectrometer!")
		return True
	def set_slit(self, slit):
		print ("Slit is not motorized in Acton spectrometer!")
		return True
		  
	def waitreply(self, timeout=20):
		responce = ""
		time1 = time.time()
		elapsedtime = 0
		while not("ok" in responce):
			responce = responce+self.ser.read()
			sleep(0.005)
			elapsedtime = time.time()-time1
			if elapsedtime>timeout:
				print ("Timeout error!")
				return False
			
		return responce
	def set_wavelength(self, wlen, cw=False):
		#cw means spectrometer will be set to specific wavelength in the middle of CCD chip, (row number 256)
		#it will use calibration constants self.k_calibr and self.b_calibr to move to specific wavelength
		#if cw is False spectrometer will be set to the wavlengths wlen
		
		#check if we need to moove spectrometer
		print ("self.last_wlen, wlen")
		print (self.last_wlen, wlen)
		if abs(self.last_wlen-wlen)<self.delta_wlen:
			return self.last_wlen
		if cw: 
			wlen = int(wlen - self.zero_position*self.k_calibr - self.b_calibr)
			
		self.ser.write('%1.2f GOTO\r'%wlen)
		reply = self.waitreply()
		#if reply:
		self.cur_wlen = self.get_wavelength()
		return self.last_wlen
		#else:
		#	return False
	
	def close(self):
		if self.port_is_open:
			self.ser.close()
		else:
			print ("Device connected to port ", str(self.ser.port), " is already closed...")

if __name__ == "__main__":
	acton = Acton()
	acton.get_grating()
	acton.get_wavelength()
	acton.change_grating(2)
	acton.set_wavelength(500)
	acton.get_grating()
	acton.get_wavelength()
