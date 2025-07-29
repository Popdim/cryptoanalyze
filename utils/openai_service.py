import os
import logging
import openai
from config import ANN_KEY, base_url


async def get_ai_prediction(prompt, model="gpt-4o", max_token=500):
    try:
        client = openai.OpenAI(api_key=ANN_KEY, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "ты опытный инвестор в криптомире. объясняй простым языком"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_token,
            temperature=1
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        logging.error(f'ошибка запроса {e}')
        return f"ошибка запроса {e}"

