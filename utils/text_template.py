def make_ai_prompt(
        coin_id,
        summary,
        current_rsi,
        current_ema,
        signal_rsi,
        # price_change_24,
        # percent_change_24,
        # price_change_30,
        # percent_change_30
):
    prompt = f"""сделай краткий информативный прогноз по монете {coin_id} на основе слудющих данных:
           текущая цена {summary["current_price"]:.2f}USD
           минимальная цена за сутки {summary["min_price"]:.2f}USD
           максимальная цена за сутки {summary["max_price"]:.2f}USD
           объем торгов за сутки {summary["total_volume"]:.2f}USD
           RSI {current_rsi:.2f}
           EMA {current_ema:.2f}
"""
    return prompt


