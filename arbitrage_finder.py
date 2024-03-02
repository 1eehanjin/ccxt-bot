# -*- coding: utf-8 -*-

import os
import sys
import math
import pprint
import ccxt
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
        "bitget_swap": []
    }
    MIN_VOLUME= 100000

    def __init__(self):
        
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
            "mexc" : ccxt.mexc(),
            "mexc_swap": ccxt.mexc(config={
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'swap'
                },
            }),
            "bitget" : ccxt.bitget(),
            "bitget_swap": ccxt.bitget(config={
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'swap'
                },
            })
        }
        self.ids = self.exchanges.keys()
        dump(yellow(' '.join(self.ids)))

    def retrieve_gap_symbols(self):
        self.tickers = {}
        self.load_tickers()

        arbitrableSymbols = self.retrieve_arbitrable_symbols()
        
        self.print_arbitrage_table_header()

        arbitrage_table = {}
        gap_symbols = []
        for symbol in arbitrableSymbols:
            
            string = ' {:<20} | '.format(symbol)
            arbitrage_table[symbol] = {}
            arbitrage_table[symbol]['min'] = math.inf
            arbitrage_table[symbol]['max'] = -math.inf
            
            for id in self.ids:
                if self.is_perpetual_exchange(id):
                    try:
                        swap_symbol = symbol + ':USDT'
                        if swap_symbol in self.tickers[id].keys() and self.tickers[id][swap_symbol]['quoteVolume'] > ArbitrageFinder.MIN_VOLUME:
                            if(symbol in ArbitrageFinder.EXCEPT_SYMBOLS_DICT[id] ):
                                raise ValueError("invalid value ticker")
                            string += blue(' {:<20} '.format(self.tickers[id][swap_symbol]['close'] )) + '| '
                            close =float(self.tickers[id][swap_symbol]['close'])
                            
                            if close > arbitrage_table[symbol]['max']:
                                arbitrage_table[symbol]['max'] = close
                                arbitrage_table[symbol]['max_exchange'] = id
                            if close < arbitrage_table[symbol]['min']:
                                arbitrage_table[symbol]['min'] = close
                                arbitrage_table[symbol]['min_exchange'] = id
                        else:
                            string += blue(' {:<20} '.format('' )) + '| '
                            
                    except Exception as e:
                        string += ' {:<20} | '.format('error')
                else:
                    try:
                        if symbol in self.tickers[id].keys() and self.tickers[id][symbol]['quoteVolume'] > ArbitrageFinder.MIN_VOLUME:
                            if(symbol in ArbitrageFinder.EXCEPT_SYMBOLS_DICT[id] ):
                                raise ValueError("invalid value ticker")
                            string += ' {:<20} | '.format(self.tickers[id][symbol]['close'] )
                            close =float(self.tickers[id][symbol]['close'])
                            if close> arbitrage_table[symbol]['max']:
                                arbitrage_table[symbol]['max'] = close
                                arbitrage_table[symbol]['max_exchange'] = id
                            if close < arbitrage_table[symbol]['min']:
                                arbitrage_table[symbol]['min'] = close
                                arbitrage_table[symbol]['min_exchange'] = id
                        else:
                            string += ' {:<20} | '.format('' )
                            
                    except Exception as e:
                        string += ' {:<20} | '.format('error')
            arbitrage_table[symbol]['gap'] = (arbitrage_table[symbol]['max']  / arbitrage_table[symbol]['min'])

            if  arbitrage_table[symbol]['gap'] > 1.02 :
                gap_symbols.append(symbol)
            dump(string)

        print(gap_symbols)

        for gap_symbol in gap_symbols:
            # if gap_symbol in ArbitrageFinder.EXCEPT_SYMBOLS:
            #     continue
            print(gap_symbol)
            pprint.pprint(arbitrage_table[gap_symbol])

    def retrieve_arbitrable_symbols(self):
        allSymbols = [symbol.replace(":USDT", "") for id in self.ids for symbol in self.tickers[id].keys()]
        uniqueSymbols = list(set(allSymbols))
        arbitrableSymbols = sorted([symbol for symbol in uniqueSymbols if allSymbols.count(symbol) > 1])
        return arbitrableSymbols

    def load_tickers(self):
        for id in self.ids:
            exchange = self.exchanges[id]
            self.tickers[id] = exchange.fetch_tickers()
            dump(green(id), 'loaded', green(str(len(self.tickers[id].keys()))), 'markets')

    def print_arbitrage_table_header(self):
        dump(green(' symbol               | ' + ''.join([' {:<20} | '.format(id) for id in self.ids])))
        dump(green(''.join(['----------------------+-' for x in range(0, len(self.ids) + 1)])))

    def is_perpetual_exchange(self, id):
        return  '_swap' in id

if __name__ == '__main__': 
    arbitrage_finder = ArbitrageFinder()
    arbitrage_finder.retrieve_gap_symbols()