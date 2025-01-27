# utils/data_fetcher.py
import yfinance as yf
import pandas as pd
import streamlit as st

def get_interval_and_period(period):
    """Dynamically determine interval based on requested period"""
    interval_rules = {
        "1d": ("5m", "7d"),    # 5m interval (covers 7 days to ensure 50+ points for 1d)
        "5d": ("15m", "1mo"),  # 15m interval (covers 1 month)
        "1mo": ("60m", "3mo"), # 1h interval
        "6mo": ("1d", "6mo"),  # Daily data
        "1y": ("1d", "1y"),
        "5y": ("1d", "5y")
    }
    return interval_rules.get(period, ("1d", "1y"))  # Default fallback

def fetch_stock_data(ticker, period="1y"):
    """Fetch historical stock data with adaptive intervals"""
    try:
        # Get interval dynamically from period
        interval, adjusted_period = get_interval_and_period(period)        
        stock = yf.Ticker(ticker)
        df = stock.history(period=adjusted_period, interval=interval)  # Uses dynamic interval
        
        # Filter to only keep data within the original requested period
        if period == "1d":
            df = df.last("1D")
        elif period == "5d":
            df = df.last("5D")
        # ... similar logic for other periods
        
        # Final check for sufficient data
        if len(df) < 50:
            st.warning(f"Insufficient data ({len(df)} points). Try a longer period.")
            return None
            
        df.index = pd.to_datetime(df.index)
        return df
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None
