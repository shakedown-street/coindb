import datetime
import logging
import json
import requests
import psycopg2
import decimal
from bs4 import BeautifulSoup

# Parse the table at
# https://coinmarketcap.com/currencies/bitcoin/historical-data/
# to store in our own database

logger = logging.getLogger("coindb")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("historical.log")
logger.setLevel(logging.ERROR)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# Request https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20180105

def get_raw_html():
    return requests.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20180105").text

# Parse data into a python dict
soup = BeautifulSoup(get_raw_html(), "html.parser")

extracted_data = []
for table_row in soup.find("tbody").find_all("tr"):
    extracted_row = []
    for table_data in table_row.find_all("td"):
        extracted_row.append(table_data.get_text())
    extracted_data.append(extracted_row)
logger.info("Parsed table data")

# Insert data into postgres

def convert_to_decimal(val):
    try:
        return decimal.Decimal(val)
    except decimal.InvalidOperation:
        return None

conn = psycopg2.connect("dbname='coin_db' user='coin_db' host='localhost' password='coin_db'")
logger.info("Connected to db")
cursor = conn.cursor()
for row in extracted_data:
    DELETE_QUERY = """
    DELETE FROM btc_tick
    WHERE *;
    """
    QUERY = """
    INSERT INTO btc_tick(
        date_str, open, high, low, close, volume, market_cap)
    VALUES(%s, %s, %s, %s, %s, %s, %s)
    """
    date_str = row[0]
    open = convert_to_decimal(row[1])
    high = convert_to_decimal(row[2])
    low = convert_to_decimal(row[3])
    close = convert_to_decimal(row[4])
    volume = convert_to_decimal(row[5].replace(',', ''))
    market_cap = convert_to_decimal(row[6].replace(',', ''))
    updated_row = (date_str, open, high, low, close, volume, market_cap,)
    cursor.execute(DELETE QUERY, {})
    cursor.execute(QUERY, updated_row)
    logger.info("Data stored in database")

conn.commit()
cursor.close()
conn.close()
