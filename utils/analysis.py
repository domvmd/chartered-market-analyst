# utils/analysis.py
import pandas as pd
import numpy as np
import streamlit as st

def analyze_candlestick_patterns(client, stock_data, period):
    """Analyze candlestick patterns using OpenAI"""
    try:
        if stock_data is None or len(stock_data) < 50:
            return "Insufficient data for analysis"

        # Extract the latest 50 rows
        latest_50 = stock_data.iloc[-50:]

        # Convert to candlestick format
        candles = []
        for idx, row in latest_50.iterrows():
            candles.append({
                "date": idx.strftime("%Y-%m-%d"),  # Format date
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            })

        # Build description using the candles list
        description = (
            f"The stock data for the selected period ({period}) shows the following candlestick patterns:\n"
            f"Last 5 candlesticks as examples:\n"
        )

        # Add formatted candlestick details
        description += "\n".join(
            [f"{c['date']}: Open={c['open']:.2f}, High={c['high']:.2f}, Low={c['low']:.2f}, Close={c['close']:.2f}, Volume={c['volume']}"
             for c in candles[-5:]]  # Use the last 5 candles for context
        )

        # Add analysis instructions
        description += (
            "\n\nPlease analyze 5 significant candlestick patterns and provide insights considering: "
            "\n1. Pattern strength and confirmation"
            "\n2. Confluence with RSI/MA/Volume"
            "\n3. Recent price action context"
            "\nEach candlestick represents a specific time interval (e.g., 1 hour or 1 day). "            
        )

        # Send the description to OpenAI for analysis
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Chartered Market Technician (CMT) with 20 years experience. Analyze strictly the following rules:
                    
                    1. Pattern Analysis:
                    - Identify AT MOST 5 significant patterns in the whole trend
                    - For each pattern:
                        * Name & location (e.g. '3rd candlestick: Bullish Engulfing')
                        * Confidence level (High/Medium/Low)
                        * Key confirmation factors (volume, indicator alignment)
                        * Immediate price implications
                                           
                    2.Trading Plan:
                    -Clear entry/exit levels:
                    - For each pattern:
                        * Ideal Buy Zone ${X} - ${Y}
                        * Stop Loss: ${Z}
                        * Take profit: ${A} (short-term)
                    - Risk-reward ratio
                    
                    3. Price Predictions (technical-only)
                    - 4 months:
                    - 8 months:
                    - 12 months:
                    Format predictions with price ranges and confidence percentages
                                           
                    4. Professional Tone:
                    - Avoid speculation
                    - Highlight key support/resistance
                    - Mention any divergence patterns"""
                },
                {"role": "user", "content": description},
            ],
            temperature=0.3,
        )

        # Extract the analysis result
        analysis = response.choices[0].message.content.strip()
        return analysis
    except Exception as e:
        st.error(f"Error in candlestick pattern analysis: {str(e)}")
        return "Unable to analyze candlestick patterns."
