import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
st.title("☑️나만의 챗GPT 테스트😂")
from dotenv import load_dotenv
load_dotenv()

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    
with st.sidebar:
    clear_btn = st.button("대화 초기화")
    if clear_btn:
        st.session_state["messages"] = []
        
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)
        
def add_messages(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))
    
def create_chain():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트입니다"),
        ("user", "#Question:\n{question}")
    ])
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    output_parser = StrOutputParser()
    
    chain = prompt | llm | output_parser
    return chain

print_messages()

user_input = st.chat_input("궁금한 내용을 물어보세요!")

if user_input:
    st.chat_message("user").write(user_input)
    chain = create_chain()
    response = chain.invoke({"question": user_input})
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)
            
    add_messages("user", user_input)
    add_messages("assistant", ai_answer)