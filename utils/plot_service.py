import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from pathlib import Path
from utils.coingeeko_service import get_historical_data
from utils.indicators import calculate_ema, calculate_rsi, simple_signal
from utils.openai_service import get_ai_prediction


def plotpricechart(coin_id, days=30):
    df = get_historical_data(coin_id, days=days)
    if df is None or df.empty:
        return None
    charts_dir = Path('charts')
    if not charts_dir.exists():
        charts_dir.mkdir(parents=True)
    ema = calculate_ema(df['price'], period=days)
    rsi = calculate_rsi(df['price'], period=days)
    fig, (exprice, exrsi) = plt.subplots(
        2, 1, figsize=(10, 7), sharex=True, gridspec_kw={'height_ratios': [3, 1]}
    )
    fig.suptitle(f'{coin_id}-цена, rsi, ema', fontsize=14)
    exprice.plot(df['date'], df['price'], label="цена", linewidth=2)
    exprice.plot(df['date'], ema, label="ema", linestyle='--', linewidth=2)
    exprice.set_ylabel('цена')
    exprice.legend(loc='upper left')
    exprice.grid(True, alpha=0.3)
    signal = [simple_signal(r) for r in rsi]
    colors = {'buy': 'green',
              'hold': 'yellow',
              'sell': 'red'}
    last_signal = None
    start_index = 0

    for i, sig in enumerate(signal):
        if sig != last_signal and last_signal is not None:
            exprice.axvspan(
                df['date'].iloc[start_index],
                df['date'].iloc[i - 1],
                color=colors.get(last_signal, "grey"), alpha=0.07
            )
            start_index=i
        last_signal=sig
    exprice.axvspan(
        df['date'].iloc[start_index],
        df['date'].iloc[i - 1],
        color=colors.get(last_signal, "grey"), alpha=0.07
    )
    exrsi.plot(df['date'], rsi, label='rsi', color='blue')
    exrsi.axhline(70, color='red', linestyle="--", alpha=0.7, label='rsi sell 70')
    exrsi.axhline(30, color='green', linestyle="--", alpha=0.7, label='rsi buy 30')
    exrsi.set_ylabel("rsi")
    exrsi.set_xlabel("date")
    exrsi.legend(loc='upper left')
    exrsi.grid(True, alpha=0.3)
    plt.tight_layout(rect=[0,0.03, 1, 0.95])
    fname= charts_dir/f"{coin_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(fname)
    plt.close(fig)
    return fname
if __name__ == '__main__':
    plotpricechart(coin_id='ethereum', days=30)
