import streamlit as st
import os
import pytz
import datetime
import requests
import json

st.set_page_config(page_title="藤田ソフィアのチャットルーム", page_icon="💬")

with st.sidebar:
    st.title('藤田ソフィアのチャットルーム')

if "history" not in st.session_state:
    st.session_state.history = []

def askllm(query):
    try:
        response = requests.post(st.secrets["LLM_URL"], json={"query":query})
        restext = json.loads(response.text)["text"]
        st.markdown(restext)
        st.session_state.history.append({"role": "user", "content": query})
        st.session_state.history.append({"role": "ai", "content": restext})
    except:
        st.text("お待たせしごめんなさい。順番にお答えしていきますね。しばらく待ってからまたいらしてくださいね！")


for chat in st.session_state.history:
    if chat["role"] == "user":
        with st.chat_message("user"):
            st.markdown(chat['content'])
    else:
        with st.chat_message("assistant"):
            st.markdown(chat['content'])

if len(st.session_state.history) == 0:
    askllm("手短に自己紹介して")

def clear_chat_history():
    st.session_state.history = []

st.sidebar.button('履歴クリア', on_click=clear_chat_history, use_container_width=True)

if prompt := st.chat_input("何でも聞いてください。"):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            askllm(prompt)
