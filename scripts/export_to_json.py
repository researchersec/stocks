import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('data/stocks_data.db')

tickers = ['TSLA', 'NVO', 'NVDA']

for ticker in tickers:
    # Query the data into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM stock_data WHERE ticker = '{ticker}'", conn)
    
    # Calculate additional statistics
    df['daily_change'] = df['close'].pct_change() * 100  # Daily percentage change
    df['moving_avg_20'] = df['close'].rolling(window=20).mean()  # 20-day moving average
    df['moving_avg_50'] = df['close'].rolling(window=50).mean()  # 50-day moving average
    
    # Convert the DataFrame to JSON and save it
    df.to_json(f'data/stocks_data_{ticker}.json', orient='records', date_format='iso')

# Close the connection
conn.close()
