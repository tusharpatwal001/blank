import os
from dotenv import load_dotenv

load_dotenv()
from huggingface_hub import InferenceClient
print(os.getenv("HF_TOKEN"))
client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

completion = client.chat.completions.create(
    model='deepseek-ai/DeepSeek-V4-Pro',
    messages=[
        {
            "role":"user",
            "content":"What is your cutoff date?"
        }
    ]
)

print(completion.choices[0].message)

# ChatCompletionOutputMessage(role='assistant', content='My knowledge cutoff is **May 2025**. I don’t have information on events or developments that occurred after that date unless you enable web search in our interface (Web/App). Let me know how I can help!', reasoning=None, tool_call_id=None, tool_calls=None, reasoning_content='We need to understand the user\'s question: "What is your cutoff date?" This is a common question asked to AI models about the knowledge cutoff date. The user wants to know when my training data ends.I need to respond with my knowledge cutoff date. I\'m DeepSeek, and my knowledge is up to May 2025. I\'ll state that clearly. No need for extra details unless asked. I\'ll keep it simple.')