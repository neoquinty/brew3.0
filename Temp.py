import glob
import math
import time
import Relay
import os

class Temp:
    TIMECYCLE=7.5
    t=0  # type: int
    device_file=0
    start_time=0
    tot_time=0
    history_temp=[]
    history_time=[]
    history_heat=[]
		
    def __init__(self):
        print "Temp  __init__: temp initializing"
        try:
            os.system('modprobe w1-gpio')
            os.system('modprobe w1-therm')
            self.base_dir='/sys/bus/w1/devices/'
        except:
            print "ERROR: Module 'w1-gpio' or 'w1-therm' not found"
            exit()
			
	try:
            self.device_folder=glob.glob(self.base_dir + '28*')[0]
            self.device_file=self.device_folder + '/w1_slave'
 	    print self.device_file
        except:
            print "ERROR: Temperature probe not found!!"
            exit()
	self.start_time()	

    def start_time(self):
        #store time of start (in seconds)
	self.start_time=time.time()
	
    def get_current_time(self):
        #get time elapsed from start brewing (in seconds)
	return time.time()-self.start_time

    def save(self,heat):
        #storing each value of temp/time/heat on its own list for plotting later
	self.history_temp.append(self.get_temp())
        self.history_time.append(self.get_current_time())
        self.history_heat.append(heat.get_status())
	
    def get_temp(self):
        return self.t
	
    def read_temp_raw(self):
        f = open(self.device_file,'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            self.t = float(temp_string)/1000

    def increase_to(self,target,heat):
        self.read_temp()
        self.target=target
        start_t=self.t
        elapsed=0.1
        ## bottom error: 1 degree
	while float(self.t)<(float(target)-1):
            ## switch on heat
	    if(heat.get_status()==0):
                heat.on()
            ## cycle every TIMECYCLE sec
	    time.sleep(self.TIMECYCLE)
            elapsed+=(self.TIMECYCLE/60)
            self.read_temp()
            self.tot_time+=(self.TIMECYCLE/60)
	    self.save(heat)
	## target reached
	heat.off()
	ramp=float((float(self.t)-float(start_t))/elapsed)
	print "Stats: %.2fC | %.2fC | %.2fmin | %.2fC/min" % (start_t,self.t,elapsed,ramp)
	return elapsed

    def decrease_to(self,target,heat):
	    self.read_temp()
	    self.target=target
	    start_t=self.t
	    elapsed=0.1
	    while math.ceil(self.t)>target:
		## spegni resistenza
		if(heat.get_status()==1):
			heat.off()		
		##print "HEAT OFF"		
		## cycle every 30sec
		time.sleep(self.TIMECYCLE)
		elapsed+=(self.TIMECYCLE/60)
		self.tot_time+=(self.TIMECYCLE/60)
		self.read_temp()
		self.save(heat)
		##print "Temperature"+str(self.t)+"/"++str(target)
	    ## target reached
	    ramp=float((float(start_t)-float(self.t))/elapsed)
	    print "Stats: %.2fC | %.2fC | %.2fmin | %.2fC/min" % (start_t,self.t,elapsed,ramp)
	    return elapsed

    def boil(self,fortime,heat):
	    self.read_temp()
	    elapsed=0.1
	    while elapsed<fortime:
		## switch on heat
		if (heat.get_status() == 0):
		    heat.on()
		## cycle every TIMECYCLE sec
		time.sleep(self.TIMECYCLE)
		elapsed += (self.TIMECYCLE / 60)
		self.read_temp()
		self.tot_time += (self.TIMECYCLE / 60)
		self.save(heat)
	    ## target reached
	    heat.off()
	    print "Stats: %.2fmin | %.2fC" % (elapsed,self.t)
	    return elapsed


    def keep_constant(self,target,fortime,heat):
	    print "keep constant"
	    self.read_temp()
	    self.target=target
	    elapsed = 0.1
	    min_t=target
	    max_t=target
	    while elapsed<fortime:
		min_t=min(min_t,self.t)
		max_t=max(max_t,self.t)
		if math.ceil(self.t)<target:
		    e=self.increase_to(target,heat)
		    elapsed+=e	
		else:
		    e=self.decrease_to(target,heat)
		    elapsed+=e
		    time.sleep(self.TIMECYCLE)
		    elapsed+=(self.TIMECYCLE/60)
		    self.tot_time+=(self.TIMECYCLE/60)
	    ##print "Stats: %.2fC | %.2fC | %.2fmin | %.2fC | %.2fC" % (start_t,self.t,elapsed, max_t, min_t)
	    heat.off()
	    return elapsed
		


if __name__=='__main__':
	temperature=Temp()
	##heat=Relay.Relay(21)
	
	##print "Testing increasing temperature..."
	##elapsed_time = temperature.increase_to(55,heat)
	
	##print "Testing decreasing temperature..."
	##elapsed_time = temperature.decrease_to(52,heat)
	
	##print "Testing constant temperature..."
	##elapsed_time = temperature.keep_constant(55,5,heat,0,0)
	
	while 1:
		temperature.read_temp()
		print temperature.t
		time.sleep(5)	
	

		
	
		
