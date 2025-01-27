# main.py
import streamlit as st
from utils.data_fetcher import fetch_stock_data
from utils.indicators import calculate_technical_indicators
from utils.analysis import analyze_candlestick_patterns, calculate_sentiment_analysis
from utils.visualization import plot_predictions
from utils.report_generator import generate_pdf_report
from utils.initialize_client import initialize_openai_client

def main():
    st.title("Chartered Market Analyst Agent for Stock and Crypto")
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
                time.sleep(1)  # Simulate a delay for demonstration
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

                    st.subheader("Technical Indicators")
                    st.write(
                        f"**20-hour MA:** ${prediction['technical_indicators']['ma20']:.2f}"
                    )
                    st.write(
                        f"**50-hour MA:** ${prediction['technical_indicators']['ma50']:.2f}"
                    )
                    st.write(
                        f"**RSI:** {prediction['technical_indicators']['rsi']:.2f}"
                    )

                    st.subheader("Market Insight")
                    st.write(f"**Summary:** {prediction['market_insight']['summary']}")
                    st.write(
                        f"**Risk Level:** {prediction['market_insight']['risk_level']}"
                    )
                    st.write(
                        f"**Recommendation:** {prediction['market_insight']['recommendation']}"
                    )

                    # Clear session state for report files when analyzing a new stock or period
                    if "report_files" in st.session_state:
                        del st.session_state.report_files

                    # Analyze candlestick patterns using AI first
                    analysis = analyze_candlestick_patterns(client, stock_data, period)
                    st.subheader("Candlestick Pattern Analysis")
                    st.write(analysis)

                    # Plot predictions and get image paths
                    candlestick_img, rsi_img = plot_predictions(
                        stock_data, prediction, period
                    )

                    # Generate PDF report
                    pdf_report = generate_pdf_report(prediction, analysis)

                    # Store file paths in session state
                    st.session_state.report_files = {
                        "pdf_report": pdf_report,
                        "candlestick_img": candlestick_img,
                        "rsi_img": rsi_img,
                    }

                    # Create ZIP file with all reports
                    zip_filename = f"{ticker}_analysis_reports.zip"
                    with zipfile.ZipFile(zip_filename, "w") as zipf:
                        # Add PDF report
                        if st.session_state.report_files["pdf_report"]:
                            zipf.write(
                                st.session_state.report_files["pdf_report"],
                                os.path.basename(
                                    st.session_state.report_files["pdf_report"]
                                ),
                            )

                        # Add candlestick chart
                        if st.session_state.report_files["candlestick_img"]:
                            zipf.write(
                                st.session_state.report_files["candlestick_img"],
                                f"{ticker}_candlestick_chart.png",
                            )

                        # Add RSI chart
                        if st.session_state.report_files["rsi_img"]:
                            zipf.write(
                                st.session_state.report_files["rsi_img"],
                                f"{ticker}_rsi_chart.png",
                            )

                    # Single download button for ZIP file
                    st.subheader("Download All Reports")
                    with open(zip_filename, "rb") as f:
                        st.download_button(
                            label="📦 Download All Reports (ZIP)",
                            data=f,
                            file_name=zip_filename,
                            mime="application/zip",
                        )

                    if st.button("Analyze a Different Stock"):
                        # Clear session state to reset the app
                        st.session_state.clear()
                        st.rerun()  # Rerun the app to reset the UI
                else:
                    st.error(
                        f"Unable to analyze {ticker}. Please check the ticker symbol."
                    )


# Run the Streamlit app
if __name__ == "__main__":
    main()
