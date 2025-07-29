import pandas as pd
from utils.coingeeko_service import get_historical_data

df = get_historical_data(coin_id="bitcoin", currency="usd", days=14)


def calculate_rsi(prices, period=14):
    prices = pd.Series(prices)
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gained = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gained / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_ema(prices, period=14):
    prices = pd.Series(prices)
    ema = prices.ewm(span=period, adjust=False).mean()
    return ema


def get_rsi(df: pd.DataFrame, period=14):
    rsi = calculate_rsi(df["price"], period=period)
    last_rsi = rsi.iloc[-1]
    return last_rsi


def get_ema(prices, period=14):
    ema = calculate_ema(df["price"], period=period)
    last_ema = ema.iloc[-1]
    return last_ema


def simple_signal(rsi):
    if rsi > 70:
        return "sell"
    elif rsi < 30:
        return "buy"
    else:
        return "hold"


if __name__ == '__main__':
    df = get_historical_data(coin_id="bitcoin", currency="usd", days=14)
    # rsi = calculate_rsi(df["price"])
    # last_rsi = rsi.iloc[-1]
    ema = calculate_ema(df["price"])
    last_ema = ema.iloc[-1]
    print(last_ema)
