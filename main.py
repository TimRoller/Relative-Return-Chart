import pandas_datareader as web
import datetime as dt
import plotly.graph_objects as go
import pandas as pd

start = dt.datetime(2021,1,1)
end = dt.datetime.now()
Tickers = ['SPY', '1INCH-USD', 'ETH-USD','BTC-USD','BAT-USD','UNI1-USD', 'ATOM-USD', 'AAVE-USD', 'DOGE-USD', 'MATIC-USD']
Labels = ['S&P500','1INCH', 'ETH','BTC','BAT','UNI', 'ATOM', 'AAVE', 'DOGE', 'MATIC']
Returns = {}

fig = go.Figure()

Returns = pd.DataFrame(columns=['Ticker', 'Return', 'Drawdown'])

for index,value in enumerate(Tickers):
    df = web.DataReader(value, 'yahoo', start, end)

    fig.add_trace(go.Scatter(x=df.index, y=round(100*df['Adj Close']/(df['Adj Close'][0])-100,0),name=Labels[index]))
    df['daily_returns'] = (df['Adj Close'] / df['Adj Close'].shift(1)) - 1

    # Drop all Not a number values using drop method.
    df['daily_returns'].dropna(inplace=True)

    df["total_return"] = df["daily_returns"].cumsum()
    df["drawdown"] = df["total_return"] - df["total_return"].cummax()
    maxdd = df["drawdown"].min()

    temp_return = {
        'Ticker': value,
        'Return': 100*(df['Adj Close'].iloc[-1])/(df['Adj Close'][0])-100,
        'Drawdown': 100*maxdd
    }
    Returns = Returns.append(temp_return, ignore_index=True)

Returns.sort_values(by=['Return'], inplace=True, ascending=False)
Returns['Return'] = Returns['Return'].map('{:,.0f}%'.format)
Returns['Drawdown'] = Returns['Drawdown'].map('{:,.0f}%'.format)

fig.update_traces(mode="lines", hovertemplate=None)
fig.update_layout(hovermode="x")
fig.update_layout(yaxis_type="log")
fig.update_layout(title='Total % Return since 2021 on Log Scale')
fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))

print (Returns)
fig.show()
