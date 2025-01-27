# utils/visualization.py
import matplotlib.pyplot as plt
import mplfinance as mpf
import tempfile
import streamlit as st

def plot_predictions(stock_data, prediction, period):
    """Create visualization of stock data and predictions using candlestick chart"""
    try:
        # Get data for the selected period
        if period == "1d":
            data = stock_data.tail(70)  # 24 hours for 1 day
        elif period == "5d":
            data = stock_data.tail(70)  # 24 hours * 5 days = 120 hours
        elif period == "1mo":
            data = stock_data.tail(70)
        elif period == "6mo":
            data = stock_data.tail(70)
        elif period == "1y":
            data = stock_data.tail(70)
        elif period == "5y":
            data = stock_data.tail(70)
        else:
            data = stock_data.tail(70)  # Default to 30 days

        # Create a candlestick chart
        mpf.plot(
            data,
            type="candle",
            style="yahoo",  # You can choose other styles like 'classic', 'yahoo', etc.
            title=f"{prediction['ticker']} Stock Analysis - {prediction['prediction_date']}",
            ylabel="Price ($)",  # Updated to $ for US stocks
            volume=True,  # Add volume subplot
            mav=(20, 50),  # Add 20-hour and 50-hour moving averages
            figsize=(14, 8),
            show_nontrading=False,
            returnfig=False,
        )

        # Display the plot in Streamlit
        st.pyplot(plt.gcf())

        # Save the candlestick chart
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            plt.savefig(tmpfile.name, bbox_inches="tight", dpi=300)
            candlestick_img = tmpfile.name

        # Create RSI plot with improved styling
        plt.figure(figsize=(14, 4))
        plt.plot(data.index, data["RSI"], label="RSI", color="purple", linewidth=2)

        # Add RSI zones with better visibility
        plt.axhline(
            y=70, color="red", linestyle="--", alpha=0.5, label="Overbought (70)"
        )
        plt.axhline(
            y=30, color="green", linestyle="--", alpha=0.5, label="Oversold (30)"
        )

        plt.fill_between(
            data.index,
            data["RSI"],
            70,
            where=(data["RSI"] >= 70),
            color="red",
            alpha=0.2,
        )
        plt.fill_between(
            data.index,
            data["RSI"],
            30,
            where=(data["RSI"] <= 30),
            color="green",
            alpha=0.2,
        )

        plt.title("RSI Indicator", fontsize=12, pad=20)
        plt.ylabel("RSI", fontsize=10)
        plt.xlabel("Date", fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tick_params(axis="x", rotation=45)

        # Move RSI legend to the right
        plt.legend(
            bbox_to_anchor=(1.05, 1),
            loc="upper left",
            borderaxespad=0.0,
            frameon=True,
            fontsize=10,
        )

        # Display the RSI plot in Streamlit
        st.pyplot(plt)

        # Save the RSI chart
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            plt.savefig(tmpfile.name, bbox_inches="tight", dpi=300)
            rsi_img = tmpfile.name

    except Exception as e:
        st.error(f"Error in plotting: {str(e)}")
        return None, None

    return candlestick_img, rsi_img
