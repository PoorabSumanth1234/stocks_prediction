import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import argparse # Used to read command-line arguments

load_dotenv()

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com"

def fetch_and_save_data(ticker):
    """
    Fetches 5 years of daily historical data for a given ticker and saves it to a CSV file.
    """
    if not API_KEY:
        print("Error: TWELVE_DATA_API_KEY not found in .env file.")
        return

    output_file = f"{ticker}_data.csv" # The filename is now based on the ticker
    end_date = datetime.now()
    start_date = end_date - relativedelta(years=5)

    params = {
        "symbol": ticker.upper(), # Use the ticker provided by the user
        "interval": "1day",
        "start_date": start_date.strftime('%Y-%m-%d'),
        "end_date": end_date.strftime('%Y-%m-%d'),
        "apikey": API_KEY,
        "outputsize": 5000
    } 

    print(f"Fetching data for {ticker} from {start_date.date()} to {end_date.date()}...")
    try:
        response = requests.get(f"{BASE_URL}/time_series", params=params)
        response.raise_for_status()
        data = response.json()

        if "values" not in data or len(data["values"]) == 0:
            print(f"Error: No data received. Response: {data}")
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
    # This section reads the ticker you provide in the terminal
    parser = argparse.ArgumentParser(description="Fetch historical stock data.")
    parser.add_argument("ticker", help="The stock ticker symbol to fetch (e.g., MSFT, GOOG).")
    args = parser.parse_args()
    
    fetch_and_save_data(args.ticker)