#!/usr/bin/env python3
import requests
import mysql.connector
from datetime import datetime

URL = 'https://api.porssisahko.net/v2/latest-prices.json'
conn = mysql.connector.connect(host='localhost', user='exampleuser',
password='change_this_strong_password', database='weather_db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS electric_prices (id INT
AUTO_INCREMENT PRIMARY KEY, area VARCHAR(20), price_cents FLOAT,
start_time DATETIME, end_time DATETIME)''')
response = requests.get(URL)
data = response.json()
prices = data.get('prices', [])
saved = 0
for row in prices:
    area = row['area']
    price = row['price']
    start_time = datetime.fromisoformat(row['startDate'].replace('Z', '+00:00')).replace(tzinfo=None)
    end_time = datetime.fromisoformat(row['endDate'].replace('Z', '+00:00')).replace(tzinfo=None)
    cursor.execute('INSERT INTO electric_prices (area, price_cents, start_time, end_time) VALUES (%s, %s, %s, %s)',
    (area, price, start_time, end_time))
    saved += 1
conn.commit()
cursor.close()
conn.close()
print(f'Tallennettu {saved} sähkön hintaa')

