import streamlit as st
from openai import OpenAI
from prompts import INFO_PROMPT, TECH_PROMPT
from utils import extract_candidate_info

# Configure Streamlit page
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖")

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}

# OpenAI client (make sure OPENAI_API_KEY is set as env variable)
client = OpenAI()

st.title("🤖 TalentScout - Hiring Assistant")
st.write("Hello! I am TalentScout, your AI-powered hiring assistant. "
         "I’ll collect your details and ask technical questions based on your skills.")

# Chat input box
user_input = st.chat_input("Type your response here...")

if user_input:
    # Append user query
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Decide which prompt to use
    if "tech stack" not in st.session_state.candidate_info:
        prompt = INFO_PROMPT.format(history=st.session_state.conversation)
    else:
        prompt = TECH_PROMPT.format(stack=st.session_state.candidate_info["tech stack"])

    # LLM response
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}] + st.session_state.conversation
    )

    reply = response.choices[0].message.content

    # Extract candidate info if possible
    info = extract_candidate_info(user_input)
    st.session_state.candidate_info.update(info)

    # Save assistant reply
    st.session_state.conversation.append({"role": "assistant", "content": reply})

# Display chat history
for msg in st.session_state.conversation:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
