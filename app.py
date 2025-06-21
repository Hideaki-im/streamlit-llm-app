from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

# アプリの概要・操作説明
st.title("LLM専門家相談アプリ")
st.write("""
このアプリは、OpenAIのLLM（大規模言語モデル）を使い、選択した専門家になりきって質問に答えます。
1. 専門家の種類を選択
2. 質問を入力
3. 「送信」ボタンで回答を表示
""")

# 専門家の種類
experts = {
    "医師": "あなたは優秀な医師です。医学的な観点から、わかりやすく丁寧に回答してください。",
    "弁護士": "あなたは経験豊富な弁護士です。法律的な観点から、わかりやすく丁寧に回答してください。",
    "エンジニア": "あなたは熟練したエンジニアです。技術的な観点から、わかりやすく丁寧に回答してください。"
}

# ラジオボタンで専門家選択
selected_expert = st.radio("専門家を選んでください", list(experts.keys()))

# 入力フォーム
user_input = st.text_area("質問を入力してください")

def get_llm_response(user_text, expert_key):
    """入力テキストと専門家種別を受け取り、LLMの回答を返す"""
    system_prompt = experts[expert_key]
    chat = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5, max_tokens=1000)
    
    # メッセージの構築
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_text)
    ]
    response = chat(messages)
    return response.content

if st.button("送信"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("回答を生成中..."):
            answer = get_llm_response(user_input, selected_expert)
            st.success("回答：")
            st.write(answer)