import yfinance as yf
import pandas as pd
from datetime import datetime

# Function to fetch stock data
def fetch_stock_data(ticker, start_date, end_date):
    stock = yf.download(ticker, start=start_date, end=end_date)
    stock.to_csv(f'data/{ticker}_stock_data.csv')

# Example fetching Tesla data
fetch_stock_data('TSLA', '2023-01-01', datetime.now().strftime('%Y-%m-%d'))
