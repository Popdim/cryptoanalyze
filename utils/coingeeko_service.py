from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime, timezone

cg = CoinGeckoAPI()
pd.set_option('display.float_format', '{:,.2f}'.format)


def get_current_price(coin_id, currency="usd"):
    data = cg.get_price(ids=coin_id, vs_currencies=currency)
    if coin_id in data and currency in data[coin_id]:
        return data[coin_id][currency]
    else:
        return None


def get_historical_data(coin_id, currency="usd", days=90):
    """получить историческую информацию о монете"""
    data = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)
    prices = data["prices"]
    volumes = data["total_volumes"]
    print(prices)
    print(volumes)
    date_list = []
    price_list = []
    volume_list = []
    for price, volume in zip(prices, volumes):
        timestamp = price[0] / 1000
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        print(dt)
        date_list.append(dt)
        price_list.append(price[1])
        volume_list.append(volume[1])
    df = pd.DataFrame({'date': date_list, 'price': price_list, 'volume': volume_list})
    # print(df)
    return df


def get_daily_summary(coin_id, vs_currency="usd"):
    df = get_historical_data(coin_id, vs_currency, days=1)
    if df is None or len(df) == 0:
        return None
    current_price = df["price"].iloc[-1]
    min_price = df["price"].min()
    max_price = df["price"].max()
    total_volume = df["volume"].sum()
    summary = {
        "current_price": current_price,
        "min_price": min_price,
        "max_price": max_price,
        "total_volume": total_volume
    }
    return summary


if __name__ == '__main__':
    # price = get_current_price("ethereum")
    # price = get_historical_data("bitcoin", days=360)
    price = get_daily_summary("bitcoin")
    print(price)
