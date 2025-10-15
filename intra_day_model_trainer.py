import sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import save_model
import os
import joblib

# --- Configuration ---
LOOK_BACK = 60 # Use the last 60 minutes/intervals to predict the next one

def load_and_preprocess_data(data_file):
    if not os.path.exists(data_file):
        print(f"Error: Data file {data_file} not found. Please run the intraday_data_fetcher.py first.")
        return None, None, None

    df = pd.read_csv(data_file, index_col='datetime', parse_dates=True)
    data = df.filter(['close'])
    dataset = data.values
    
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    
    return dataset, scaled_data, scaler

def create_sequences(dataset, look_back=LOOK_BACK):
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0])
        y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_intraday_model(ticker, interval):
    data_file = f"{ticker}_{interval}_data.csv"
    
    full_dataset, scaled_data, scaler = load_and_preprocess_data(data_file)
    if full_dataset is None: return

    X, y = create_sequences(scaled_data)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    print(f"Training on {len(X)} samples for {ticker} ({interval}).")

    model = build_lstm_model((X.shape[1], 1))
    model.fit(X, y, batch_size=32, epochs=25)

    model_path = f'{ticker}_{interval}_predictor_model.h5'
    scaler_path = f'{ticker}_{interval}_scaler.gz'
    
    model.save(model_path)
    joblib.dump(scaler, scaler_path)

    print(f"Intraday model for {ticker} ({interval}) saved successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python intraday_model_trainer.py <TICKER> <INTERVAL>")
        print("Example: python intraday_model_trainer.py AAPL 1min")
        sys.exit(1)

    ticker_symbol = sys.argv[1].upper()
    interval_arg = sys.argv[2]
    train_intraday_model(ticker_symbol, interval_arg)