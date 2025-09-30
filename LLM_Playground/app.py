# import streamlit as st
# from datetime import datetime
# from test_inference import HFChatClient

# # ----------------------
# # App Config
# # ----------------------
# st.set_page_config(
#     page_title="🧠 LLM Playground",
#     page_icon="🤖",
#     layout="centered"
# )

# # ----------------------
# # Sidebar (Settings)
# # ----------------------
# with st.sidebar:
#     st.markdown("## ⚙️ Settings")

#     model_choice = st.selectbox(
#     "Choose Model:",
#     ["google/flan-t5-base", "google/flan-t5-large", "facebook/opt-350m"]
# )


#     if "hf_client" not in st.session_state or st.session_state["model"] != model_choice:
#         st.session_state["hf_client"] = HFChatClient(
#             model=model_choice,
#             token="YOUR_HF_TOKEN"  # 🔑 Replace with your HF token
#         )
#         st.session_state["model"] = model_choice

#     if st.button("🧹 Clear Chat"):
#         st.session_state["messages"] = []

# # ----------------------
# # Initialize Session
# # ----------------------
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []

# # ----------------------
# # Chat Display
# # ----------------------
# st.title("🧠 LLM Playground")

# for msg in st.session_state["messages"]:
#     role_icon = "🧑" if msg["role"] == "user" else "🤖"
#     st.markdown(f"**{role_icon} {msg['role'].capitalize()}:** {msg['content']} *(at {msg['time']})*")

# # ----------------------
# # User Input
# # ----------------------
# user_input = st.text_input("💬 Enter your message:", "")

# if user_input:
#     st.session_state["messages"].append(
#         {"role": "user", "content": user_input, "time": datetime.now().strftime("%H:%M:%S")}
#     )

#     with st.spinner("🤖 AI is typing..."):
#         response = st.session_state["hf_client"].chat(st.session_state["messages"])
    
#     st.session_state["messages"].append(
#         {"role": "assistant", "content": response, "time": datetime.now().strftime("%H:%M:%S")}
#     )
#     st.experimental_rerun()

# # ----------------------
# # Export Chat
# # ----------------------
# if st.button("📥 Export Chat"):
#     chat_text = ""
#     for msg in st.session_state["messages"]:
#         role = "User" if msg["role"] == "user" else "Assistant"
#         chat_text += f"{role} ({msg['time']}): {msg['content']}\n\n"

#     st.download_button(
#         label="Download Chat",
#         data=chat_text,
#         file_name="conversation.txt",
#         mime="text/plain"
#     )

import streamlit as st
from datetime import datetime
from test_inference import get_assistant_response

# --- PAGE CONFIG ---
st.set_page_config(page_title="LLM Playground", page_icon="🤖")

# --- AUTHENTICATION ---
# Use token-based authentication from Streamlit's secrets manager [cite: 21]
# This is CORRECT
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
except FileNotFoundError:
    st.error("Please provide your Hugging Face API token in a .streamlit/secrets.toml file.")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.title("LLM Playground")
    st.markdown("Chat with different Large Language Models from Hugging Face.")
    
    # Model selection dropdown [cite: 35]
    selected_model = st.selectbox(
        "Choose a model",
        ["mistralai/Mistral-7B-Instruct-v0.2", "mistralai/Mistral-7B-Instruct-v0.1"],
        key="selected_model"
    )
    
    # Clear Chat button [cite: 30]
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- SESSION STATE INITIALIZATION ---
# Construct and maintain chat history [cite: 23]
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CHAT UI ---
st.title("🤖 Conversational LLM Web App")

# Display previous chat messages
for message in st.session_state.messages:
    # Add chat avatars for user and AI [cite: 36]
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        # Add timestamp to chat turns (Optional Enhancement) [cite: 40]
        st.markdown(f"*{message['timestamp']}*")
        # Use Markdown-style message formatting [cite: 37]
        st.markdown(message["content"])

# --- USER INPUT AND RESPONSE HANDLING ---
# Input text box for user queries [cite: 27, 34]
if prompt := st.chat_input("What is the capital of France?"):
    # Get current time for timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": timestamp})
    with st.chat_message("user", avatar="👤"):
        st.markdown(f"*{timestamp}*")
        st.markdown(prompt)

    # Get and display assistant response
    with st.chat_message("assistant", avatar="🤖"):
        # Add animated typing indicator (Optional Enhancement) [cite: 42]
        with st.spinner("Thinking..."):
            # The conversation history is preserved across multiple turns [cite: 29]
            # We filter out the timestamp key before sending to the API
            api_messages = [
                {"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages
            ]
            
            # Get AI-generated response from the selected model [cite: 28]
            response_generator = get_assistant_response(
                model=selected_model,
                messages=api_messages,
                token=HF_TOKEN
            )
            
            # Use st.write_stream to display the streaming response
            full_response = st.write_stream(response_generator)
            
            # Add assistant's full response to session state
            response_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response, "timestamp": response_timestamp}
            )

# --- EXPORT FUNCTIONALITY ---
# Create a formatted string of the conversation history
chat_history = ""
for message in st.session_state.messages:
    avatar = "You" if message["role"] == "user" else "Bot"
    chat_history += f"[{message['timestamp']}] {avatar}:\n{message['content']}\n\n"

# Add the export button to the sidebar [cite: 38]
st.sidebar.download_button(
    label="Export Conversation",
    data=chat_history.encode("utf-8"),
    file_name="conversation.txt",
    mime="text/plain"
)