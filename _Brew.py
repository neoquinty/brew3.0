import sys
import time
import datetime
import thread
import Temp
import Relay
import Sound
import pickle
##import Display

## connections

## 3.3v   --> num:  1 (primo in verticale, colonna sx)  --> GPIO??
## ground --> num: 39 (ultimo in verticale, colonna sx) --> GPIO20

## Temperature probe PIN  --> num  7 (quarto in verticale, colonna sx) --> GPIO04
## Resistance Relay PIN   --> mun 40 (ultimo in verticale, colonna dx) --> GPIO21

class Brew:

	## data from recipe

	def __init__(self,filepath,t=1,h=1,w=1):
		self.filepath=filepath
		## initialize T probe
		if t:
			self.probe_T=Temp.Temp()
		## initialize heat
		if h:
			self.heat=Relay.Relay(21)	
		## initialize sound
		if w:
			self.warning=Sound.Sound()
		##for now no Display
		## self.screen=Display.Display()
	
	def get_phase(self):
		return self.phase
	
	def show(self):
		while self.end==0:
			percentage=int(round(self.probe_T.tot_time*100/self.tottime))
			line="Heat: " +str(self.heat.get_status())+" Temp: "+str(self.probe_T.get_temp())+" / "+str(self.probe_T.target)+" Progress: %3d [%2d/%2d]" % (percentage,int(round(self.probe_T.tot_time)),int(round(self.tottime)))
			EL = '\x1b[K'  # clear to end of line
			CR = '\r'  # carriage return
			sys.stdout.write(line+EL+CR)
			sys.stdout.flush()
			## print line+"\r"
			## self.screen.fill(line_one,line_two,line_three,line_four,line_five)
			time.sleep(1)

		print "\n"
		print "have a nice day\n"
		##self.screen.clear()
		##self.screen.fill(" "," ","** END **"," "," ")
	
	def read_recipe(self):
		try:
			f=open(self.filepath,'r')
			for line in f:
				if   "mash_temp:" in line:
					self.mash_temp=line[-3:-1]
				elif "mash_time:" in line:
					self.mash_time=line[-3:-1]
				elif "boil_temp:" in line:
					self.boil_temp=line[-3:-1]
				elif "boil_time:" in line:
					self.boil_time=line[-3:-1]
				elif "hop_bitter_time:" in line:
					self.hop_bitter_time=line[-3:-1]
				elif "hop_taste_time:" in line:
					self.hop_taste_time=line[-3:-1]
				elif "hop_flav_time:" in line:
					self.hop_flav_time=line[-3:-1]
		
			self.tottime=int(self.mash_time)+int(self.boil_time)+14+30		##14 valore fisso x portare T a 70 + 30 tempo per portarla a 100
		except (FileNotFoundError, IOError): 
			print "File '%s' not found!!" % (self.filepath)			
			print "Exiting.."
			print "\n"
			exit()

	def save(self):
		now=datetime.datetime.now()
		filename_prefix="%d-%d-%d_%d.%d_" % (now.year,now.month,now.day,now.hour,now.minute)
		temperature_file=filename_prefix+"temperature.pickle"
		time_file=filename_prefix+"time.pickle"
		heat_file=filename_prefix+"heat.pickle"
		with open(temperature_file,'wb') as handle:
			pickle.dump(self.probe_T.history_temp, handle, protocol=pickle.HIGHEST_PROTOCOL)
		with open(time_file,'wb') as handle:
			pickle.dump(self.probe_T.history_time, handle, protocol=pickle.HIGHEST_PROTOCOL)
		with open(heat_file,'wb') as handle:
			pickle.dump(self.probe_T.history_heat, handle, protocol=pickle.HIGHEST_PROTOCOL)

	def load(self,filename):
		with open(filename,'rb') as handle:
			obj=pickle.load(handle)
			return obj

	
if __name__ == "__main__":
	app=Brew("recipe.txt",1,1,1)
	app.read_recipe()

	print "BOIL TIME  "+str(app.boil_time)+" min"
	print "BOIL TEMP  "+str(app.boil_temp)+" C"
	print "MASH TIME  "+str(app.mash_time)+" min"
	print "MASH TEMP  "+str(app.mash_temp)+" C"
	print "HOP BITTER "+str(app.hop_bitter_time)+" min"
	print "HOP TASTE  "+str(app.hop_taste_time)+" min"
	print "HOP FLAV   "+str(int(app.hop_flav_time))+" min"
	
	thread.start_new_thread( app.show, ())

	time.sleep(60)
	
	app.save()
	
	app.end=1	
	app.heat.off()
	app.heat.reset()
