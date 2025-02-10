import streamlit as st
import google.generativeai as genai
import base64
import os
from dotenv import load_dotenv

# Configure API Key
API_KEY = st.secrets["API_KEY"]

if not API_KEY:
    st.error("API Key is missing. Please check your Streamlit secrets.")
    st.stop()


# Load the Credit Policy Markdown file
def load_credit_policy(file_path):
    """Loads credit policy text from a file, or returns a default message if missing."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    return "No credit policy found. Please upload a policy document."

# Function to set background image
def set_background(image_path):
    """Sets the background image for the Streamlit app."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{encoded_string});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.7);
                z-index: -1;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Initialize Gemini Model
model = genai.GenerativeModel("gemini-pro")

# Function to Ask Questions
def ask_gemini(question, credit_policy_text):
    """Sends a question with the credit policy text to Gemini for a response."""
    prompt = f"Use the following credit policy document to answer the question:\n\n{credit_policy_text}\n\nQuestion: {question}"
    response = model.generate_content(prompt)
    return response.text if response else "Sorry, I couldn't generate a response."

# Enhanced CSS with modern design elements
def load_css():
    """Creates and loads custom CSS for modern dark theme."""
    css_content = """
    /* Modern Dark Theme for Credit Policy Chatbot */
    :root {
        --background-dark: #121212;
        --background-light: #1E1E1E;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
        --accent-color: #BB86FC;
        --user-message-bg: #2C2C2C;
        --bot-message-bg: #1E1E1E;
        --gradient-primary: linear-gradient(135deg, #BB86FC 0%, #9C27B0 100%);
        --gradient-secondary: linear-gradient(135deg, #3a1c71, #d76d77, #ffaf7b);
    }

    /* Global Styles */
    .stApp {
        background-color: var(--background-dark) !important;
        color: var(--text-primary) !important;
    }

    /* Main Title */
    .main-title {
        background: var(--gradient-secondary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 2.8em;
        margin: 30px 0;
        font-weight: 700;
        letter-spacing: 1px;
        animation: titleGlow 3s ease-in-out infinite;
    }

    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 30px rgba(187, 134, 252, 0.3); }
        50% { text-shadow: 0 0 50px rgba(187, 134, 252, 0.5); }
    }

    /* Chat Messages */
    .user-message, .bot-message {
        color: var(--text-primary) !important;
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 15px;
        max-width: 85%;
        line-height: 1.6;
        box-shadow: 0 2px 15px rgba(0,0,0,0.2);
        animation: fadeIn 0.3s ease-in;
        position: relative;
    }

    .user-message {
        background: var(--gradient-secondary) !important;
        align-self: flex-end;
        margin-left: auto;
        border-bottom-right-radius: 5px;
    }

    .bot-message {
        background: linear-gradient(145deg, #1E1E1E, #2C2C2C) !important;
        border: 1px solid rgba(187, 134, 252, 0.3);
        align-self: flex-start;
        margin-right: auto;
        border-bottom-left-radius: 5px;
    }

    /* Message Icons */
    .message-icon {
        position: absolute;
        top: -10px;
        width: 25px;
        height: 25px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }

    .user-icon {
        right: -10px;
        background: var(--gradient-secondary);
    }

    .bot-icon {
        left: -10px;
        background: var(--gradient-primary);
    }

    /* Enhanced Select Box with Full Visibility Fix */
    .stSelectbox {
        margin-bottom: 20px;
    }

    .stSelectbox > div > div {
        background-color: var(--background-light) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--accent-color) !important;
        border-radius: 12px !important;
        min-height: 45px !important;
        padding: 5px 10px !important;
        width: 100% !important;
        position: relative;
        z-index: 1;
    }

    .stSelectbox > div > div > div {
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
        align-items: center;
        min-height: 45px;
    }

    div[data-baseweb="popover"] {
        background-color: var(--background-light) !important;
        border: 2px solid var(--accent-color) !important;
        border-radius: 12px !important;
        margin-top: 5px;
    }

    div[data-baseweb="popover"] ul {
        background-color: var(--background-light) !important;
        padding: 5px !important;
    }

    div[data-baseweb="popover"] li {
        color: var(--text-primary) !important;
        padding: 10px !important;
        border-radius: 8px !important;
        transition: background-color 0.2s ease;
    }

    div[data-baseweb="popover"] li:hover {
        background-color: rgba(187, 134, 252, 0.2) !important;
    }

    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: rgba(187, 134, 252, 0.3) !important;
    }

    /* Input Field */
    .stTextInput > div > div > input {
        color: var(--text-primary) !important;
        background-color: var(--background-light) !important;
        border: 2px solid var(--accent-color) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 10px rgba(187, 134, 252, 0.5) !important;
    }

    /* Enhanced Button Styles */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(187, 134, 252, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(187, 134, 252, 0.4) !important;
    }

    /* Sidebar */
    .sidebar-content {
        padding: 20px;
        background: rgba(30, 30, 30, 0.9);
        border-radius: 15px;
        margin: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border: 1px solid rgba(187, 134, 252, 0.1);
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    """
    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="Credit Policy Assistant",
        page_icon="✨",
        layout="wide"
    )

    # Load CSS
    load_css()

    # Try to set background
    set_background("background.png")

    # Display logo and title
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("msfincap.png", width=250)
        st.markdown("<h1 class='main-title'>✨ Credit Policy Assistant</h1>", unsafe_allow_html=True)

    # Sidebar with enhanced UI
    with st.sidebar:
        st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        st.header("🎯 Chat Controls")

        # Enhanced select box with better visibility
        mode = st.selectbox(
            "💫 Conversation Mode",
            options=["Standard", "Detailed", "Concise"],
            index=0,
            help="Choose how detailed you want the responses to be",
            key="conversation_mode"
        )

        if st.button("🔮 Reset Conversation"):
            st.session_state.messages = []
            st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Load credit policy
    credit_policy_text = load_credit_policy("Credit_Policy2.md")

    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "✨ Hello! I'm your Credit Policy Assistant. How can I help you today?"
            }
        ]

    # Chat container
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(
                    f"""<div class='user-message'>
                        <div class='message-icon user-icon'>👤</div>
                        <strong>You:</strong> {message['content']}
                    </div>""", 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""<div class='bot-message'>
                        <div class='message-icon bot-icon'>🤖</div>
                        <strong>Assistant:</strong> {message['content']}
                    </div>""", 
                    unsafe_allow_html=True
                )

    # Chat input
    user_query = st.chat_input("💭 Ask about the credit policy...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})

        additional_prompt = {
            "Concise": " Please provide a very brief and to-the-point answer.",
            "Detailed": " Please provide a comprehensive and detailed explanation.",
            "Standard": ""
        }.get(mode, "")

        with st.spinner("✨ Analyzing policy..."):
            response = ask_gemini(user_query + additional_prompt, credit_policy_text)

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

if __name__ == "__main__":
    main()
