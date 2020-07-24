import telepot
import time
import sys
from telepot.loop import MessageLoop

class Telegram:

	TOKEN= "830412257:AAF2ktzaGT2VqRAOFwlmRIeP0m8JQkBbVDA"
	bot=0
	chat_id=0
	##variable to be sent in chat
	temp=0
	status=0
	time=0
	t=0
	

	def __init__(self):
		self.bot=telepot.Bot(self.TOKEN)
	
	def update_variables(self,status,temp,time):
		self.temp=temp
		self.status=status
		self.time=time

	def handle(self,msg):
		content_type, chat_type, chat_id=telepot.glance(msg)
		self.chat_id=chat_id
		if content_type == 'text':
			STRING="comando non riconosciuto\ncomandi:time,temp,status,update"
			if "temp" in msg['text'].lower():
				STRING="temp: "+str(self.temp)
			elif "status" in msg['text'].lower():
				STRING="status: "+str(self.status)
			elif "time" in msg['text'].lower():
				STRING="missing time: "+str(self.time)
			elif "update" in msg['text'].lower():
				STRING="temp: "+str(self.temp)+"\nstatus: "+str(self.status)+"\ntime: "+str(self.time)

			self.bot.sendMessage(chat_id, STRING )



if __name__ == "__main__":
	t=Telegram()
	MessageLoop(t.bot, t.handle).run_as_thread()
	print("Listening...")
	while 1:
		time.sleep(10)



	
	


