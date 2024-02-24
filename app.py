import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets.OpenAIAPI.openai_api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Piensa como un ingeniero de Software"}
    ]

def comunicate():
    user_input = st.session_state.get("user_input", "")  # Get user input from session state
    if user_input.strip():  # Check if user input is not empty
        messages = st.session_state["messages"]
        user_message = {"role": "user", "content": user_input}
        messages.append(user_message)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        bot_messages = response.choices[0].messages
        for bot_message in bot_messages:
            messages.append(bot_message)

        st.session_state["user_input"] = ""  # Reset user input after processing

    st.title("Desarrollador AI")
    st.write("Utilizando la API chatGPT, este chatbot ofrece capacidades conversacionales avanzadas.")

    st.text_input("Por favor ingrese un mensaje aquí", key="user_input", on_change=comunicate)

    if st.session_state["messages"]:
        messages = st.session_state["messages"]
        for message in reversed(messages[1:]):
            if isinstance(message, dict):
                speaker = "😎" if message["role"] == "user" else "🤖"
                st.write(speaker + ": " + message["content"])
            else:
                st.write("🤖: " + message.content)

# Call the function to start the app
comunicate()
