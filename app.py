import streamlit as st
import json
import re
from typing import Dict, List, Any
import random

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_step" not in st.session_state:
    st.session_state.current_step = "greeting"
if "candidate_info" not in st.session_state:
    st.session_state.candidate_info = {}
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "current_tech_index" not in st.session_state:
    st.session_state.current_tech_index = 0

# Define the chatbot steps
STEPS = {
    "greeting": {
        "message": "Hello! Welcome to Talent Scout's hiring assistant. I'm here to help with the initial screening process. Could you please provide some basic information to get started?",
        "next_step": "get_name" 
    },
    "get_name": {
        "message": "Let's start with your full name:",
        "field": "full_name",
        "validation": r"^[A-Za-z\s]{2,50}$",
        "error_msg": "Please enter a valid name (2-50 characters, letters and spaces only).",
        "next_step": "get_email"
    },
    "get_email": {
        "message": "Thank you! Now, what's your email address?",
        "field": "email",
        "validation": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "error_msg": "Please enter a valid email address.",
        "next_step": "get_phone"
    },
    "get_phone": {
        "message": "Great! What's your phone number?",
        "field": "phone",
        "validation": r"^[\d\s\-\+\(\)]{10,20}$",
        "error_msg": "Please enter a valid phone number (10-20 digits).",
        "next_step": "get_experience"
    },
    "get_experience": {
        "message": "Thanks! How many years of professional experience do you have?",
        "field": "years_experience",
        "validation": r"^\d{1,2}(\.\d{1,2})?$",
        "error_msg": "Please enter a valid number of years (e.g., 3 or 2.5).",
        "next_step": "get_position"
    },
    "get_position": {
        "message": "What position(s) are you interested in?",
        "field": "desired_positions",
        "validation": r".{2,100}",
        "error_msg": "Please describe the position(s) you're interested in (2-100 characters).",
        "next_step": "get_location"
    },
    "get_location": {
        "message": "What's your current location?",
        "field": "location",
        "validation": r".{2,50}",
        "error_msg": "Please enter a valid location (2-50 characters).",
        "next_step": "get_tech_stack"
    },
    "get_tech_stack": {
        "message": "Please specify your tech stack (programming languages, frameworks, databases, tools). Separate them with commas:",
        "field": "tech_stack",
        "validation": r".{2,200}",
        "error_msg": "Please list at least one technology (2-200 characters).",
        "next_step": "generate_questions"
    },
    "generate_questions": {
        "message": "Thanks! Now I'll ask you a few technical questions based on your skills.",
        "next_step": "ask_technical_questions"
    },
    "ask_technical_questions": {
        "message": "",
        "next_step": "ask_technical_questions"
    },
    "conclusion": {
        "message": "Thank you for completing the screening process! Our team will review your information and get back to you soon. Have a great day!",
        "next_step": None
    }
}

# Technical questions database
TECH_QUESTIONS = {
    "python": [
        "What are Python decorators and how would you use them?",
        "Explain the difference between lists and tuples in Python.",
        "How does Python's garbage collection work?",
        "What are some ways to optimize Python code performance?",
        "Explain the Global Interpreter Lock (GIL) in Python."
    ],
    "javascript": [
        "What is the event loop in JavaScript?",
        "Explain the difference between let, const, and var.",
        "What are promises and how do they work?",
        "Describe the concept of hoisting in JavaScript.",
        "What are arrow functions and how do they differ from regular functions?"
    ],
    "java": [
        "Explain the difference between abstract classes and interfaces in Java.",
        "What is the Java Virtual Machine (JVM) and how does it work?",
        "Describe the concept of multithreading in Java.",
        "What are Java annotations and how would you use them?",
        "Explain the principles of object-oriented programming as implemented in Java."
    ],
    "react": [
        "What is the virtual DOM and how does it work in React?",
        "Explain the difference between state and props.",
        "What are React hooks and how do they work?",
        "Describe the component lifecycle in React.",
        "How would you optimize performance in a React application?"
    ],
    "node.js": [
        "What is the event-driven architecture in Node.js?",
        "How does Node.js handle asynchronous operations?",
        "Explain the concept of middleware in Express.js.",
        "What are streams in Node.js and how would you use them?",
        "How do you manage packages and dependencies in Node.js?"
    ],
    "sql": [
        "What are database indexes and how do they work?",
        "Explain the difference between INNER JOIN and LEFT JOIN.",
        "What is database normalization and why is it important?",
        "How would you optimize a slow SQL query?",
        "What are transactions and why are they important?"
    ],
    "aws": [
        "What are the key differences between S3 and EBS?",
        "Explain how Auto Scaling works in AWS.",
        "What is IAM and why is it important?",
        "Describe the difference between EC2 and Lambda.",
        "How would you design a highly available architecture on AWS?"
    ],
    "docker": [
        "What is the difference between a Docker image and a container?",
        "How does Docker manage networking between containers?",
        "What are Docker volumes and why are they important?",
        "Explain the Dockerfile instructions you use most frequently.",
        "How would you optimize a Docker image size?"
    ],
    "kubernetes": [
        "What is the difference between a deployment and a statefulset?",
        "How does Kubernetes handle service discovery?",
        "Explain the concept of namespaces in Kubernetes.",
        "What are liveness and readiness probes?",
        "How would you troubleshoot a pod that won't start?"
    ]
}

# Fallback responses for unexpected inputs
FALLBACK_RESPONSES = [
    "I'm here to help with the screening process. Could you please answer the question?",
    "Let's focus on the screening process for now. Could you provide the requested information?",
    "I'm designed to assist with candidate screening. Please answer the question so we can proceed.",
    "To make the most of our time, let's stick to the screening questions. Could you please respond accordingly?"
]

# Function to validate input
def validate_input(input_text, pattern):
    return re.match(pattern, input_text) is not None

# Function to generate technical questions based on tech stack
def generate_tech_questions(tech_stack):
    questions = []
    tech_list = [tech.strip().lower() for tech in tech_stack.split(",")]
    
    for tech in tech_list:
        # Find the best matching technology in our questions database
        matched_tech = None
        for known_tech in TECH_QUESTIONS.keys():
            if known_tech in tech or tech in known_tech:
                matched_tech = known_tech
                break
        
        if matched_tech and TECH_QUESTIONS.get(matched_tech):
            # Select 1-2 questions per technology
            num_questions = min(2, len(TECH_QUESTIONS[matched_tech]))
            selected_questions = random.sample(TECH_QUESTIONS[matched_tech], num_questions)
            questions.extend(selected_questions)
    
    # If no specific tech matched, use general questions
    if not questions:
        general_questions = [
            "What version control system do you prefer and why?",
            "Describe your experience with testing frameworks.",
            "How do you approach debugging complex issues?",
            "What development methodologies have you worked with?",
            "How do you stay updated with the latest technology trends?"
        ]
        questions = random.sample(general_questions, 3)
    
    return questions

# Function to handle conversation flow
def handle_conversation(user_input):
    current_step = st.session_state.current_step
    step_info = STEPS[current_step]
    
    # Handle conversation-ending keywords
    end_keywords = ["bye", "goodbye", "exit", "quit", "stop", "end"]
    if any(keyword in user_input.lower() for keyword in end_keywords):
        st.session_state.current_step = "conclusion"
        return STEPS["conclusion"]["message"]
    
    # Handle different steps in the conversation
    if current_step in ["get_name", "get_email", "get_phone", "get_experience", "get_position", "get_location", "get_tech_stack"]:
        field = step_info["field"]
        if validate_input(user_input, step_info["validation"]):
            st.session_state.candidate_info[field] = user_input
            st.session_state.current_step = step_info["next_step"]
            next_step_info = STEPS[st.session_state.current_step]
            return next_step_info["message"]
        else:
            return step_info["error_msg"]
    
    elif current_step == "generate_questions":
        # Generate technical questions based on tech stack
        tech_stack = st.session_state.candidate_info.get("tech_stack", "")
        st.session_state.tech_questions = generate_tech_questions(tech_stack)
        st.session_state.current_tech_index = 0
        st.session_state.current_step = "ask_technical_questions"
        
        if st.session_state.tech_questions:
            return f"Great! I have {len(st.session_state.tech_questions)} questions for you. Let's start with: {st.session_state.tech_questions[0]}"
        else:
            st.session_state.current_step = "conclusion"
            return "Thank you for your responses! We'll review your information and contact you soon."
    
    elif current_step == "ask_technical_questions":
        if st.session_state.current_tech_index < len(st.session_state.tech_questions) - 1:
            st.session_state.current_tech_index += 1
            next_question = st.session_state.tech_questions[st.session_state.current_tech_index]
            return next_question
        else:
            st.session_state.current_step = "conclusion"
            return STEPS["conclusion"]["message"]
    
    # Fallback for unexpected inputs
    return random.choice(FALLBACK_RESPONSES)

# Streamlit UI
def main():
    st.set_page_config(
        page_title="Talent Scout Hiring Assistant",
        page_icon="🤖",
        layout="centered"
    )
    
    st.title("Talent Scout Hiring Assistant 🤖")
    st.caption("Your intelligent recruitment screening chatbot")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Initial greeting
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            st.markdown(STEPS["greeting"]["message"])
        st.session_state.messages.append({"role": "assistant", "content": STEPS["greeting"]["message"]})
        st.session_state.current_step = "get_name"
    
    # User input
    if prompt := st.chat_input("Type your response here..."):
        # Add user message to chat history
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get bot response
        response = handle_conversation(prompt)
        
        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Display progress
    progress_steps = list(STEPS.keys())[:-2]  # Exclude the technical questions and conclusion steps
    current_progress = progress_steps.index(st.session_state.current_step) if st.session_state.current_step in progress_steps else len(progress_steps)
    st.progress(current_progress / len(progress_steps))
    
    # Show candidate info (for demo purposes)
    with st.expander("View Collected Information"):
        st.json(st.session_state.candidate_info)

if __name__ == "__main__":
    main()