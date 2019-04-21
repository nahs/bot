# -*- coding: utf-8 -*- 
import time 
from multiprocessing.dummy import Pool as ThreadPool 
from multiprocessing import Process 
import websocket
import json
ws = websocket.WebSocket()
ws.connect("wss://o7.click/api/ws?key=qhs0uaf9fa")

created_bots = {} 

pool = ThreadPool(8)

'''[inst]

[__init__(ид бота, логин, пароль) - ,
main() - бесконечное создание процессов для обновления сообщнений,
first_mess() - собирает всех пользователей и игнорит их, если после включения бота, они не пишут,
send_to_json(id) - пакует данные в json и отправляет на сервер,
update() - делает тоже самое, что и first_mess, но не игнорит пользователей,
send_to_client(js) - отправляет ответы от сервера в инстаграм]
'''
class inst(): 
	from instabot import Bot 
	def __init__(self, id, username, password):
		print('begin', id, username, password)
		self.id = id 
		self.username = username 
		self.password = password 
		self.users = [] # id пользователей
		self.usernames = [] 
		self.fullnames = [] 
		self.messages = [] # messages и old_messages нужны для того, чтобы не спамить серверу одинаковые сообщения пользователей
		self.old_messages = [] 
		self.skip_users = [] # для игнора пользователей, которые писали до включения бота
		self.skip_messages = [] 
		self.bot = Bot() 
		self.bot.login(username = self.username, password = self.password) 
		self.pool = ThreadPool(8) 
		main(self) 
 
	def main(self): 
		first_mess(self) 
		while True: 
			update() 
			pool.map(sends_message, users) 
			time.sleep(3) 
 
	def first_mess(self): 
		all_mess = self.bot.get_messages() # парсит сообщения из деректа и собирает все данные о пользователях
		for i in range(len(all_mess['inbox']['threads'])): 
			try: 
				user_id = all_mess['inbox']['threads'][i]['items'][-1]['user_id'] 
			except: 
				pass 
			try: 
				username = all_mess['inbox']['threads'][i]['users'][-1]['username'] 
			except: 
				pass 
			try: 
				fullname = all_mess['inbox']['threads'][i]['users'][-1]['full_name'] 
			except: 
				fullname = 'None' 
			try: 
				message = all_mess['inbox']['threads'][i]['items'][-1]['text'] 
			except: 
				message = 'text' 
			if message == '': 
				message = 'text' 
			self.skip_users.append(user_id) 
			self.skip_messages.append(message) 
			self.old_messages.append(message) 
 
	def send_to_json(self, user_id): 
		message = self.messages[users.index(user_id)] 
		if message != self.old_messages[user_id]: 
			username = self.usernames[users.index(user_id)] 
			fullname = self.fullnames[users.index(user_id)] 
			js = json.dumps({'type': 'text', 'text' : message, 'bot': self.id, 'user': user_id, 'info': {'nickname':username,'name':fullname}})
			self.old_messages[user_id] = message 
			send_to_server(js) 
 
	def update(self): 
		all_mess = self.bot.get_messages() # парсит сообщения из деректа и собирает все данные о пользователях
		for i in range(len(all_mess['inbox']['threads'])): 
			try:  
				user_id = all_mess['inbox']['threads'][i]['items'][-1]['user_id'] 
			except: 
				pass 
			try: 
				username = all_mess['inbox']['threads'][i]['users'][-1]['username'] 
			except: 
				pass 
			try: 
				fullname = all_mess['inbox']['threads'][i]['users'][-1]['full_name'] 
			except: 
				fullname = 'None' 
			try: 
				message = all_mess['inbox']['threads'][i]['items'][-1]['text'] 
			except: 
				message = 'text' 
			if message == '': 
				message = 'text' 
			if str(user_id) not in str(self.users): 
				self.users.append(user_id) 
				self.messages.append(message) 
				self.usernames.append(username) 
				self.fullnames.append(fullname) 
				send_to_json(self, user_id) 
			else: 
				if self.messages[users.index(user_id)] != message: 
					self.messages[users.index(user_id)] = message 
					send_to_json(self, user_id) 
 
	def send_to_client(self, js): 
		if js['type'] == 'text': 
			user_id = str(js['user']) 
			message = str(js['text']) 
			self.bot.send_message(message, user_id) 
		elif js['type'] == 'media': 
			user_id = str(js['user']) 
			media = str(js['media'])
			self.bot.send.media(media, user_id)
 
'''[send_to_server]

[send_to_server(js) - отправляет данные от бота серверу, 
recv - прослушивание порта на новые сообщения]
'''
def send_to_server(js): 
	ws.send(js)`
 
def recv():
	print('recv')
	while True:
		global created_bots
		print() 
		result = ws.recv()
		if result:
			js = json.loads(result)
			print(js)
			if js['type'] == 'create_bot':
				proc = Process(target=inst, args=(js["bot"], js["login"], js["password"])) 
				proc.start() 
				proc.join() 
				created_bots[js['bot']] = [js['login'], proc.name(), proc] 
			elif js['type'] == 'update_bot':
				kill(created_bots[js['bot']][1])
				proc = Process(target=inst, args=(js["bot"], js["login"], js["password"])) 
				proc.start() 
				proc.join() 
				created_bots[js['bot']] = [js['login'], proc.name(), proc]
			elif js['type'] == 'text' or js['type'] == 'media':  
				created_bots[js['bot']][2].send_to_client(js)

 
forever = Process(target=recv) 
forever.start()
forever.join()