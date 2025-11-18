import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import ta
import yfinance as yf

from pages.utils.plotly_figure import (
    plotly_table,
    close_chart,
    candlestick,
    Moving_average,
    RSI,
    MACD,
)

# =========================
# Page config & title
# =========================
st.set_page_config(
    page_title="Stock Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.markdown(
    """
# Stock Analysis
""",
    unsafe_allow_html=True,
)
st.markdown("---")

today = datetime.date.today()

# =========================
# Popular tickers & inputs
# =========================
popular_stocks = {
    "NVIDIA (NVDA)": "NVDA",
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Tesla (TSLA)": "TSLA",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "Google / Alphabet (GOOGL)": "GOOGL",
    "Netflix (NFLX)": "NFLX",
}

col1, col2, col3 = st.columns(3)

# How user chooses the stock (popular list vs manual input)
with col1:
    mode = st.radio(
        "How do you want to choose?",
        ["Popular list", "Type manually"],
        horizontal=True,
    )

    if mode == "Popular list":
        stock_label = st.selectbox("Choose a stock", list(popular_stocks.keys()))
        ticker = popular_stocks[stock_label]
    else:
        ticker = st.text_input("Stock Ticker", "TSLA")

# Date range selectors
with col2:
    start_date = st.date_input(
        "Choose Start Date",
        datetime.date(today.year - 1, today.month, today.day),
    )

with col3:
    end_date = st.date_input(
        "Choose End Date",
        datetime.date(today.year, today.month, today.day),
    )

# Main header for selected ticker
st.subheader(ticker)  # could also use stock_name if you prefer full company name

# =========================
# Company info (yfinance)
# =========================
stock = yf.Ticker(ticker)
stock_info = stock.info

# Use a nicer display name if possible
if mode == "Popular list":
    stock_name = stock_label  # e.g. "NVIDIA (NVDA)"
else:
    stock_name = stock_info.get("longName", ticker)  # e.g. "NVIDIA Corporation"

# ---------- Sidebar: company summary ----------
logo_url = stock_info.get("logo_url", None)
if logo_url:
    st.sidebar.image(logo_url, width=200)

st.sidebar.markdown(f"# {stock_name} Stock Analysis")
st.sidebar.markdown(f"**Ticker:** `{ticker}`")

sector = stock_info.get("sector", None)
if sector:
    st.sidebar.markdown(f"**Sector:** {sector}")

employees = stock_info.get("fullTimeEmployees", None)
if employees:
    st.sidebar.markdown(f"**Full Time Employees:** {employees:,}")

website = stock_info.get("website", None)
if website:
    st.sidebar.markdown(f"**Website:** [{website}]({website})")

# Short description (trimmed so it doesn’t take over the sidebar)
summary = stock_info.get("longBusinessSummary", "")
if summary:
    st.sidebar.markdown("### About the company")
    st.sidebar.markdown(summary[:500] + ("..." if len(summary) > 500 else ""))

st.sidebar.markdown("### Data range")
st.sidebar.markdown(f"{start_date} → {end_date}")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Manvendra Ray")
st.sidebar.write("Contact: mr6695@nyu.edu")

# =========================
# Fundamentals tables
# =========================
col1, col2 = st.columns(2)

with col1:
    df_left = pd.DataFrame(
        {
            "Metric": ["Market Cap", "Beta", "EPS", "PE Ratio"],
            "Value": [
                stock.info["marketCap"],
                stock.info["beta"],
                stock.info["trailingEps"],
                stock.info["trailingPE"],
            ],
        }
    )
    st.dataframe(df_left, hide_index=True, use_container_width=True)

with col2:
    df_right = pd.DataFrame(
        {
            "Metric": [
                "Quick Ratio",
                "Revenue per share",
                "Profit Margins",
                "Debt to Equity",
                "Return on Equity",
            ],
            "Value": [
                stock.info["quickRatio"],
                stock.info["revenuePerShare"],
                stock.info["profitMargins"],
                stock.info["debtToEquity"],
                stock.info["returnOnEquity"],
            ],
        }
    )
    st.dataframe(df_right, hide_index=True, use_container_width=True)


# =========================
# Historical price data
# =========================
data = yf.download(ticker, start=start_date, end=end_date)

# Data for the simple built-in Streamlit charts
df_select = data[["Open", "High", "Low", "Close", "Volume"]].copy()

# If yf returns a MultiIndex (e.g. ('Open', 'NVDA')), flatten to just 'Open', etc.
if isinstance(df_select.columns, pd.MultiIndex):
    df_select.columns = df_select.columns.get_level_values(0)

# Pretty name for chart titles
stock_name = stock_label if mode == "Popular list" else ticker

# =========================
# Metrics (daily change)
# =========================
col1, col2, col3 = st.columns(3)

last_close = float(data["Close"].iloc[-1])
prev_close = float(data["Close"].iloc[-2])
daily_change = last_close - prev_close

col1.metric(
    "Daily Change",
    str(round(last_close, 2)),
    str(round(daily_change, 2)),
)

# =========================
# Last 10 days table
# =========================
last_10_df = data.tail(10).sort_index(ascending=False).round(3)

# Drop ticker level if present
if isinstance(last_10_df.columns, pd.MultiIndex):
    last_10_df.columns = last_10_df.columns.get_level_values(0)

# Last 10 rows, newest at the top
last_10_df = data.tail(10).sort_index(ascending=False).round(3)

# Flatten MultiIndex if yfinance returns ('Close', 'NVDA') etc.
if isinstance(last_10_df.columns, pd.MultiIndex):
    last_10_df.columns = last_10_df.columns.get_level_values(0)

# Move the Date index into a proper column so it looks like a DB table
history_df = last_10_df.reset_index().rename(columns={"index": "Date"})

st.write("##### Historical Data (Last 10 days)")
st.dataframe(history_df, hide_index=True, use_container_width=True)


# =========================
# Time period buttons
# =========================
col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns(
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
)

num_period = ""

with col1:
    if st.button("5D"):
        num_period = "5d"

with col2:
    if st.button("1M"):
        num_period = "1mo"

with col3:
    if st.button("6M"):
        num_period = "6mo"

with col4:
    if st.button("YTD"):
        num_period = "ytd"

with col5:
    if st.button("1Y"):
        num_period = "1y"

with col6:
    if st.button("5Y"):
        num_period = "5y"

with col7:
    if st.button("MAX"):
        num_period = "max"

# =========================
# Chart type & indicator selection
# =========================
col1, col2, col3 = st.columns([1, 1, 4])

with col1:
    chart_type = st.selectbox("", ("Candle", "Line"))

with col2:
    if chart_type == "Candle":
        indicators = st.selectbox("", ("RSI", "MACD"))
    else:
        indicators = st.selectbox("", ("RSI", "Moving Average", "MACD"))

# Full-history data for the custom Plotly charts
ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period="max")  # keeping this since you had it
data1 = ticker_.history(period="max")

# =========================
# Custom indicator charts
# =========================
if num_period == "":
    # Default to 1Y when no button is pressed
    if chart_type == "Candle" and indicators == "RSI":
        st.plotly_chart(candlestick(data1, "1y"), use_container_width=True)
        st.plotly_chart(RSI(data1, "1y"), use_container_width=True)

    if chart_type == "Candle" and indicators == "MACD":
        st.plotly_chart(candlestick(data1, "1y"), use_container_width=True)
        st.plotly_chart(MACD(data1, "1y"), use_container_width=True)

    if chart_type == "Line" and indicators == "RSI":
        st.plotly_chart(close_chart(data1, "1y"), use_container_width=True)
        st.plotly_chart(RSI(data1, "1y"), use_container_width=True)

    if chart_type == "Line" and indicators == "Moving Average":
        st.plotly_chart(Moving_average(data1, "1y"), use_container_width=True)

    if chart_type == "Line" and indicators == "MACD":
        st.plotly_chart(close_chart(data1, "1y"), use_container_width=True)

# =========================
# Built-in Streamlit charts
# =========================
st.subheader(f"Open & Close Prices for {stock_name} Stock")
st.line_chart(df_select[["Open", "Close"]])

st.subheader(f"High and Low Prices for {stock_name} Stock")
st.line_chart(df_select[["High", "Low"]])

st.subheader(f"Volume Traded for {stock_name} Stock")
st.bar_chart(df_select["Volume"])

st.subheader(f"Moving Averages of Open and Closing Stock Prices for {stock_name}")
moveavg_len = st.slider(
    "Select the number of days for Moving Averages",
    min_value=1,
    max_value=250,
    value=50,
)
moveavg_oc = df_select[["Open", "Close"]].rolling(moveavg_len).mean()
st.line_chart(moveavg_oc)
