import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.models import save_model
import os
import argparse
import joblib
 
# --- Configuration ---
# Number of previous days' prices to use to predict the next day
LOOK_BACK = 60 
def load_and_preprocess_data(data_file):
    """
    Loads data from the specified CSV file, selects the 'close' price, 
    and scales it for the model.
    """
    if not os.path.exists(data_file):
        print(f"Error: Data file {data_file} not found. Please run data_fetcher.py for this ticker first.")
        return None, None, None

    df = pd.read_csv(data_file, index_col='datetime', parse_dates=True)
    data = df.filter(['close'])
    dataset = data.values
    
    # Scale the data to be between 0 and 1 for optimal model performance
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    
    return dataset, scaled_data, scaler

def create_sequences(dataset, look_back=LOOK_BACK):
    """
    Creates sequences of data for training the LSTM. For each sequence,
    it takes 'look_back' number of data points as input (X) and the next
    data point as the output to be predicted (y).
    """
    X, y = [], []
    for i in range(len(dataset) - look_back):
        X.append(dataset[i:(i + look_back), 0])
        y.append(dataset[i + look_back, 0])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    """
    Builds the LSTM (RNN) model architecture.
    """
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def train_model(ticker):
    """
    Main function to orchestrate the loading, preprocessing, building, 
    and training of the model for a specific ticker.
    """
    data_file = f"{ticker}_data.csv"
    
    # 1. Load and prepare the data
    full_dataset, scaled_data, scaler = load_and_preprocess_data(data_file)
    if full_dataset is None:
        return

    # 2. Create the training sequences
    X, y = create_sequences(scaled_data)
    
    # Reshape input to be [samples, time steps, features] as required for LSTM layers
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    
    # Split the data into training and testing sets (80% for training, 20% for testing)
    training_data_len = int(np.ceil(len(X) * .8))
    X_train, X_test = X[:training_data_len], X[training_data_len:]
    y_train, y_test = y[:training_data_len], y[training_data_len:]

    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples for {ticker}.")

    # 3. Build the LSTM model
    model = build_lstm_model((X_train.shape[1], 1))
    
    # 4. Train the model
    print(f"Training model for {ticker}...")
    model.fit(X_train, y_train, batch_size=32, epochs=25)

    # 5. Evaluate the model on the test data (optional, but good practice)
    print(f"Test Loss: {model.evaluate(X_test, y_test)}")

    # 6. Save the trained model and the scaler object for later use in prediction
    model.save(f'{ticker}_predictor_model.h5')
    joblib.dump(scaler, f'{ticker}_scaler.gz')
    
    print(f"Model and scaler for {ticker} saved successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train an LSTM model for a specific stock.")
    parser.add_argument("ticker", help="The stock ticker symbol to train on (e.g., MSFT, GOOG).")
    args = parser.parse_args()
    
    train_model(args.ticker)