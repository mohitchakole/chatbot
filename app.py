
import streamlit as st
import config
import chatbot

st.set_page_config(page_title="Simple Chatbot")
st.title("Chatbot")
st.caption(f"Provider: {config.LLM_PROVIDER}")

configuration_error = config.get_configuration_error()

if configuration_error:
    st.error(configuration_error)
    st.stop()

user_input = st.chat_input("Ask me anything...")

if user_input and user_input.strip():
    question = user_input.strip()

    with st.chat_message("user"):
        st.write(question)

    try:
        with st.spinner("Thinking..."):
            reply = chatbot.get_llm_response([
                {"role": "system", "content": config.SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ])

        if reply:
            with st.chat_message("assistant"):
                st.write(reply)
        else:
            st.warning("The model returned an empty response.")

    except Exception as error:
        st.error(f"Request failed: {error}")
