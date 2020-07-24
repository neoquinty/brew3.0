from paho.mqtt.client import Client


client = Client(client_id="client_1")


def on_publish(client, userdata, mid):
    print("Messaggio pubblicato")

client.on_publish = on_publish

client.connect("192.168.86.111")
client.loop_start()

messaggio = "22"
client.publish(topic = "test", payload = messaggio)

client.loop_stop()
client.disconnect()
