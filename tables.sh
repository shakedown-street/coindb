#!/bin/bash

sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib

echo "CREATE TABLE btc_tick(\
date_str VARCHAR(50) NOT NULL,\
open DECIMAL(20, 2),\
close DECIMAL(20, 2),\
high DECIMAL(20, 2),\
low DECIMAL(20, 2),\
volume DECIMAL(20, 2),\
market_cap DECIMAL(20, 2)\
);
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO coin_db;
" | sudo su postgres -c psql coin_db
