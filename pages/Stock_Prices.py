import streamlit as st
import pandas as pd
import datetime



# If you already call set_page_config in Trading_App.py, you can
# keep this or comment it out. It’s safe in a standalone page.
st.set_page_config(
    page_title='Stock Pricessss',
    page_icon='https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png',
    layout="wide",
)

# --- Header / social links ---
st.markdown(
    """

# Nvidia's Stock Performance
""",
    unsafe_allow_html=True,
)

st.markdown('---')
# Dictionary of popular stocks: label -> ticker
popular_stocks = {
    "NVIDIA (NVDA)": "NVDA",
    "Apple (AAPL)": "AAPL",
    "Microsoft (MSFT)": "MSFT",
    "Tesla (TSLA)": "TSLA",
    "Amazon (AMZN)": "AMZN",
    "Meta (META)": "META",
    "Google / Alphabet (GOOGL)": "GOOGL",
    "Netflix (NFLX)": "NFLX"
}

# Dropdown for user to choose stock
stock_label = st.selectbox(
    "Choose a stock",
    list(popular_stocks.keys()),
    index=0
)

# Get the ticker symbol from selection
ticker = popular_stocks[stock_label]

# --- Sidebar ---
st.sidebar.image(
    'https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png',
    width=200,
)
st.sidebar.markdown('# Nvidia Stock Price Analysis')
st.sidebar.markdown(
    'Nvidia is a global leader in artificial intelligence hardware and software.'
)
st.sidebar.markdown('Stock Data from 2019 thru 2021')
st.sidebar.markdown(
    "You can visualise Nvidia's stock price trends and patterns over a given time span."
)
st.sidebar.markdown('---')
st.sidebar.write('Developed by Manvendra Ray')
st.sidebar.write('Contact at mr6695@nyu.edu')

# --- Load & prepare data ---
df = pd.read_csv('NVidia_stock_history.csv')

# Parse dates as UTC → filter → drop timezone
df['Date'] = pd.to_datetime(df['Date'], utc=True)
cutoff = pd.to_datetime('2019-01-01', utc=True)
df = df[df['Date'] >= cutoff]
df['Date'] = df['Date'].dt.tz_convert(None)  # make them tz-naive for convenience
df.set_index('Date', inplace=True)

# --- Show raw data & stats ---
st.subheader('Looking at the Data')
st.dataframe(df.head())

st.subheader('Statistical Info about the Data')
st.write(df.describe())

# --- Date range selection ---
st.subheader('Select a Date Range')
df_select = df.copy()

col1, col2 = st.columns(2)

min_date = df.index.min().date()
max_date = df.index.max().date()

with col1:
    st.write('Select a Start Date')
    start_date = st.date_input(
        'Start Date',
        min_value=min_date,
        max_value=max_date,
        value=min_date,
    )

with col2:
    st.write('Select an End Date')
    end_date = st.date_input(
        'End Date',
        min_value=min_date,
        max_value=max_date,
        value=max_date,
    )

if start_date and end_date:
    if start_date <= end_date:
        df_select = df.loc[start_date:end_date]
    else:
        st.warning("Invalid Date Range - Re-enter Dates")

# --- Charts ---
st.subheader("Open & Close Prices for Nvidia Stock")
st.line_chart(df_select[['Open', 'Close']])

st.subheader("High and Low Prices for Nvidia Stock")
st.line_chart(df_select[['High', 'Low']])

st.subheader("Volume Traded for Nvidia Stock")
st.bar_chart(df_select['Volume'])

st.subheader('Moving Averages of Open and Closing Stock Prices')
moveavg_len = st.slider(
    'Select the number of days for Moving Averages',
    min_value=1,
    max_value=250,
    value=50,
)
moveavg_oc = df_select[['Open', 'Close']].rolling(moveavg_len).mean()
st.line_chart(moveavg_oc)

