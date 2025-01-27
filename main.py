# main.py
import streamlit as st
from utils.data_fetcher import fetch_stock_data
from utils.indicators import calculate_technical_indicators
from utils.analysis import analyze_candlestick_patterns, calculate_sentiment_analysis
from utils.visualization import plot_predictions
from utils.report_generator import generate_pdf_report
from utils.initialize_client import initialize_openai_client

def main():
    st.title("Papa Dom's Stock/Crypto Price Analysis App")
    st.write("Analyze stocks from the US and other markets or Cryptocurrency.")

    # Input Deepseek API key
    deepseek_api_key = st.text_input(
        "Enter your Deepseek API key:",
        type="password",
        help="You can find your API key at https://platform.deepseek.com/account/api-keys",
    )

    # Initialize OpenAI client
    client = initialize_openai_client(deepseek_api_key)

    # Input ticker symbol
    ticker = st.text_input(
        "Enter a ticker compatible with Yahoo Finance (e.g., NVDA for Nvidia, BTC-USD for Bitcoin):",
        "AAPL",
    )

    # Time period selection
    period = st.selectbox(
        "Select the time period for analysis:",
        options=["1d", "5d", "1mo", "6mo", "1y", "5y"],
        index=4,  # Default to 1 year
    )

    # Button to analyze the stock
    if st.button("Analyze"):
        if not client:
            st.error("Please enter a valid Deepseek API key to proceed.")
        else:
            with st.spinner("Analyzing stock data..."):
                prediction, stock_data = predict_next_day(ticker, period)

                if prediction and stock_data is not None:
                    # Display results
                    st.subheader("Stock Analysis Results")
                    st.write(f"**Ticker:** {prediction['ticker']}")
                    st.write(f"**Current Price:** ${prediction['last_close']:.2f}")
                    st.write(
                        f"**Predicted Price:** ${prediction['predicted_price']:.2f}"
                    )
                    st.write(
                        f"**Predicted Change:** {((prediction['predicted_price'] / prediction['last_close']) - 1) * 100:.1f}%"
                    )
                    st.write(f"**Prediction Date:** {prediction['prediction_date']}")

                    # Analyze candlestick patterns using AI
                    analysis = analyze_candlestick_patterns(client, stock_data, period)
                    st.subheader("Candlestick Pattern Analysis")
                    st.write(analysis)

                    # Plot predictions
                    candlestick_img, rsi_img = plot_predictions(
                        stock_data, prediction, period
                    )

                    # Generate PDF report
                    pdf_report = generate_pdf_report(prediction, analysis)

                    # Download button for PDF report
                    with open(pdf_report, "rb") as f:
                        st.download_button(
                            label="📄 Download PDF Report",
                            data=f,
                            file_name=f"{ticker}_analysis_report.pdf",
                            mime="application/pdf",
                        )

if __name__ == "__main__":
    main()
