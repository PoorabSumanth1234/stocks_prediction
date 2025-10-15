import subprocess
import sys
# Add all the stock tickers you want your app to be able to predict.
POPULAR_TICKERS = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "TSLA",
    "NVDA",
    "META",
    "TSLA",
    "RELI",
]

def run_command(command):
    """Runs a command in the terminal and checks for errors."""
    try:
        print(f"--- Running command: {' '.join(command)} ---")
        subprocess.run(command, check=True, text=True)
        print(f"--- Successfully completed: {' '.join(command)} ---\n")
    except subprocess.CalledProcessError as e:
        print(f"--- Error running command: {' '.join(command)} ---")
        print(f"Error: {e}")

def main():
    """
    Iterates through the list of popular tickers and runs the data fetching
    and model training scripts for each one.
    """
    python_executable = sys.executable  # Gets the path to the python in your venv

    for ticker in POPULAR_TICKERS:
        print(f"*** Starting process for {ticker} ***")

       
        fetch_command = [python_executable, "data_fetcher.py", ticker]
        run_command(fetch_command)
        
        train_command = [python_executable, "model_trainer.py", ticker]
        run_command(train_command)

        print(f"*** Finished process for {ticker} ***\n")

    print("All popular stocks have been pre-trained!")

if __name__ == "__main__":
    main()
    