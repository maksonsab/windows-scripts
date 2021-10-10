import socket
import os
import time
import json



class Kerio(object):
	
	def __init__(self):
		try:
			with open('config.cfg', 'r') as f:
				self.params = json.loads(f.read())
				if self.params['DEBUG']:
					print('Configuration:', self.params)
		except FileNotFoundError as e:
			self.params = dict()
			self.params.update(
			CONNECTION_NAME = input('Enter VPN-connection name: '),
			LOGIN = input('Enter Kerio login: '),
			PASSWORD = input('Input password: '),
			KERIO_GATE = input('Enter Kerio gate (empty == 172.27.21.1)'),
			TIMEOUT = 60, 
			DEBUG = True)
			if not self.params['KERIO_GATE']:
				self.params['KERIO_GATE'] = '172.27.21.1'
			with open('config.cfg','w') as f:
				f.write(json.dumps(self.params, sort_keys=True, indent=4))

	@staticmethod	#checking internet connection	
	def internet_connection(message=True): 
		try:
			connection = socket.create_connection(('77.88.55.77',443),2) #yandex
			print('Internet Connected!')
			connection.close()
			return True
		except	Exception:
			if message:
				print('Problems with internet!')
			return False

	#pinging kerio host
	def checking_kerio(self): 
		answer = os.system('ping '+ self.params['KERIO_GATE'])
		if self.params['DEBUG']:
			print('Pinging status:',answer) #if 1 no connection
		return answer
	
	#connecting to kerio-vpn
	def connect_kerio(self):
		if self.params['DEBUG']:
			print('Connecting to {} with login {}.'.format(self.params['CONNECTION_NAME'], self.params['LOGIN']))
		else:
			print('Connecting Kerio')
		os.system('rasdial.exe {} {} {}'.format(self.params['CONNECTION_NAME'], self.params['LOGIN'], self.params['PASSWORD']))

def main():
	kerio = Kerio()
	while True:
		if kerio.internet_connection():	#есть ли интернет
			kerio.connect_kerio() #цепляем керио
			while True:
				if not kerio.checking_kerio(): #пинг шлюза возвращает 0, если есть пинги и 1 если нет 
					os.system('cls')
					print('Kerio connected!')
					time.sleep(kerio.params['TIMEOUT'])
				else: #если пингов нет, то чекаем интернет соединение
					if kerio.internet_connection(message=False):# если интернета нет, то ломаем второй бесконечный цикл
						kerio.connect_kerio()
					else:
						break #попадаем на первый 
		else:
			time.sleep(kerio.params['TIMEOUT'])
			continue



if __name__ == '__main__':
	main()
