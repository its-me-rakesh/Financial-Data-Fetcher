import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Yahoo Finance Data Fetcher", layout="wide")

# ----------------------
# Helper function to display data
# ----------------------
def display_data(df):
    if isinstance(df, pd.Series):
        df = df.to_frame()
    if df.empty:
        st.warning("No data available for this section.")
    else:
        st.dataframe(df)

# ----------------------
# App Title
# ----------------------
st.title("📊 Yahoo Finance Data Fetcher")

# ----------------------
# User Inputs
# ----------------------
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    ticker_symbol = st.text_input("Enter NSE/BSE Symbol (e.g., RELIANCE.NS, TCS.BO)", value="RELIANCE.NS")
with col2:
    start_date = st.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
with col3:
    end_date = st.date_input("End Date", value=pd.to_datetime("today"))

if st.button("Fetch Data"):
    if ticker_symbol:
        stock = yf.Ticker(ticker_symbol)

        # ----------------------
        # Tabs for different data sections
        # ----------------------
        tabs = st.tabs([
            "📈 Price History", "💰 Financials", "📄 Balance Sheet", "💵 Cash Flow",
            "🏦 Dividends", "🔄 Splits", "📊 Financial Ratios", "ℹ️ Company Info",
            "📆 Earnings", "🌱 Sustainability", "👥 Holders", "📜 Options"
        ])

        # Price History
        with tabs[0]:
            st.subheader("📈 Historical Price Data")
            hist = stock.history(start=start_date, end=end_date)
            display_data(hist)

        # Financials
        with tabs[1]:
            st.subheader("💰 Financials")
            display_data(stock.financials)

        # Balance Sheet
        with tabs[2]:
            st.subheader("📄 Balance Sheet")
            display_data(stock.balance_sheet)

        # Cash Flow
        with tabs[3]:
            st.subheader("💵 Cash Flow")
            display_data(stock.cashflow)

        # Dividends
        with tabs[4]:
            st.subheader("🏦 Dividends")
            display_data(stock.dividends)

        # Splits
        with tabs[5]:
            st.subheader("🔄 Stock Splits")
            display_data(stock.splits)

        # Financial Ratios
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
            display_data(df_ratios)

        # Company Info
        with tabs[7]:
            st.subheader("ℹ️ Company Profile")
            info = stock.info
            if info:
                df_info = pd.DataFrame(info.items(), columns=["Attribute", "Value"])
                display_data(df_info)
            else:
                st.warning("No company information available.")

        # Earnings
        with tabs[8]:
            st.subheader("📆 Quarterly & Yearly Earnings")
            st.markdown("**Quarterly Earnings**")
            display_data(stock.quarterly_earnings)
            st.markdown("**Yearly Earnings**")
            display_data(stock.earnings)

        # Sustainability
        with tabs[9]:
            st.subheader("🌱 Sustainability")
            display_data(stock.sustainability)

        # Holders
        with tabs[10]:
            st.subheader("👥 Major Holders")
            st.markdown("**Institutional Holders**")
            display_data(stock.institutional_holders)
            st.markdown("**Mutual Fund Holders**")
            display_data(stock.mutualfund_holders)
            st.markdown("**Major Holders Breakdown**")
            display_data(stock.major_holders)

        # Options
        with tabs[11]:
            st.subheader("📜 Options Expiration Dates & Chain")
            try:
                options_dates = stock.options
                st.write("Available Expiration Dates:", options_dates)
                if options_dates:
                    first_date = options_dates[0]
                    st.write(f"Options Chain for {first_date}:")
                    display_data(stock.option_chain(first_date).calls)
                    display_data(stock.option_chain(first_date).puts)
            except Exception as e:
                st.error(f"Error fetching options data: {e}")

    else:
        st.error("Please enter a stock symbol.")
