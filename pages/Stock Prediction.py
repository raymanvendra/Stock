import streamlit as st
from pages.utils.model_train import (get_data, get_rolling_mean, get_differencing_order, scaling, evaluate_model, get_forecast, inverse_scaling,)
import pandas as pd
from pages.utils.plotly_figure import plotly_table, Moving_average_forecast

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
)
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
st.title("Stock Prediction")

col1, col2, col3 = st.columns(3)

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

rmse = 0

st.subheader('Predicting Next 30 days Close Price for: ' + ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scaler = scaling(rolling_price)
rmse = evaluate_model(scaled_data, differencing_order)


st.write("**Model RMSE Score:**", rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling(scaler, forecast['Close'])
st.write('##### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending=True).round(3))
fig_tail.update_layout(height=220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])

st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), use_container_width=True)





