import streamlit as st
import requests

st.header("AI Chat (demo)", divider="orange")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_model" not in st.session_state:
    st.session_state.current_model = "model"

# Model selection
model = st.selectbox(
    "사용할 모델을 선택하세요:",
    (
        "model",
        "api",
    ),
    key="model_select",
)

# 대화 초기화
if model != st.session_state.current_model:
    st.session_state.messages = []
    st.session_state.current_model = model
    st.experimental_rerun()

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # API 요청
        with st.spinner("AI가 응답을 생성 중입니다..."):
            response = requests.post(
                "http://localhost:5000/generate",
                json={
                    "prompt": prompt,
                    "max_length": 100,
                    "model": model,
                    "messages": st.session_state.messages
                },
                # data={"prompt": prompt},
            )

        if response.status_code == 200:
            full_response = response.json()["generated_text"]
            # full_response = response.text
            message_placeholder.markdown(full_response)
        else:
            message_placeholder.error("오류가 발생했습니다.")

    # AI 메시지 추가
    st.session_state.messages.append({"role": "assistant", "content": full_response})
