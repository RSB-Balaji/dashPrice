from engine import Engine
from db_connector import DbConnector

from exchange_db_query import ExchangeDbQuery

from order import Order

from enum import Enum
import socket
from uuid import uuid4
import threading

import matplotlib.pyplot as plt

lock = threading.Lock()

class Status(Enum):
	ACCEPT = "Accepted"
	REJECT = "Rejected"
	NOFILL = "No_Fill"
	PARTFILL = "Part_Fill"
	FULLFILL = "Full_Fill"

class Exchange:
	BOOK_EXTENSION = 'order_book'
	players_list = []

	def __init__(self ):
		self._conn = DbConnector('postgres', 5000, 'postgres', 'localhost')
		self._engine = Engine()
		self._symbol_list = self._get_all_symbols()
	
	def _clear_all_order_books(self ):
		symbols = self._get_all_symbols()
		direcion = ['buy', 'sell']
		for i in symbols:
			book_name = '_'.join((self.BOOK_EXTENSION,str(i)))
			for j in direcion:
				bn = '_'.join((book_name,j))
				query = ExchangeDbQuery._clear_table_query().format(bn)
				self._conn.execute(query)

	def _clear_trade_table(self ):
		query = ExchangeDbQuery._clear_table_query().format('TRADE')
		self._conn.execute(query)

	def _clear_players_orders_table(self ):
		query = ExchangeDbQuery._clear_table_query().format('players_orders')
		self._conn.execute(query)
		
	def _get_all_symbols(self ):
		query =  ExchangeDbQuery._select_symbols_query()
		self._conn.execute(query)
		row = self._conn._cursor.fetchall()
		symbol_list = [str(i[0]) for i in row]
		return symbol_list

	def _get_best_price(self, book_name):
		direcion = book_name.split('_')[3]
		if direcion == 'buy':
			query = ExchangeDbQuery.best_buy_price_query().format(book_name)
		else:
			query = ExchangeDbQuery.best_sell_price_query().format(book_name)
		try:
			self._conn.execute(query)
			price = self._conn._cursor.fetchone()[0]
			return price
		except Exception as e:
			print("Error ",e)
			return None

	def _start_engine(self, symbol):
		book_name = self.BOOK_EXTENSION+'_'+symbol
		self._engine.match_order(book_name)

	def _plot_stock_price(self ):
		query = ExchangeDbQuery.select_price_from_trade_table_query()
		self._conn.execute(query)
		p = self._conn._cursor.fetchall()
		price = [i[0] for i in p]
		t = list(range(len(price)))
		plt.plot(t, price)
		plt.xlabel("Timesteps:{}".format(len(t)))
		plt.show()

	def _insert_into_order_book(self, order):
		order = order.split('_')

		player_id = order[0]
		order_id = order[1]
		order_type = order[2]
		time_stamp = order[3]
		symbol = order[4]
		direcion = order[5]
		quantity = int(order[6])
		price = float(order[7])

		if order_type == 'MarketOrder':
			d = "buy" if direcion == "sell" else "sell"
			bn = self.BOOK_EXTENSION+'_'+symbol+'_'+d
			p = self._get_best_price(bn)
			if p == None:
				return Status.REJECT
			else:
				price = p

		book_name = self.BOOK_EXTENSION+'_'+symbol+'_'+direcion

		query = ExchangeDbQuery.insert_order_into_order_book_query().format(book_name, player_id, order_id, time_stamp, quantity, price)
		try:
			self._conn.execute(query)
			return Status.ACCEPT
		except Exception as e:
			print("Error :",e)
			return Status.REJECT

	def receive_order(self, conn):
		order = conn.recv(1024).decode()
		status = str(self._insert_into_order_book(order))
		conn.send(status.encode())

