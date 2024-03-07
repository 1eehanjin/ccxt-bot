# -*- coding: utf-8 -*-

import os
import sys
import math
import pprint
import ccxt
import time
from itertools import combinations
from modules.message_dumper import *

class ArbitrageFinder:
    #EXCEPT_SYMBOLS = ['ALT/USDT', 'ANT/USDT', 'BEAM/USDT', 'DEFI/USDT', 'FMC/USDT', 'FON/USDT', 'GMT Token/USDT', 'MDT/USDT', 'MULTI/USDT',  'VELO/USDT', 'XMR/USDT']

    
    EXCEPT_SYMBOLS_DICT = {
        "binance": ['XMR/USDT', 'MULTI/USDT','ANT/USDT'],
        "binance_swap": ['DEFI/USDT'],
        "bybit": ['FMC/USDT'],
        "bybit_swap": [],
        "mexc": ['MDT/USDT','GMT Token/USDT', 'ALT/USDT','BEAM/USDT','GPT/USDT'],
        "mexc_swap": [],
        "bitget": ['VELO/USDT', 'ALT/USDT'],
        "bitget_swap": [],
        "gateio": ['BTG/USDT', 'YFII/USDT'],
        "gateio_swap": ['BTG/USDT', 'YFII/USDT']

    }


    def __init__(self, min_volume, min_gap):
        self.previous_gap_infos = []
        self.min_volume= min_volume
        self.min_gap = min_gap
        self.exchanges = {
            "binance" :ccxt.binance(),
            "binance_swap": ccxt.binance(config={
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'swap'
                }
            }),
            "bybit" : ccxt.bybit(config={
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'spot'
                },
            }),
            "bybit_swap" : ccxt.bybit(config={
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'swap'
                },
            }),
            # "mexc" : ccxt.mexc(),
            # "mexc_swap": ccxt.mexc(config={
            #     'enableRateLimit': True,
            #     'options': {
            #         'defaultType': 'swap'
            #     },
            # }),
            "bitget" : ccxt.bitget(),
            "bitget_swap": ccxt.bitget(config={
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'swap'
                },
            }),
            # "gateio" : ccxt.gateio(),
            # "gateio_swap": ccxt.gateio(config={
            #     'enableRateLimit': True,
            #     'options': {
            #         'defaultType': 'swap'
            #     },
            # })
        }
        self.ids = self.exchanges.keys()

    def retrieve_spot_future_gaps(self):
        
        self.load_tickers()
        arbitrableSymbols = self.retrieve_arbitrable_symbols()
        self.exchange_table_strings = []
        self.arbitrage_table = {}
        self.gap_symbols = []

        for symbol in arbitrableSymbols:
            if self.is_gap_symbol(symbol):
                self.gap_symbols.append(symbol)

        #self.print_exchange_table()
        print(self.gap_symbols)

        gap_infos = []

        for gap_symbol in self.gap_symbols:
            #dump(yellow(gap_symbol))
            gap_combinations = self.generate_gap_combinations(gap_symbol)

            for gap_combination in gap_combinations:
                gap_info = self.generate_gap_info(gap_symbol, gap_combination)
                gap = gap_info.get_gap()
                if gap > self.min_gap:
                    gap_infos.append(gap_info)


        #TODO: 여기 구조 수정
        for gap_info in gap_infos:
            self.perform_gap_action(gap_info)

        


        self.remove_not_updated_gap_infos()
        return self.previous_gap_infos


    def is_gap_symbol(self, symbol):
        self.arbitrage_table[symbol] = {}
        self.arbitrage_table[symbol]['min'] = math.inf
        self.arbitrage_table[symbol]['max'] = -math.inf
        
        for id in self.ids:
            self.retrieve_pair(id, symbol)
            
        self.arbitrage_table[symbol]['gap'] = (self.arbitrage_table[symbol]['max']  / self.arbitrage_table[symbol]['min'])

        if  self.arbitrage_table[symbol]['gap'] > self.min_gap :
            return True
        else:
            return False

    def retrieve_pair(self, exchange_id, symbol):
        string = ' {:<20} | '.format(symbol)

        if self.is_perpetual_exchange(exchange_id):
            swap_symbol = symbol + ':USDT'
        else:
            swap_symbol = symbol

        try:
            if swap_symbol in self.tickers[exchange_id].keys() and self.tickers[exchange_id][swap_symbol]['quoteVolume'] > self.min_volume:
                if(symbol in ArbitrageFinder.EXCEPT_SYMBOLS_DICT[exchange_id] ):
                    raise ValueError("invalid exchange_id value ticker")
                string += blue(' {:<20} '.format(self.tickers[exchange_id][swap_symbol]['close'] )) + '| '
                close =float(self.tickers[exchange_id][swap_symbol]['close'])
                if close > self.arbitrage_table[symbol]['max']:
                    self.arbitrage_table[symbol]['max'] = close
                    self.arbitrage_table[symbol]['max_exchange'] = exchange_id
                if close < self.arbitrage_table[symbol]['min']:
                    self.arbitrage_table[symbol]['min'] = close
                    self.arbitrage_table[symbol]['min_exchange'] = exchange_id
            else:
                string += blue(' {:<20} '.format('' )) + '| '        
        except Exception as e:
            string += ' {:<20} | '.format('error')
        self.exchange_table_strings.append(string)

    def load_tickers(self):
        self.tickers = {}
        for id in self.ids:
            exchange = self.exchanges[id]
            self.tickers[id] = exchange.fetch_tickers()
            #dump(green(id), 'loaded', green(str(len(self.tickers[id].keys()))), 'markets')

    def retrieve_arbitrable_symbols(self):
        allSymbols = [symbol.replace(":USDT", "") for id in self.ids for symbol in self.tickers[id].keys()]
        uniqueSymbols = list(set(allSymbols))
        arbitrableSymbols = sorted([symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])
        return arbitrableSymbols

    def print_exchange_table_header(self):
        dump(green(' symbol               | ' + ''.join([' {:<20} | '.format(id) for id in self.ids])))
        dump(green(''.join(['----------------------+-' for x in range(0, len(self.ids) + 1)])))

    def print_exchange_table(self):
        self.print_exchange_table_header()
        for string in self.exchange_table_strings:
            dump(string)

    def generate_gap_combinations(self, symbol):
        gap_ticker_infos = []
        for id in self.ids:
            if(symbol in ArbitrageFinder.EXCEPT_SYMBOLS_DICT[id] ):
                continue
            if self.is_perpetual_exchange(id):
                ticker_symbol = symbol + ':USDT'
            else:
                ticker_symbol = symbol
            try:    
                ticker_info = self.tickers[id][ticker_symbol]
                ticker_info['id'] = id
                if ticker_info['close'] is None:
                    raise ValueError
                gap_ticker_infos.append(ticker_info)
                
            except Exception as e:
                continue
            gap_ticker_infos = sorted(gap_ticker_infos, key=lambda x:x['close'], reverse = True)
        return list(combinations(gap_ticker_infos, 2))

    def generate_gap_info(self,symbol, sorted_gap_combination):
        return GapInfo(symbol, sorted_gap_combination[0], sorted_gap_combination[1])     
        
    def perform_gap_action(self, gap_info):
        #self.dump_gap_info(gap_info)
        gap_category = gap_info.get_category()
        if gap_category =="현선갭":
            previous_gap_exists = False
            length = len(self.previous_gap_infos)
            for i in range(length):
                if self.previous_gap_infos[i].is_match(gap_info):
                    self.previous_gap_infos[i].increase_count()
                    previous_gap_exists = True
                    break
            if not previous_gap_exists:
                self.previous_gap_infos.append(gap_info)

    def dump_gap_info(self, gap_info):
        dump(str(gap_info))
        # dump( (' {:<15} '.format(sorted_gap_combination[0]['id'] )) + '| '+ green(' {:<20} '.format(sorted_gap_combination[0]['close'] ))  )
        # dump( (' {:<15} '.format(sorted_gap_combination[1]['id'] )) + '| '+ green(' {:<20} '.format(sorted_gap_combination[1]['close'] ))  )

    def remove_not_updated_gap_infos(self):
        new_list = []
        for previous_gap_info in self.previous_gap_infos:
            if previous_gap_info.is_updated:
                previous_gap_info.init_is_updated()
                new_list.append(previous_gap_info)
        self.previous_gap_infos = new_list

        

    def is_perpetual_exchange(self, id):
        return  '_swap' in id
    
class GapInfo:
    def __init__(self, symbol, exchange1_info, exchange2_info):
        self.symbol = symbol
        self.exchange1_info = exchange1_info
        self.exchange2_info = exchange2_info
        self.is_updated = True
        self.count = 1
    def init_is_updated(self):
        self.is_updated = False
    def increase_count(self):
        self.is_updated = True
        self.count = self.count + 1
    def is_match(self, another_gap_info):
        if self.symbol == another_gap_info.symbol and self.exchange1_info['id'] == another_gap_info.exchange1_info['id'] and self.exchange2_info['id'] == another_gap_info.exchange2_info['id']:
            return True
        else:
            return False
        
    def get_category(self):
        is_exchange1_swap = '_swap' in self.exchange1_info['id']
        is_exchange2_swap = '_swap' in self.exchange2_info['id']

        if is_exchange1_swap and is_exchange2_swap:
            return "선선갭"
        elif is_exchange1_swap:
            return "선현갭" #선물이 더 비싼 갭
        elif is_exchange2_swap:
            return "현선갭" #현물이 더 비싼 갭
        else:
            return "현현갭"
        
    def get_gap(self):
        return self.exchange1_info['close'] / self.exchange2_info['close']

    def __repr__(self):
        return f'gap_info({self.symbol}, {self.get_category()}, {self.get_gap()}, {self.exchange1_info["id"]}, {self.exchange2_info["id"]}, {self.count})'
    

if __name__ == '__main__': 

    arbitrage_finder = ArbitrageFinder(min_volume=50000, min_gap=1.02)

    for i in range(5):
        start_time = time.time()
        pprint.pprint(arbitrage_finder.retrieve_spot_future_gaps())
        end_time = time.time()
        execution_time = end_time - start_time
        print("프로그램 실행 시간:", execution_time, "초")

    

