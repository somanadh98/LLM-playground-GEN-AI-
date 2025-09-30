# import os
# from huggingface_hub import InferenceClient

# class HFChatClient:
#     def __init__(self, model="google/flan-t5-large", token=None):
#         self.model = model
#         self.token = token or os.getenv("HF_TOKEN")
#         if not self.token:
#             raise ValueError("Hugging Face token not provided!")
#         self.client = InferenceClient(model=self.model, token=self.token)

#     def chat(self, messages, max_tokens=200):
#         prompt = ""
#         for msg in messages:
#             role = "User" if msg["role"] == "user" else "Assistant"
#             prompt += f"{role}: {msg['content']}\n"
#         prompt += "Assistant:"

#         response = self.client.text_generation(
#             prompt,
#             max_new_tokens=max_tokens
#         )
#         return response.strip()

from huggingface_hub import InferenceClient

def get_assistant_response(model: str, messages: list, token: str):
    """
    Connects to the Hugging Face Inference API and gets a streaming response.

    Args:
        model (str): The model ID to use for inference.
        messages (list): The conversation history in the required format.
        token (str): The Hugging Face API token for authentication.

    Yields:
        str: Chunks of the generated text from the model.
    """
    # Use huggingface_hub.InferenceClient to connect to the model [cite: 19]
    client = InferenceClient(model=model, token=token)
    
    # Use client.chat_completion with streaming enabled
    response = client.chat_completion(
        messages=messages,
        max_tokens=500,
        stream=True
    )
    
    # Yield each token as it is generated
    for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content is not None:
            yield delta.content