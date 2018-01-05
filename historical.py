import datetime
import logging
import json
import requests
import psycopg2
import pprint
from bs4 import BeautifulSoup

# Parse the table at
# https://coinmarketcap.com/currencies/bitcoin/historical-data/
# to store in our own database

logger = logging.getLogger("coindb")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("historical.log")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

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
print(extracted_data)

# Insert data into postgres
conn = psycopg2.connect("dbname='coin_db' user='coin_db' host='localhost' password='coin_db'")
logger.info("Connected to db")
cursor = conn.cursor()
