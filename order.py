from datetime import datetime
from uuid import uuid4

from enum import Enum

def _get_curr_time():
		now = datetime.now()
		return now.strftime("%H:%M:%S")

class Order:
	def __init__(self, symbol, direction, quantity, price=0):
		self._time_stamp = _get_curr_time()
		self._symbol = symbol
		self._direction = direction
		self._quantity = quantity
		self._orderId = uuid4()
		if price == 0:
			self._orderType = "MarketOrder"
			self._price = 0
		else:
			self._orderType = "LimitOrder"
			self._price = price
		
	def to_string(self ):
		return str(self._orderId)+'_'+self._orderType+'_'+self._time_stamp+'_'+self._symbol+'_'+self._direction+'_'+str(self._quantity)+'_'+str(self._price)