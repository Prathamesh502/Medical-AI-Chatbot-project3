import streamlit as st
from connect_memory_with_llm import get_response
import time
def main():
    st.set_page_config(page_title="HealthVis 🩺", page_icon="🩺", layout="wide")

    st.markdown("<h1 style='text-align: center; font-size: 3rem;'>👋 Hi, I am HealthVis!🧠😊</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: gray;'>Your friendly medical advisor. How can I help you today?🩺💡</h3>", unsafe_allow_html=True)
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Type your question here… 💬")

    if prompt:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": f"🗨️ {prompt}"})
        with st.chat_message("user"):
            st.markdown(f"🗨️ {prompt}")

        # Get response (simulated streaming for smooth UI)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response_generator = get_response(prompt)

            # This part simulates streaming the response
            for chunk in response_generator.split(): # Replace with your actual streaming logic
                full_response += chunk + " "
                time.sleep(0.05) # Small delay to simulate typing
                message_placeholder.markdown(f"🩺 {full_response}▌")

            message_placeholder.markdown(f"🩺 {full_response}")
            st.session_state.messages.append({"role": "assistant", "content": f"🩺 {full_response}"})

        # Place the auto-scroll code here
        # This ensures the scroll happens after the new message is rendered
        st.components.v1.html("""
            <script>
                const chatDiv = window.parent.document.querySelector('div.stApp');
                if (chatDiv) chatDiv.scrollTop = chatDiv.scrollHeight;
            </script>
        """, height=0)

# The rest of your code
if __name__ == "__main__":
    main()






