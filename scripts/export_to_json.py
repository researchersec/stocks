import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect('data/stocks_data.db')

tickers = ['TSLA', 'NVO', 'NVDA']

for ticker in tickers:
    # Query the data into a DataFrame
    df = pd.read_sql_query(f"SELECT * FROM stock_data WHERE ticker = '{ticker}'", conn)

    # Convert the DataFrame to JSON and save it
    df.to_json(f'data/stocks_data_{ticker}.json', orient='records', date_format='iso')

# Close the connection
conn.close()
