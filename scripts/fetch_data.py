import yfinance as yf
import sqlite3
from datetime import datetime

# List of stock tickers to track
tickers = ['TSLA', 'NVO', 'NVDA']

# Connect to SQLite database (or create it)
conn = sqlite3.connect('data/stocks_data.db')
cursor = conn.cursor()

# Create a table for stock data if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_data (
    ticker TEXT,
    date TEXT,
    close REAL,
    sentiment REAL,
    PRIMARY KEY (ticker, date)
)
''')

# Function to fetch stock data and insert into SQLite
def fetch_and_store_stock_data(ticker):
    # Get the latest date available in the database for this ticker
    cursor.execute('''
    SELECT MAX(date) FROM stock_data WHERE ticker = ?
    ''', (ticker,))
    last_date = cursor.fetchone()[0]

    # If the last date is None, start from a reasonable default date
    if last_date is None:
        last_date = '2023-01-01'

    # Fetch stock data from last_date to today
    stock = yf.download(ticker, start=last_date, end=datetime.now().strftime('%Y-%m-%d'))
    
    # Insert new data into the database
    for index, row in stock.iterrows():
        # Check if data for this date already exists
        cursor.execute('''
        SELECT 1 FROM stock_data WHERE ticker = ? AND date = ?
        ''', (ticker, index.strftime('%Y-%m-%d')))
        if cursor.fetchone() is None:
            cursor.execute('''
            INSERT INTO stock_data (ticker, date, close, sentiment) VALUES (?, ?, ?, ?)
            ''', (ticker, index.strftime('%Y-%m-%d'), row['Close'], None))  # Add sentiment later

# Fetch and store data for each ticker
for ticker in tickers:
    fetch_and_store_stock_data(ticker)

# Commit and close the database connection
conn.commit()
conn.close()
