from exchange import Exchange
from exchange_db_query import ExchangeDbQuery
from exchange import Status

from uuid import uuid4
from datetime import datetime
import socket
import threading

class Player:
	host = '127.0.0.1'
	port = 12345

	def __init__(self , playerName):
		self._player_id = uuid4()
		self._player_name = playerName

	def _get_socket(self ):
		return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def _get_curr_time(self ):
		now = datetime.now()
		return now.strftime("%H:%M:%S")
		
	def send_order_to_exchange(self, order):
		try:
			self.s = self._get_socket()
			self.s.connect((self.host, self.port))
			order = str(self._player_id)+'_'+order
			self.s.send(order.encode())
			status = self.s.recv(1024).decode()
			self.s.close()
		except Exception as e:
			print("error sending order to exchange:",e)
