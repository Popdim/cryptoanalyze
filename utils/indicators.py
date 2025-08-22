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


def calculate_macd(price, fast_period=14, slow_period=30, signal_period=9):
    price = pd.Series(price)
    fast_ema = calculate_ema(price, period=fast_period)
    slow_ema = calculate_ema(price, period=slow_period)
    macd_line = fast_ema - slow_ema
    signal_line = calculate_ema(macd_line, period=signal_period)
    histogram = macd_line - signal_line
    return {"macd_line": macd_line, "signal_line": signal_line, "histogram": histogram}


def get_macd(df, fast_period=14, slow_period=30, signal_period=9):
    macd_data = calculate_macd(df["price"], fast_period, slow_period, signal_period)
    return {"macd_line": round(macd_data["macd_line"].iloc[-1], 2),
            "signal_line": round(macd_data["signal_line"].iloc[-1], 2),
            "histogram": round(macd_data["histogram"].iloc[-1], 2), }


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


def macd_signal(macd_line, signal_line, histogram, preview_histogram=None):
    if macd_line > signal_line and histogram > 0:
        if preview_histogram is not None and preview_histogram <= 0:
            return "buy"
        elif histogram>0:
            return "bullish"
    elif macd_line< signal_line and histogram<0:
        if preview_histogram is not None and preview_histogram >= 0:
            return "sell"
        elif histogram<0:
            return "bearish"
    return "hold"
if __name__ == '__main__':
    df = get_historical_data(coin_id="bitcoin", currency="usd", days=14)
    # rsi = calculate_rsi(df["price"])
    # last_rsi = rsi.iloc[-1]
    ema = calculate_ema(df["price"])
    last_ema = ema.iloc[-1]
    print(last_ema)
