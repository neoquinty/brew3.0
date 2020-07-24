import paho.mqtt.client as mqtt
import time


def messageFunction(client,userdata,msg):
	topic = str(msg.topic)
	msg = str(msg.playload.decode("utf-8"))
	print( topic+msg )

client = mqtt.Client("rpi_client_01")
client.connect("192.168.86.111",1883)

#client.subscribe("brew/temperature")

#client.on_message = messageFunction
client.loop_start()


temp=22
while(1):
	client.publish("brew/temperature", str(temp))
	time.sleep(1)
	print(str(temp))
	temp=temp+1	
