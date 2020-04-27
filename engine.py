from db_connector import DbConnector
from exchange_db_query import ExchangeDbQuery

from uuid import uuid4
from enum import Enum
from datetime import datetime

class Status(Enum):
    NOFILL = 'No_Fill'
    PARTFILL = 'Partial_Fill'
    FULLFILL = 'Full_Fill'

class Engine:
    BOOK_EXTENSION = 'order_book'

    def __init__(self ):
        self._engine_id = uuid4()
        self._conn = DbConnector('postgres', 5000, 'postgres', 'localhost')

    def _get_curr_time(self ):
        now = datetime.now()
        return now.strftime("%H:%M:%S")
# Db updation
    def update_order_quantity(self, order_id, quantity, book_name):
        if quantity == 0:
            self._conn.execute(ExchangeDbQuery._delete_zero_quantity_query().format(book_name, order_id))
        else:
            self._conn.execute(ExchangeDbQuery._update_modified_quantity_query().format(book_name, quantity, order_id))

    def update_trade_info(self, symbol, buy_order_id, sell_order_id, time_stamp, trade_price, sell_quantity, buy_quantity, trade_quantity):
        query = ExchangeDbQuery._insert_into_trade_table().format(symbol, buy_order_id, sell_order_id, time_stamp, trade_quantity, trade_price)
        self._conn.execute(query)

# Best price 
    def _get_best_buy_price(self, book_name):
        query = ExchangeDbQuery.best_buy_price_query().format(book_name+'_buy')
        try:
            self._conn.execute(query)
            price = self._conn._cursor.fetchone()[0]
            return price
        except Exception as e:
            return None

    def _get_best_sell_price(self, book_name):
        try:
            query = ExchangeDbQuery.best_sell_price_query().format(book_name+'_sell')
            self._conn.execute(query)
            price = self._conn._cursor.fetchone()[0]
            return price
        except Exception as e:
            return None

    def if_trade_possible(self, book_name):
        best_buy = self._get_best_buy_price(book_name)
        best_sell = self._get_best_sell_price(book_name)

        if best_sell == None or best_buy == None:
            return False
        elif best_sell <= best_buy:
            return True

# Matching 
    def match_order(self, book_name):
        symbol = book_name.split('_')[2]
        while True:
            if self.if_trade_possible(book_name):
                try:
                    sell_top_level_query = ExchangeDbQuery.get_sell_top_level_query().format(book_name+'_sell')
                    self._conn.execute(sell_top_level_query)
                    sell_order = self._conn._cursor.fetchone()

                    sell_player_id = sell_order[1]
                    sell_order_id = sell_order[2]
                    sell_quantity = sell_order[4]
                    sell_price = sell_order[5]

                    buy_top_level_query = ExchangeDbQuery.get_buy_top_level_query().format(book_name+'_buy')
                    self._conn.execute(buy_top_level_query)
                    buy_order = self._conn._cursor.fetchone()

                    buy_player_id = buy_order[1]
                    buy_order_id = buy_order[2]
                    buy_quantity = buy_order[4]
                    buy_price = buy_order[5]

                    trade_quantity = 0 

                    if buy_quantity >= sell_quantity:
                        buy_quantity -= sell_quantity
                        trade_quantity = sell_quantity
                        sell_quantity = 0

                    else:
                        sell_quantity -= buy_quantity
                        trade_quantity = buy_quantity
                        buy_quantity = 0

                    time_stamp = self._get_curr_time()
                    self.update_order_quantity(sell_order_id, sell_quantity, book_name+'_sell')
                    self.update_order_quantity(buy_order_id, buy_quantity, book_name+'_buy')

                    self.update_trade_info(symbol, buy_order_id, sell_order_id, time_stamp, buy_price, sell_quantity, buy_quantity, trade_quantity)
                except:
                    continue

