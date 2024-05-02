import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('Big Tech Company Stock Prices')

st.sidebar.write("""
# Big Tech Company Stock Prices
This is a stock price visualization tool for Big Tech companies. You can specify the number of days to display from the following options
""")

st.sidebar.write("""
## Select the number of days to display
""")

days = st.sidebar.slider('Days', 1, 90, 20)

st.write(f"""
### Big tech company stock prices over the past **{days} days**.
""")

@st.cache_data
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = pd.to_datetime(hist.index)  # Ensure the index is datetime type
        hist.index = hist.index.strftime('%d %B %Y')  # Now you can safely format it
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df

try: 
    st.sidebar.write("""
    ## Stock Price Range Designation
    """)
    ymin, ymax = st.sidebar.slider(
        'Specify the range.',
        0.0, 3000.0, (0.0, 1500.0)
    )

    tickers = {
        'apple': 'AAPL',
        'facebook': 'META',
        'google': 'GOOGL',
        'microsoft': 'MSFT',
        'netflix': 'NFLX',
        'amazon': 'AMZN',
        'Tesla':'TSLA',
        'Alphabet': 'GOOGL',
        'NVIDIA': 'NVDA',
        'Adobe': 'ADBE',
        'Salesforce': 'CRM',
        'Twilio': 'TWLO',
        'Shopify': 'SHOP',
        'Baidu': 'BIDU',  
        'Alibaba': 'BABA',  
        'Tencent': 'TCEHY',  
        'HUAWEI': '002502.SZ'
    }
    df = get_data(days, tickers)
    companies = st.multiselect(
        'Please select a company name.',
        list(df.index),
        ['google', 'amazon', 'facebook', 'apple']
    )

    if not companies:
        st.error('Choose at least one company.')
    else:
        data = df.loc[companies]
        st.write("### stock prices (USD)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices(USD)'}
        )
        chart = (
            alt.Chart(data)
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Prices(USD):Q", stack=None, scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "Oops! Something seems to be in error."
    )