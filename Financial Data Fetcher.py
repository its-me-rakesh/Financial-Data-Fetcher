# streamlit_app.py

import streamlit as st
import yfinance as yf
import pandas as pd
from io import BytesIO

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="Stock Data & Ratios App",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Stock Data & Financial Ratios Viewer")
st.markdown("Fetch historical price data & financial ratios from Yahoo Finance.")

# ------------------- SIDEBAR INPUTS -------------------
st.sidebar.header("Input Parameters")

stock_symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="RELIANCE.NS",
    help="Use .NS for NSE and .BO for BSE (e.g., INFY.NS, TCS.BO)"
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2024-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

fetch_button = st.sidebar.button("Fetch Data")

# ------------------- FETCH FUNCTION -------------------
def get_financial_ratios(ticker_obj):
    info = ticker_obj.info
    ratios_dict = {
        "Previous Close": info.get("previousClose"),
        "Open": info.get("open"),
        "Market Cap": info.get("marketCap"),
        "Trailing P/E": info.get("trailingPE"),
        "Forward P/E": info.get("forwardPE"),
        "PEG Ratio": info.get("pegRatio"),
        "Price to Book": info.get("priceToBook"),
        "Beta": info.get("beta"),
        "Dividend Yield": info.get("dividendYield"),
        "Return on Assets": info.get("returnOnAssets"),
        "Return on Equity": info.get("returnOnEquity"),
        "Profit Margins": info.get("profitMargins"),
        "Operating Margins": info.get("operatingMargins"),
        "Revenue Growth": info.get("revenueGrowth"),
        "Earnings Growth": info.get("earningsGrowth"),
        "Debt to Equity": info.get("debtToEquity")
    }
    return pd.DataFrame(list(ratios_dict.items()), columns=["Ratio", "Value"])

# ------------------- CSV DOWNLOAD FUNCTION -------------------
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

# ------------------- MAIN APP LOGIC -------------------
if fetch_button:
    if stock_symbol.strip() == "":
        st.error("Please enter a valid stock symbol.")
    else:
        try:
            st.subheader(f"📈 Historical Price Data for {stock_symbol}")
            stock = yf.Ticker(stock_symbol)
            price_data = stock.history(start=start_date, end=end_date)

            if price_data.empty:
                st.warning("No data found for the given symbol & date range.")
            else:
                st.dataframe(price_data)

                csv_price = convert_df_to_csv(price_data)
                st.download_button(
                    label="💾 Download Price Data (CSV)",
                    data=csv_price,
                    file_name=f"{stock_symbol}_prices_{start_date}_to_{end_date}.csv",
                    mime="text/csv"
                )

            # Financial Ratios
            st.markdown("---")
            st.subheader(f"📊 Financial Ratios for {stock_symbol}")
            ratios_df = get_financial_ratios(stock)
            st.dataframe(ratios_df)

            csv_ratios = convert_df_to_csv(ratios_df)
            st.download_button(
                label="💾 Download Financial Ratios (CSV)",
                data=csv_ratios,
                file_name=f"{stock_symbol}_financial_ratios.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"Error fetching data: {e}")

# ------------------- EXTRA SECTIONS -------------------
st.markdown("---")
st.subheader("📂 Additional Data Sections")

sections = [
    "Dividends",
    "Splits",
    "Recommendations",
    "Sustainability (ESG)",
    "Institutional Holders",
    "Mutual Fund Holders",
    "Major Holders",
    "Earnings",
    "Quarterly Earnings",
    "Financials (Annual)",
    "Quarterly Financials",
    "Balance Sheet (Annual)",
    "Quarterly Balance Sheet",
    "Cashflow (Annual)",
    "Quarterly Cashflow",
    "Analyst Price Targets",
    "Calendar Events",
    "Options Data"
]

selected_section = st.selectbox("Select a data section to view", sections)

def display_data(data):
    if data is None or (hasattr(data, 'empty') and data.empty):
        st.warning("No data available for this section.")
    else:
        st.dataframe(data)

if selected_section == "Dividends":
    display_data(stock.dividends)

elif selected_section == "Splits":
    display_data(stock.splits)

elif selected_section == "Recommendations":
    display_data(stock.recommendations)

elif selected_section == "Sustainability (ESG)":
    display_data(stock.sustainability)

elif selected_section == "Institutional Holders":
    display_data(stock.institutional_holders)

elif selected_section == "Mutual Fund Holders":
    display_data(stock.mutualfund_holders)

elif selected_section == "Major Holders":
    display_data(stock.major_holders)

elif selected_section == "Earnings":
    display_data(stock.earnings)

elif selected_section == "Quarterly Earnings":
    display_data(stock.quarterly_earnings)

elif selected_section == "Financials (Annual)":
    display_data(stock.financials)

elif selected_section == "Quarterly Financials":
    display_data(stock.quarterly_financials)

elif selected_section == "Balance Sheet (Annual)":
    display_data(stock.balance_sheet)

elif selected_section == "Quarterly Balance Sheet":
    display_data(stock.quarterly_balance_sheet)

elif selected_section == "Cashflow (Annual)":
    display_data(stock.cashflow)

elif selected_section == "Quarterly Cashflow":
    display_data(stock.quarterly_cashflow)

elif selected_section == "Analyst Price Targets":
    try:
        display_data(stock.analyst_price_targets)
    except:
        st.warning("Analyst price targets not available.")

elif selected_section == "Calendar Events":
    display_data(stock.calendar)

elif selected_section == "Options Data":
    expiries = stock.options
    if expiries:
        expiry = st.selectbox("Select Expiry Date", expiries)
        chain = stock.option_chain(expiry)
        st.markdown("**Calls**")
        display_data(chain.calls)
        st.markdown("**Puts**")
        display_data(chain.puts)
    else:
        st.warning("No options data available.")



# ------------------- FOOTER -------------------
st.markdown("---")
st.caption("Developed by Rakesh Chourasia")



