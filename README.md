Project Documentation: LLM Playground
Project Overview
The LLM Playground is an interactive and user-friendly web application that allows users to engage in real-time conversations with various state-of-the-art Large Language Models (LLMs) hosted on the Hugging Face Hub. Built with Python and Streamlit, the application provides a clean chat interface, supports multi-turn conversations, and demonstrates modern web development practices for creating AI-powered applications.
The core functionality revolves around connecting to the Hugging Face Inference API, sending user prompts along with conversation history, and streaming the model's response back to the user in real-time.

Key Features
Dynamic Chat Interface: A responsive and intuitive chat UI built using Streamlit's st.chat_message and st.chat_input components, providing a familiar messaging experience.
Multi-Model Selection: Users can dynamically switch between different powerful LLMs (e.g., mistralai/Mistral-7B-Instruct-v0.2) via a dropdown menu in the sidebar.
Real-time Streaming Responses: Assistant responses are streamed token-by-token directly to the UI using st.write_stream. This provides an engaging user experience, as the response appears as if it's being typed live.
Persistent Conversation History: The application maintains the full conversation history within the user's session using st.session_state. This context is sent back to the model with each new prompt, enabling coherent, multi-turn dialogues.
Secure Credential Management: The Hugging Face API token is handled securely using Streamlit's built-in secrets management (st.secrets), preventing sensitive information from being hardcoded in the source.
Chat Session Management: Users have the ability to clear the entire chat history with a single button click, allowing them to easily start a new conversation.
Conversation Export: A feature to download the entire chat log as a formatted .txt file, allowing users to save their interactions for future reference.

Technical Stack
Language: Python 3
Framework: Streamlit
Core Libraries:
huggingface-hub: To interact with the Hugging Face Inference API.
streamlit: For building the web application front-end and managing state.
Platform/API: Hugging Face Inference API

Code Highlights & Best Practices
This project demonstrates several software engineering best practices for building modern AI applications.
Modular Backend Logic: The API interaction logic is separated into a dedicated function (get_assistant_response in test_inference.py), promoting code reusability and separation of concerns.
Efficient Streaming with Generators: The application uses a Python generator to yield response tokens as they are received from the API. This is memory-efficient and enables the real-time streaming feature on the front-end via st.write_stream.
# In g:\zip cache\LLM_Playground (1)\LLM_Playground\test_inference.py
def get_assistant_response(model: str, messages: list, token: str):
    """
    Connects to the Hugging Face Inference API and gets a streaming response.
    ...
    """
    client = InferenceClient(model=model, token=token)
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

3) Stateful Application Design: Streamlit's st.session_state is effectively used to maintain the chat history (messages) across user interactions and app reruns, which is crucial for a stateful chat application.
# In g:\zip cache\LLM_Playground (1)\LLM_Playground\app.py
# --- SESSION STATE INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- USER INPUT AND RESPONSE HANDLING ---
if prompt := st.chat_input("What is the capital of France?"):
    # Add user message to session state
    st.session_state.messages.append(...)

    # ... API call ...

    # Add assistant's full response to session state
    st.session_state.messages.append(...)



4) Secure Authentication: The application avoids hardcoding API keys. Instead, it leverages Streamlit's recommended approach for secrets management, gracefully handling errors if the token is not found.
 

# In g:\zip cache\LLM_Playground (1)\LLM_Playground\app.py
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except FileNotFoundError:
    st.error("Please provide your Hugging Face API token in a .streamlit/secrets.toml file.")
    st.stop()
