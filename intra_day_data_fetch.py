import os
import sys
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()

# --- Configuration ---
API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"

def fetch_and_save_intraday_data(ticker, interval):
    """
    Fetches recent intraday historical data for a given ticker and interval.
    NOTE: Free Twelve Data API has limitations on how far back you can go.
    """
    if not API_KEY:
        print("Error: TWELVE_DATA_API_KEY not found in .env file.")
        return

    output_file = f"{ticker}_{interval}_data.csv"
    
    # For intraday, we typically get the last month of data
    end_date = datetime.now()
    start_date = end_date - relativedelta(months=2) # Request 2 months to get as much as possible

    params = {
        "symbol": ticker,
        "interval": interval,
        "start_date": start_date.strftime('%Y-%m-%d %H:%M:%S'),
        "end_date": end_date.strftime('%Y-%m-%d %H:%M:%S'),
        "apikey": API_KEY,
        "outputsize": 5000 
    }

    print(f"Fetching {interval} data for {ticker}...")
    try:
        response = requests.get(f"{BASE_URL}/time_series", params=params)
        response.raise_for_status()
        data = response.json()

        if "values" not in data or len(data["values"]) == 0:
            print(f"Warning: No intraday data received for {ticker} at {interval} interval. This may be a limitation of the free API plan.")
            return

        df = pd.DataFrame(data['values'])
        df = df.iloc[::-1].reset_index(drop=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        
        df.to_csv(output_file)
        print(f"Successfully saved data to {output_file}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python intraday_data_fetcher.py <TICKER> <INTERVAL>")
        print("Example: python intraday_data_fetcher.py AAPL 1min")
        sys.exit(1)
    
    ticker_symbol = sys.argv[1].upper()
    interval_arg = sys.argv[2] # e.g., "1min", "5min"
    fetch_and_save_intraday_data(ticker_symbol, interval_arg)
