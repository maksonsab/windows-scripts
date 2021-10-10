import socket
import os
import time
import json



class VPN_connection(object):
	
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
			LOGIN = input('Enter VPN login: '),
			PASSWORD = input('Input password: '),
			VPN_GATE = input('Enter VPN gate'),
			TIMEOUT = 60, 
			DEBUG = True)
		
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

	#pinging VPN host
	def checking_VPN(self): 
		answer = os.system('ping '+ self.params['VPN_GATE'])
		if self.params['DEBUG']:
			print('Pinging status:',answer) #if 1 no connection
		return answer
	
	#connecting to vpn
	def connect_vpn(self):
		if self.params['DEBUG']:
			print('Connecting to {} with login {}.'.format(self.params['CONNECTION_NAME'], self.params['LOGIN']))
		else:
			print('Connecting VPN')
		os.system('rasdial.exe {} {} {}'.format(self.params['CONNECTION_NAME'], self.params['LOGIN'], self.params['PASSWORD']))

def main():
	vpn = VPN_connection()
	while True:
		if VPN_connection.internet_connection():	#есть ли интернет
			VPN_connection.connect_vpn() #цепляем керио
			while True:
				if not VPN_connection.checking_VPN(): #пинг шлюза возвращает 0, если есть пинги и 1 если нет 
					os.system('cls')
					print('VPN connected!')
					time.sleep(VPN_connection.params['TIMEOUT'])
				else: #если пингов нет, то чекаем интернет соединение
					if VPN_connection.internet_connection(message=False):# если интернета нет, то ломаем второй бесконечный цикл
						VPN_connection.connect_vpn()
					else:
						break #попадаем на первый 
		else:
			time.sleep(VPN_connection.params['TIMEOUT'])
			continue



if __name__ == '__main__':
	main()
