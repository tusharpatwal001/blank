import os
from dotenv import load_dotenv

load_dotenv()
from huggingface_hub import InferenceClient
print(os.getenv("HF_TOKEN"))
client = InferenceClient(
    api_key=os.getenv("HF_TOKEN")
)

completion = client.chat.completions.create(
    model='zai-org/GLM-5.2',
    messages=[
        {
            "role":"user",
            "content":"What is your cutoff date?"
        }
    ]
)

print(completion.choices[0].message)

# ChatCompletionOutputMessage(role='assistant', content="My knowledge is current up to June 2024. I was developed by Z.ai and am designed to provide helpful information within my knowledge scope. \n\nIs there something specific you'd like to know about? I'm happy to assist with questions while being upfront about the boundaries of my knowledge.", reasoning="The user is asking about my cutoff date. Let me recall what I know.\n\nI was developed by Z.ai, and my knowledge is current up to June 2024. That means I have information up to that point, but events or developments after that date might not be included in my responses. \n\nSince the cutoff is June 2024, I should make sure to mention that clearly. It's also helpful to note that I don't have real-time data or updates beyond then, so if the user asks about recent events, I might not have the latest info. \n\nI'll structure the response to be straightforward and informative, avoiding unnecessary details. The key points are the cutoff date itself and a brief explanation of what that means for the user's queries. No need to add extra context unless they ask for more.", tool_call_id=None, tool_calls=[])