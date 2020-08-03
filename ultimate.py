import os
import sys
import thread
import time
import datetime
import pickle

import hop
import malt

import Temp
import Relay
import Timer
import Sound
import telepot
from telepot.loop import MessageLoop
import telegram
import push

class Recipe:

    TITLE="Brew" 

    HOPBITTER="Inserire Luppolo da amaro"
    HOPTASTE="Inserire Luppolo da aroma"
    HOPFLAV="Inserire Luppolo da profumo"
    INSERTGRAIN="Inserire grani"
    REMOVEGRAIN="Rimuovere grani"
    ##COOLINGINSERT="Inserire serpentina"
    BOILEND="Fine bollitura"
    COOLING="Iniziare raffreddamento"
    BREWERROR="Errore procedimento, uscita!"

    filepath=0
    status="start"
    recipe=0

    ##variable for notifications
    ##pushbutton
    push=0
    ##mqtt
    mqtt=0
    ##telegram
    telegr=0

    ##other classes
    temp_mash=0
    heat_mash=0
    temp_boil=0
    heat_boil=0

    def __init__(self, filepath):
        if len(sys.argv)==2:
            self.filepath=sys.argv[1]
        else:
            self.filepath=filepath

    def parseRecipe(self):
        print "Opening file: "+self.filepath
        file=open(self.filepath, 'r')

        for l in file:
            ##excluding comments
            if "#" not in l:
                sub=l.split(":")
                if sub[0]=="system_final_volume":
                    self.sys_vol=float(sub[1])
                elif sub[0]=="system_efficiency":
                    self.sys_eff=float(sub[1])
                elif sub[0]=="malt_dry_extract":
                    self.malt_dry=malt.Malt(float(sub[1]), 350, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_pale_ale":
                    self.malt_pale=malt.Malt(float(sub[1]), 310, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_crystal":
                    self.malt_crystal=malt.Malt(float(sub[1]), 280, self.sys_eff, self.sys_vol)
                elif sub[0]=="malt_black":
                    self.malt_black=malt.Malt(float(sub[1]), 250, self.sys_eff, self.sys_vol)
                elif sub[0]=="hop_bitter":
                    self.hop_bitter=hop.Hop(float(sub[3]), float(sub[2]), float(sub[1]), self.sys_vol, float(sub[4]))
                elif sub[0]=="hop_taste":
                    self.hop_taste=hop.Hop(float(sub[3]), float(sub[2]), float(sub[1]), self.sys_vol, float(sub[4]))
                elif sub[0]=="hop_flavour":
                    self.hop_flav=hop.Hop(float(sub[3]), float(sub[2]), float(sub[1]), self.sys_vol, float(sub[4]))
                elif sub[0]=="yeast_att":
                    self.yatt=float(sub[1])
                elif sub[0]=="mash":
                    self.mash_time=float(sub[1])
                    self.mash_temp=float(sub[2])
                elif sub[0]=="boil":
                    self.boil_time=float(sub[1])
                    self.boil_temp=float(sub[2])


    def start_brew(self):
		##initialize sound for acoustic warnings
        self.sound=Sound.Sound()
		##initialize temperature probe
        self.temperature=Temp.Temp()
		##initialize relay for heat
        self.heat=Relay.Relay(21)

	self.notification=push.Push()

		##TODO - plotting -
        thread.start_new_thread(self.plot_data, ())
	
	self.status="heating to mash"
	self.notification.sendString(self.TITLE,self.status)
		##TODO - telegram -
	thread.start_new_thread(self.telegramchat, ())
		##increase to mash temperature
#        elapsed_time_tmash=self.temperature.increase_to(self.mash_temp, self.heat)
        	##acoustic warning -insertgrain-
	self.notification.sendString(self.TITLE,self.INSERTGRAIN)
	self.status="mash"
		##keep tmash constant for mash_time taken from recipe
#        self.temperature.keep_constant(self.mash_temp, self.mash_time, self.heat)
		##acoustic warning -removegrain-
        ##self.sound.play(self.REMOVEGRAIN)
	self.notification.sendString(self.TITLE,self.REMOVEGRAIN)
	self.status="heating to boil"
		##increase temperature for boiling
        elapsed_time_tboil=self.temperature.increase_to(self.boil_temp, self.heat)
        	##start timers
		##end of boiling - timer -
        timer_end=Timer.Timer(self.boil_time*60, self.notification, self.BOILEND)
        	##insert cooling element -timer-
        timer_coolinginsert=Timer.Timer((self.boil_time-15)*60, self.notification, self.COOLINGINSERT)
        timer_end.start()
        timer_coolinginsert.start()
        if self.hop_bitter:
		##timer for inserting hops for bittering
            timer_hop_bitter=Timer.Timer((self.boil_time-self.hop_bitter.boil_time)*60, self.notification, self.HOPBITTER)
            timer_hop_bitter.start()
        if self.hop_taste:
            if (self.hop_taste.boil_time>0):
			##timer for inserting hops for taste
                timer_hop_taste=Timer.Timer((self.boil_time-self.hop_taste.boil_time)*60, self.notification, self.HOPTASTE)
                timer_hop_taste.start()
        if self.hop_flav:
            if (self.hop_flav.boil_time>0):
			##timer for inserting hops for flavour
                timer_hop_flav=Timer.Timer((self.boil_time-self.hop_flav.boil_time)*60, self.notification, self.HOPFLAV)
                timer_hop_flav.start()

        	##boil -> keep resistance always on for boil time
		##start boiling for boil time -heat always on-
	self.status="boil"
	self.notification.sendString(self.TITLE,self.status)
        self.temperature.boil(self.boil_time, self.heat)
		
		##boil end
		##switch off heat
	self.status="end"
        self.heat.off()
	self.notification.sendString(self.TITLE,self.BOILEND)
        print "BREW END"
	self.plot=1
	self.chat=1

	self.save_data()
	print "data saved!"
	print ""

	##TODO save data
    def save_data(self):
	curdir=os.getcwd()
  	logdir=os.path.join(curdir, "log")
	now=datetime.datetime.now()
	filename_prefix="%d-%d-%d_%d.%d_" % (now.year,now.month,now.day,now.hour,now.minute)
	temperature_file=filename_prefix+"temperature.pickle"
	time_file=filename_prefix+"time.pickle"
	heat_file=filename_prefix+"heat.pickle"
	temp_path=os.path.join(logdir, temperature_file)
	time_path=os.path.join(logdir, time_file)
	heat_path=os.path.join(logdir, heat_file)
	with open(temp_path,'wb') as handle:
		pickle.dump(self.probe_T.history_temp, handle, protocol=pickle.HIGHEST_PROTOCOL)
	with open(time_path,'wb') as handle:
		pickle.dump(self.probe_T.history_time, handle, protocol=pickle.HIGHEST_PROTOCOL)
	with open(heat_path,'wb') as handle:
		pickle.dump(self.probe_T.history_heat, handle, protocol=pickle.HIGHEST_PROTOCOL)


	##TODO plot data
    def plot_data(self):
   	  while self.plot==0:
   	      ##terminal
   	      line="Heat: " +str(self.heat.get_status())+" Temp: "+str(self.temperature.get_temp())
	      print line
   	      time.sleep(1)

    def telegramchat(self):
	  t=telegram.Telegram() 	
	  MessageLoop(t.bot, t.handle).run_as_thread()
	  print("Listening telegram chat...")
          while self.chat==0:
		t.update_variables(self.status, self.temperature.get_temp(), 0)
		time.sleep(10)

      	
 
    def load(self,filename):
          with open(filename,'rb') as handle:
	      obj=pickle.load(handle)
	      return obj

   
	##TODO manage display?
        ##display


if __name__=="__main__":
    rec=Recipe("recipe.txt")
    rec.parseRecipe()

    print "OG: \t"+str(rec.og)
    print "FG: \t"+str(rec.fg)
    print "ABV: \t"+str(rec.abv)+" %"
    print "IBU: \t"+str(int(round(rec.ibu)))
    print "Style: \t"+str(rec.style)

    choice=raw_input('Proceed with brewing? [y/N]: ')

    if choice in ["y", "Y"]:
        print "Starting brewing..."
        try:
            rec.start_brew()
        except:
            ##catched errors
	    rec.notification.sendString(rec.TITLE,rec.BOILEND)
            print "Abnormal error, save data before exiting..."
            rec.save_data()
        print "**END**"
    elif choice in ["N", "n", ""]:
        print "Exit..."
    else:
        print "Incorrect Value..."
        print "Exit..."
