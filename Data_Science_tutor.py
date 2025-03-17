import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

load_dotenv()

os.environ["GOOGLE_API_KEY"] = "AIzaSyCrOc5PMlKnYpIuPzGO01HoQ8WZ6Ca6E5c"

st.set_page_config(
    page_title="Data Science Tutor",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    body {
        color: #f0f0f0;
    }
    .main-header {
        font-family: 'Arial', sans-serif;
        background: linear-gradient(90deg, #4776E6 0%, #8E54E9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        padding-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>✨ Data Science AI Tutor ✨</h1>", unsafe_allow_html=True)

if "conversations" not in st.session_state:
    st.session_state.conversations = {}

if "conversation_counter" not in st.session_state:
    st.session_state.conversation_counter = 0

if "current_conversation_id" not in st.session_state:
    new_id = str(uuid.uuid4())
    st.session_state.conversation_counter += 1
    st.session_state.current_conversation_id = new_id
    st.session_state.conversations[new_id] = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title": f"Conversation {st.session_state.conversation_counter}",
        "memory": ConversationBufferMemory(return_messages=True),
        "chat_history": []
    }

def get_current_conversation():
    return st.session_state.conversations[st.session_state.current_conversation_id]

def create_new_conversation():
    new_id = str(uuid.uuid4())
    st.session_state.conversation_counter += 1
    st.session_state.current_conversation_id = new_id
    st.session_state.conversations[new_id] = {
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title": f"Conversation {st.session_state.conversation_counter}",
        "memory": ConversationBufferMemory(return_messages=True),
        "chat_history": []
    }
    st.rerun()

def switch_conversation(conv_id):
    st.session_state.current_conversation_id = conv_id
    st.rerun()

def generate_conversation_title(user_input, ai_response):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.3,  
        convert_system_message_to_human=True
    )
    
    title_prompt = f"""
    Based on the following conversation, generate a brief, descriptive title (max 5 words):
    
    User: {user_input}
    AI: {ai_response}
    
    Title:
    """
    
    try:
        title = llm.invoke(title_prompt).content.strip()
        return (title[:40] + '...') if len(title) > 40 else title
    except:
        return (user_input[:30] + '...') if len(user_input) > 30 else user_input

def get_ai_response(user_input):
    current_conv = get_current_conversation()
    
    if "llm_chain" not in current_conv:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0.7,
            convert_system_message_to_human=True
        )
        
        template = """
        You are a helpful and knowledgeable Data Science Tutor. You are an expert in statistics, machine learning, 
        data analysis, Python, R, SQL, and data visualization. Your goal is to help users learn data science concepts 
        and solve data science problems.
        
        Important guidelines:
        1. Focus ONLY on data science topics. If the user asks about unrelated topics, politely redirect them to data science.
        2. Provide clear, concise explanations with examples when possible.
        3. Use code snippets to illustrate concepts when relevant.
        4. Break down complex topics into manageable parts.
        5. Encourage best practices and ethical data science.
        
        Current conversation:
        {history}
        
        Human: {input}
        AI Tutor:
        """
        
        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
        
        current_conv["llm_chain"] = ConversationChain(
            llm=llm,
            prompt=prompt,
            memory=current_conv["memory"],
            verbose=False
        )
    
    response = current_conv["llm_chain"].predict(input=user_input)
    
    if len(current_conv["chat_history"]) == 0:
        current_conv["title"] = generate_conversation_title(user_input, response)
    
    return response

with st.sidebar:
    st.markdown("# 💬 Conversations")
    
    if st.button("➕ New Conversation", key="new_conv_btn", use_container_width=True):
        create_new_conversation()
    
    st.markdown("#### Select a conversation:")
    for conv_id, conv_data in st.session_state.conversations.items():
        if st.button(
            f"📝 {conv_data['title']} ({conv_data['created_at']})",
            key=f"conv_{conv_id}",
            use_container_width=True,
            type="secondary" if conv_id != st.session_state.current_conversation_id else "primary"
        ):
            switch_conversation(conv_id)
    
    if st.button("🗑️ Clear Current Conversation", use_container_width=True):
        current_conv = get_current_conversation()
        current_conv["memory"].clear()
        current_conv["chat_history"] = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🧠 About Data Science Tutor")
    st.markdown("""
    This AI tutor is designed to help you with:
    - 📈 Statistics and probability
    - 🤖 Machine learning algorithms
    - 🧹 Data preprocessing and cleaning
    - 🐍 Python, R, and SQL for data science
    - 📊 Data visualization techniques
    - ⚙️ Feature engineering
    - 📏 Model evaluation and validation
    """)
    st.markdown("---")

current_conv = get_current_conversation()

st.markdown(f"## Chat with your Personalized Data Science Tutor :")
st.markdown("---")

for message in current_conv["chat_history"]:
    with st.chat_message(message["role"], avatar="👨‍💻" if message["role"] == "user" else "🧠"):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me about data science...")

if user_input:
    with st.chat_message("user", avatar="👨‍💻"):
        st.markdown(user_input)
    
    current_conv["chat_history"].append({"role": "user", "content": user_input})
    
    with st.spinner("Thinking... 🤔"):
        ai_response = get_ai_response(user_input)
    
    with st.chat_message("assistant", avatar="🧠"):
        st.markdown(ai_response)
    
    current_conv["chat_history"].append({"role": "assistant", "content": ai_response})