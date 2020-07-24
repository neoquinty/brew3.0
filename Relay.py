import RPi.GPIO as GPIO
import time 

class Relay:

	pin=1000
	status=0

	def __init__(self,pin):
		self.pin=pin
		GPIO.setmode(GPIO.BCM)	
		GPIO.setup(self.pin,GPIO.OUT) 

	def on(self):
		GPIO.output(self.pin, GPIO.HIGH)
		self.status=1

	def off(self):
		GPIO.output(self.pin, GPIO.LOW)	
		self.status=0
	
	def get_status(self):
		return self.status
		
	def reset(self):
		GPIO.cleanup()


if __name__=='__main__':
	try:
		while 1:
			pin_number=raw_input( 'Digit PIN number:')
			device=Relay(int(pin_number))
			print "Testing Relay"
			print "Relay  ON for 10sec"
			device.on()
			time.sleep(10)
			print "Relay OFF for 10sec"
			device.off()
			time.sleep(10)
			print "cleanup Relay"
			device.reset()
			time.sleep(1)
			 
	except KeyboardInterrupt:
		print "Ctrl-C catched!!"
		print Exit
		device.reset()	
	
