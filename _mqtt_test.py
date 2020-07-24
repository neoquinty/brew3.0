import glob
import time
import paho.mqtt.publish as publish

Broker = '192.168.86.111'
auth = {
    'username': 'root',
    'password': 'raspberry',
}

pub_topic = 'test/temperature'

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-*')[0]
device_file = device_folder + '/w1_slave'

def read_temp():
    valid = False
    temp = 0
    with open(device_file, 'r') as f:
        for line in f:
            if line.strip()[-3:] == 'YES':
                valid = True
            temp_pos = line.find(' t=')
            if temp_pos != -1:
                temp = float(line[temp_pos + 3:]) / 1000.0

    if valid:
        return temp
    else:
        return None


while True:
    temp = read_temp()
    print( "Temp: "+str(temp) )
    if temp is not None:
        publish.single(pub_topic, str(temp), hostname=Broker, port=1883, auth=auth, tls={})
    time.sleep(1)
