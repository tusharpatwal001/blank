from openrouter import OpenRouter
from dotenv import load_dotenv
import os

load_dotenv()

with OpenRouter(api_key=os.getenv("OPENROUTER_API_KEY")) as client:
    response = client.chat.send(
        model="google/gemma-4-26b-a4b-it:free",
        messages=[
            {"role": "user", "content": "Explain quantum comppputing in one sentence."}
        ],
    )

    print(response.choices[0].message.content)

