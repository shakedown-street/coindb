#!/bin/bash

sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib

echo "CREATE DATABASE coin_db;\
CREATE USER coin_db WITH PASSWORD 'coin_db';\
GRANT ALL PRIVILEGES ON DATABASE coin_db TO coin_db;" | sudo su postgres -c psql
