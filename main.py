import os
import requests
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# --- Initial Setup ---
load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Configuration ---
TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY")
TWELVE_DATA_BASE_URL = "https://api.twelvedata.com"

# --- Machine Learning Model Prediction Logic (No changes here) ---
def get_prediction(ticker: str, target_date_str: str = None):
    model_path = f'{ticker}_predictor_model.h5'
    scaler_path = f'{ticker}_scaler.gz'

    if not os.path.exists(model_path):
        return {"error": f"No pre-trained model found for {ticker}."}
    try:
        model = load_model(model_path)
        scaler = joblib.load(scaler_path)
        params = {"symbol": ticker.upper(), "interval": "1day", "outputsize": 60, "apikey": TWELVE_DATA_API_KEY}
        response = requests.get(f"{TWELVE_DATA_BASE_URL}/time_series", params=params)
        response.raise_for_status()
        data = response.json()
        if "values" not in data or len(data["values"]) < 60:
            return {"error": "Not enough recent data for prediction."}
        recent_prices = [float(item['close']) for item in data['values']][::-1]
        input_data = scaler.transform(np.array(recent_prices).reshape(-1, 1))
        if target_date_str:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
            today = date.today()
            if target_date <= today: return {"error": "Please select a future date."}
            days_to_predict = (target_date - today).days
            if days_to_predict > 365: return {"error": "Date is too far (max 1 year)."}
            num_predictions = days_to_predict
        else:
            num_predictions = 365
        current_batch = input_data.reshape(1, 60, 1)
        predictions_scaled = []
        for i in range(num_predictions):
            next_pred_scaled = model.predict(current_batch, verbose=0)[0]
            predictions_scaled.append(next_pred_scaled)
            current_batch = np.append(current_batch[:, 1:, :], [[next_pred_scaled]], axis=1)
        predictions = scaler.inverse_transform(predictions_scaled)
        if target_date_str:
            return {"date_prediction": float(predictions[-1][0])}
        return {
            "1-day": float(predictions[0][0]), "1-week": float(predictions[6][0]),
            "1-month": float(predictions[29][0]), "1-year": float(predictions[364][0]),
            "note": "Long-term predictions are speculative and based on historical data patterns."
        }
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}

# --- Main API Endpoint (OPTIMIZED) ---
@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str, interval: str = "1day", target_date: str = None, include_prediction: bool = True):
    if not TWELVE_DATA_API_KEY:
        raise HTTPException(status_code=500, detail="API key is not configured.")
    try:
        if target_date:
            prediction_data = get_prediction(ticker, target_date_str=target_date)
            return {"prediction": prediction_data}

        end_date = datetime.now()
        chart_params = { "symbol": ticker.upper(), "interval": interval, "apikey": TWELVE_DATA_API_KEY }
        if interval in ["1month", "1year", "5years"]:
            delta = {"1month": relativedelta(months=1), "1year": relativedelta(years=1), "5years": relativedelta(years=5)}
            chart_params["interval"] = "1week" if interval == "5years" else "1day"
            chart_params["start_date"] = (end_date - delta[interval]).strftime('%Y-%m-%d')
            chart_params["end_date"] = end_date.strftime('%Y-%m-%d')
        else:
            chart_params["outputsize"] = 100
        series_response = requests.get(f"{TWELVE_DATA_BASE_URL}/time_series", params=chart_params)
        series_response.raise_for_status()
        series_data = series_response.json()
        
        quote_params = {"symbol": ticker.upper(), "apikey": TWELVE_DATA_API_KEY}
        quote_response = requests.get(f"{TWELVE_DATA_BASE_URL}/quote", params=quote_params)
        quote_response.raise_for_status()
        quote_data = quote_response.json()
        
        # --- OPTIMIZATION: Only run prediction if requested ---
        prediction_data = get_prediction(ticker) if include_prediction else None
        
        analysis = {
            "currentPrice": float(quote_data.get('close', 0)), "change": float(quote_data.get('change', 0)),
            "percentChange": float(quote_data.get('percent_change', 0)), "dayHigh": float(quote_data.get('high', 0)),
            "dayLow": float(quote_data.get('low', 0)), "openPrice": float(quote_data.get('open', 0)),
            "prevClose": float(quote_data.get('previous_close', 0)),
            "explanation": f"{ticker.upper()} is currently trading at ${float(quote_data.get('close', 0)):.2f}, a change of {float(quote_data.get('change', 0)):.2f} ({float(quote_data.get('percent_change', 0)):.2f}%) for the day..."
        }
        
        chart_data = []
        if "values" in series_data:
            chart_data = [{"x": item['datetime'], "y": [float(item['open']), float(item['high']), float(item['low']), float(item['close'])]} for item in series_data['values']][::-1]

        return { "analysis": analysis, "chartData": chart_data, "prediction": prediction_data }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data from Twelve Data: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
