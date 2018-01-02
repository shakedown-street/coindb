import datetime
import logging
import json
import requests
import psycopg2

# Requests data from https://api.coinmarketcap.com/v1/ticker/ to store in our own database.

logger = logging.getLogger("coindb")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("ticker.log")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

def get_raw_data():
    return requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/').json()[0]

tick_data = get_raw_data()
conn = psycopg2.connect("dbname='coin_db' user='coin_db' host='localhost' password='coin_db'")
logger.info("Connected to db")
cursor = conn.cursor()
QUERY = """
INSERT INTO coindb_tick (name, symbol, rank, price_usd, price_btc, volume_usd_24h,
    market_cap_usd, available_supply, max_supply, percent_change_1h,
    percent_change_24h, percent_change_7d, last_updated)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, to_timestamp(%s));
"""
data_extracted = (
    tick_data['name'], tick_data['symbol'], tick_data['rank'],
    tick_data['price_usd'], tick_data['price_btc'], tick_data['24h_volume_usd'],
    tick_data['market_cap_usd'], tick_data['available_supply'], tick_data['max_supply'],
    tick_data['percent_change_1h'], tick_data['percent_change_24h'], tick_data['percent_change_7d'],
    tick_data['last_updated'],)
cursor.execute(QUERY, data_extracted)
logger.info("Stored data in database")
