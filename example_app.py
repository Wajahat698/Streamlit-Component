import streamlit as st
from st_chat_input_multimodal import multimodal_chat_input
import time

st.set_page_config(page_title="ChatGPT-like Input Demo", page_icon="💬", layout="centered")

# ================== SESSION STATE ==================
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False
if "messages" not in st.session_state:
    st.session_state.messages = []  # {"role": "user"|"assistant", "content": ...}
if "stop_signal" not in st.session_state:
    st.session_state.stop_signal = False
if "current_response" not in st.session_state:
    st.session_state.current_response = ""  # stores partial response
if "placeholder_index" not in st.session_state:
    st.session_state.placeholder_index = None  # track which message is streaming

# ================== DISPLAY CHAT ==================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ================== CHAT INPUT ==================

st.markdown("hello")
result = multimodal_chat_input(
    placeholder="Type a message and click send…",
    enable_voice_input=True,
    is_generating=st.session_state.is_generating,
)

# ================== HANDLE USER ACTION ==================
if result is not None:
    action = result.get("action") or "send"

    if action == "send":
        text = result.get("text", "").strip()
        if text:
            # Add user message
            st.session_state.messages.append({"role": "user", "content": text})
            # Prepare to generate assistant response
            st.session_state.is_generating = True
            st.session_state.stop_signal = False
            st.session_state.current_response = ""
            # Add placeholder assistant message
            st.session_state.messages.append({"role": "assistant", "content": ""})
            st.session_state.placeholder_index = len(st.session_state.messages) - 1
            st.rerun()

    elif action == "stop":
        st.session_state.stop_signal = True
        st.session_state.is_generating = False
        st.rerun()

# ================== STREAM AI RESPONSE ==================
if st.session_state.is_generating and st.session_state.placeholder_index is not None:
    simulated_response = ("This is a very long simulated AI response. " * 50)  # long response
    partial_response = st.session_state.current_response

    for char in simulated_response[len(partial_response):]:
        if st.session_state.stop_signal:
            partial_response += "\n\n**[Generation stopped by user]**"
            st.session_state.current_response = partial_response
            # Update the placeholder in messages
            st.session_state.messages[st.session_state.placeholder_index]["content"] = partial_response
            st.session_state.is_generating = False
            st.session_state.placeholder_index = None
            st.rerun()
            break

        partial_response += char
        st.session_state.current_response = partial_response
        st.session_state.messages[st.session_state.placeholder_index]["content"] = partial_response
        # Small delay to simulate streaming
        time.sleep(0.01)

    # Finished generation
    if not st.session_state.stop_signal:
        st.session_state.is_generating = False
        st.session_state.current_response = ""
        st.session_state.placeholder_index = None
        st.rerun()
