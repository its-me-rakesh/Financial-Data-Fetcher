import streamlit as st
import yfinance as yf
import pandas as pd
from io import BytesIO
from datetime import date

# Clear cache every time page reloads
st.cache_data.clear()
st.cache_resource.clear()

st.set_page_config(page_title="Yahoo Finance Data Fetcher", layout="wide")

# ----------------------
# Helper function to display & download data
# ----------------------
def display_data(df, label="Data"):
    if df is None:
        st.warning(f"No data available for {label}.")
        return
    
    if isinstance(df, pd.Series):
        df = df.to_frame()
    elif not isinstance(df, pd.DataFrame):
        try:
            df = pd.DataFrame(df)
        except Exception:
            st.warning(f"Could not convert {label} to DataFrame.")
            return

    if df.empty:
        st.warning(f"No data available for {label}.")
    else:
        st.dataframe(df, use_container_width=True)
        buffer = BytesIO()
        df.to_csv(buffer, index=True)
        st.download_button(
            label=f"Download {label} as CSV",
            data=buffer.getvalue(),
            file_name=f"{label.replace(' ', '_')}.csv",
            mime="text/csv"
        )

# ----------------------
# App Title
# ----------------------
st.title("📊 Yahoo Finance Data Fetcher")

# ----------------------
# User Inputs
# ----------------------
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    ticker_symbol = st.text_input("Enter NSE/BSE Symbol (e.g., RELIANCE.NS, TCS.BO)", value="")
with col2:
    start_date = st.date_input("Start Date", value=pd.to_datetime(""))
with col3:
    end_date = st.date_input("End Date", value=pd.to_datetime("today"))

# ----------------------
# Fetch Data on Button Click
# ----------------------
if st.button("Fetch Data"):
    if ticker_symbol:
        try:
            stock = yf.Ticker(ticker_symbol)

            tabs = st.tabs([
                "📈 Price History", "💰 Financials", "📄 Balance Sheet", "💵 Cash Flow",
                "🏦 Dividends", "🔄 Splits", "📊 Financial Ratios", "ℹ️ Company Info",
                "📆 Earnings", "🌱 Sustainability", "👥 Holders", "📜 Options"
            ])

            with tabs[0]:
                st.subheader("📈 Historical Price Data")
                display_data(stock.history(start=start_date, end=end_date), "Historical Price Data")

            with tabs[1]:
                st.subheader("💰 Financials")
                display_data(stock.financials, "Annual Financials")

            with tabs[2]:
                st.subheader("📄 Balance Sheet")
                display_data(stock.balance_sheet, "Annual Balance Sheet")

            with tabs[3]:
                st.subheader("💵 Cash Flow")
                display_data(stock.cashflow, "Annual Cash Flow")

            with tabs[4]:
                st.subheader("🏦 Dividends")
                display_data(stock.dividends, "Dividends")

            with tabs[5]:
                st.subheader("🔄 Stock Splits")
                display_data(stock.splits, "Stock Splits")

            with tabs[6]:
                st.subheader("📊 Key Financial Ratios")
                ratios = {
                    "P/E Ratio": stock.info.get("trailingPE"),
                    "Forward P/E": stock.info.get("forwardPE"),
                    "PEG Ratio": stock.info.get("pegRatio"),
                    "Price to Sales (P/S)": stock.info.get("priceToSalesTrailing12Months"),
                    "Price to Book (P/B)": stock.info.get("priceToBook"),
                    "Enterprise Value": stock.info.get("enterpriseValue"),
                    "EV/EBITDA": stock.info.get("enterpriseToEbitda"),
                    "EV/Revenue": stock.info.get("enterpriseToRevenue"),
                    "Debt to Equity": stock.info.get("debtToEquity"),
                    "Return on Equity (ROE)": stock.info.get("returnOnEquity"),
                    "Return on Assets (ROA)": stock.info.get("returnOnAssets"),
                    "Current Ratio": stock.info.get("currentRatio"),
                    "Quick Ratio": stock.info.get("quickRatio"),
                    "Gross Margins": stock.info.get("grossMargins"),
                    "Operating Margins": stock.info.get("operatingMargins"),
                    "Profit Margins": stock.info.get("profitMargins"),
                }
                df_ratios = pd.DataFrame(list(ratios.items()), columns=["Ratio", "Value"])
                display_data(df_ratios, "Key Financial Ratios")

            with tabs[7]:
                st.subheader("ℹ️ Company Profile")
                if stock.info:
                    df_info = pd.DataFrame(stock.info.items(), columns=["Attribute", "Value"])
                    display_data(df_info, "Company Info")
                else:
                    st.warning("No company information available.")

            with tabs[8]:
                st.subheader("📆 Quarterly & Yearly Earnings")
                st.markdown("**Quarterly Earnings**")
                display_data(stock.quarterly_earnings, "Quarterly Earnings")
                st.markdown("**Yearly Earnings**")
                display_data(stock.earnings, "Annual Earnings")

            with tabs[9]:
                st.subheader("🌱 Sustainability")
                display_data(stock.sustainability, "Sustainability")

            with tabs[10]:
                st.subheader("👥 Holders")
                try:
                    st.markdown("**Institutional Holders**")
                    display_data(stock.institutional_holders, "Institutional Holders")

                    st.markdown("**Mutual Fund Holders**")
                    display_data(stock.mutualfund_holders, "Mutual Fund Holders")

                    st.markdown("**Major Holders Breakdown**")
                    display_data(stock.major_holders, "Major Holders")
                except Exception as e:
                    st.error(f"Error fetching holders data: {e}")

            with tabs[11]:
                st.subheader("📜 Options Data")
                display_data(stock.options, "Available Options Expiry Dates")

        except Exception as e:
            st.error(f"Error fetching data: {e}")


