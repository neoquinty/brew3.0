import paho.mqtt.client as mqtt
import time

def on_connect(client,userdata,flags,rc):
	if rc == 0:
		print( "subscriber connected to broker" )
		client.subscribe("brew/temperature")
		client.subscribe("brew/heat")
	else:
		print( "subscriber connection failed" )


def on_message(client,userdata,msg):
	if msg.topic=="brew/temperature":
		print( "temp: "+str(msg.payload) )
	elif msg.topic=="brew/heat":
		print( "heat: "+str( msg.payload) )

client = mqtt.Client("rpi_client_02")

user="root"
password="raspberry"
port=1883
broker="192.168.86.111"

client.username_pw_set(user,password=password)
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker,port=port)

#client.loop_start()

client.loop_forever()

#try:
#	while True:
#		time.sleep(1)
#except KeyboardInterrupt:
#	print( "exiting" )
#	client.disconnect()
#	client.loop_stop()


