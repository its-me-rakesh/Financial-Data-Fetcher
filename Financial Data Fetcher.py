import streamlit as st
import pandas as pd
import yfinance as yf
from io import BytesIO

# Function to display and download data
def display_data(df, title):
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        st.warning(f"No data available for {title}")
        return
    st.subheader(title)
    st.dataframe(df)
    buffer = BytesIO()
    df.to_csv(buffer, index=True)
    st.download_button(
        label=f"Download {title} CSV",
        data=buffer.getvalue(),
        file_name=f"{title.replace(' ', '_')}.csv",
        mime="text/csv"
    )

st.title("📊 Yahoo Finance Data Fetcher")

# User inputs
ticker_symbol = st.text_input("Enter NSE/BSE Stock Symbol", value="RELIANCE.NS")
start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
end_date = st.date_input("End Date", value=pd.to_datetime("2024-08-01"))

if st.button("Fetch Data"):
    try:
        stock = yf.Ticker(ticker_symbol)

        # Historical data
        hist_data = stock.history(start=start_date, end=end_date)
        display_data(hist_data, "Historical Data")

        # Financial statements
        display_data(stock.financials, "Annual Financials")
        display_data(stock.quarterly_financials, "Quarterly Financials")

        # Balance sheets
        display_data(stock.balance_sheet, "Annual Balance Sheet")
        display_data(stock.quarterly_balance_sheet, "Quarterly Balance Sheet")

        # Cashflow
        display_data(stock.cashflow, "Annual Cashflow")
        display_data(stock.quarterly_cashflow, "Quarterly Cashflow")

        # Earnings
        display_data(stock.earnings, "Annual Earnings")
        display_data(stock.quarterly_earnings, "Quarterly Earnings")

        # Dividends & Splits
        display_data(stock.dividends, "Dividends")
        display_data(stock.splits, "Stock Splits")

        # Analyst recommendations
        display_data(stock.recommendations, "Analyst Recommendations")

        # Institutional holders
        display_data(stock.institutional_holders, "Institutional Holders")
        display_data(stock.mutualfund_holders, "Mutual Fund Holders")

        # Major holders (ownership data)
        display_data(stock.major_holders, "Major Holders")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
