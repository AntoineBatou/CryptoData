CREATE_TABLE = '''CREATE TABLE crypto_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,                -- "Bitcoin", "Ethereum"  
    price REAL,               -- Prix actuel
    market_cap INTEGER,       -- Market cap
    volume INTEGER,           -- Volume 24h
    time TIMESTAMP
);'''

ADD_DATA = '''INSERT INTO crypto_data (name, price, market_cap, volume, time) VALUES (?, ?, ?, ?, ?);'''

SHOW_DATA = '''SELECT * FROM crypto_data;'''

SELECT_PREC_DATA = '''
SELECT *
FROM crypto_data
WHERE name = ?
ORDER BY time DESC
LIMIT 2;'''

SELECT_PREC_PRICE = '''
SELECT price
FROM crypto_data
WHERE name = ?
ORDER BY time DESC
LIMIT 2;
'''

SELECT_CAP_T0 = '''
SELECT market_cap
FROM crypto_data
WHERE name = ?
ORDER BY time DESC
LIMIT 2;
'''

SELECT_2LAST_TIME = '''
SELECT time
FROM crypto_data
WHERE name = ?
ORDER BY time DESC
LIMIT 2;
'''