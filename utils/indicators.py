# utils/indicators.py
import pandas as pd
import numpy as np
import streamlit as st

def calculate_technical_indicators(df):
    """Calculate technical indicators"""
    try:
        df["Close"] = pd.to_numeric(df["Close"])
        
        # For intraday data (high frequency)
        if pd.infer_freq(df.index) in ['5T', '15T', '60T']:  # 5min, 15min, 1hr
            df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
            df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
        # For daily data
        else:
            df["MA20"] = df["Close"].rolling(window=20).mean()
            df["MA50"] = df["Close"].rolling(window=50).mean()

        # RSI calculation
        delta = df["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df["RSI"] = 100 - (100 / (1 + rs))
        
        return df
    except Exception as e:
        st.error(f"Indicator calculation failed: {e}")
        return df
