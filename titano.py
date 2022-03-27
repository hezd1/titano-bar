#!/usr/bin/env python3

import configparser
import sys
import requests
from decimal import Decimal
from os.path import expanduser

config = configparser.ConfigParser()

# File must be opened with utf-8 explicitly
with open(expanduser('~/.config/polybar/titano-bar/titano-config'), 'r', encoding='utf-8') as f:
    config.read_file(f)

# Everything except the general section
currencies = [x for x in config.sections() if x != 'general']
base_currency = config['general']['base_currency']
params = {'convert': base_currency}


for currency in currencies:
    try:
        icon = config[currency]['icon']
        json = requests.get(f'https://api.coingecko.com/api/v3/coins/{currency}').json()["market_data"]
        local_price = round(Decimal(json["current_price"][f'{base_currency.lower()}']), 4)        
        
        # remove decimals if decimals contain four zeros
        if str(local_price).split('.')[1] == "0000":
            local_price = int(local_price)
            print('local_price_int:',local)
            
        # remove decimals if currency is wbnb.
        if 'wbnb' in str(currency):
            local_price = round(Decimal(json["current_price"][f'{base_currency.lower()}']), 0)
            
        # remove decimals if currency is ethereum.
        if 'ethereum' in str(currency):
            local_price = round(Decimal(json["current_price"][f'{base_currency.lower()}']), 0)            
            
        # Set 24h % change to two decimals.
        change_24 = round(float(json['price_change_percentage_24h']), 2)
        
        display_opt = config['general']['display']
        if display_opt == 'both' or display_opt == None:
            sys.stdout.write(f'{icon}${local_price}|{change_24:+}%')
        elif display_opt == 'small':
            sys.stdout.write(f'{icon} ')
            sys.stdout.write(f'{local_price}')
            sys.stdout.write(f' | ')
            if change_24 > 0:
                # arrow up
                sys.stdout.write('')
            elif change_24 == 0:
                # straight line
                sys.stdout.write('')
            else:
                # arrow down
                sys.stdout.write('')
            sys.stdout.write(f'{change_24: }%')
        elif display_opt == 'percentage':
            sys.stdout.write(f'{icon} {change_24:+}%')
        elif display_opt == 'price':
            sys.stdout.write(f'{icon} {local_price}')
        if currency != currencies[-1]:
            sys.stdout.write('  ')
    except requests.exceptions.ConnectionError as e:
        sys.stdout.write('not connected')
        break