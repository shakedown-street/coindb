import datetime
import logging
import json
import requests
import psycopg2

# Parse the table at
# https://coinmarketcap.com/currencies/bitcoin/historical-data/
# to store in our own database

logger = logging.getLogger("coindb")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("historical.log")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# Request https://coinmarketcap.com/currencies/bitcoin/historical-data/

def get_raw_html():
    return requests.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/')

print(get_raw_html().text)

# Parse data into a python dict

# Insert data into postgres
conn = psycopg2.connect("dbname='coin_db' user='coin_db' host='localhost' password='coin_db'")
logger.info("Connected to db")
cursor = conn.cursor()
