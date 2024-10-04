import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Set up your Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Configure Streamlit layout
st.set_page_config(page_title="HopeBot", layout="wide")

# Sidebar with additional information and collapsible sections
with st.sidebar:
    st.title("🤖 About the Chatbot")
    st.markdown(
        """
        This is a **Mental Health Support Chatbot** designed to provide a friendly and supportive conversation experience. 
        Feel free to ask any questions or share your thoughts, and the chatbot will respond in a compassionate and understanding manner.
        """
    )
    st.markdown("---")  # A horizontal line for separation

    # Modern styled collapsible sections with catchy phrases and icons
    sections = {
        "🎮 Games": ("Play and unwind with exciting games!", "https://poki.com/"),
        "🏃‍♂️ Exercise": ("Get moving and feel great!", "https://www.healthline.com/health/depression/exercise"),
        "🥗 Diet": ("Tasty tips for a healthier you!", "https://www.verywellmind.com/what-you-eat-can-have-an-effect-on-your-overall-mental-well-being-5209290"),
        "🎨 Creativity": ("Unleash your creativity now!", "https://www.skillshare.com/en/browse/design"),
        "🧘 Meditation": ("Find calm with quick meditation!", "https://www.artofliving.org/in-en/meditation/guided/relaxing-music-meditation")
    }

    for section, (phrase, link) in sections.items():
        with st.expander(section, expanded=False):
            st.write(phrase)
            st.markdown(f'<a href="{link}" target="_blank" style="color: #1e90ff;">🖱️ Tap Here</a>', unsafe_allow_html=True)

# Title and description
st.image("images/HopeBot.png", width=100)
st.title("HopeBot")
st.write("I'm here to help you. Feel free to ask me anything!")

# Initialize the session state to store the chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Custom styling for GPT-like UI
st.markdown(
    """
    <style>
    .chat-container {
        display: flex;
        flex-direction: column;
        height: 80vh;
        margin-bottom: 50px; /* Space for the input area */
    }

    /* Scrollable chat history container */
    .chat-history {
        flex: 1;
        overflow-y: auto;
        padding: 10px;
        border-radius: 5px;
        background-color: #ffffff;
    }

    /* Message bubbles */
    .user-message {
        text-align: right;
        color: #212121;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 10px;
        display: inline-block;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
    }

    .bot-message {
        text-align: left;
        color: #212121;
        background-color: #fff;
        padding: 10px;
        border-radius: 10px;
        display: inline-block;
        margin: 5px 0;
        max-width: 80%;
        word-wrap: break-word;
    }

    /* Input area */
    .fixed-input {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f4f4f4;
        padding: 10px 0;
        box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .input-text {
        flex: 1;
        border-radius: 5px;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ddd;
    }

    .input-button {
        border-radius: 5px;
        background-color: #2f2f2f;
        color: white;
        padding: 10px;
        font-size: 16px;
        cursor: pointer;
        border: none;
    }

    .input-button:hover {
        background-color: #ddd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display chat history in a scrollable container
st.markdown("### Chat History:")
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-history">', unsafe_allow_html=True)
    for speaker, message in st.session_state.history:
        if speaker == "You":
            st.markdown(
                f"<div class='user-label'>{speaker}</div><div class='user-message'>{message}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='bot-label'>🤖 HopeBot</div><div class='bot-message'>{message}</div>",
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Function to send message when enter key is pressed or button is clicked
def send_message():
    if st.session_state.user_input:
        # Process user input
        statement = f'"{st.session_state.user_input}" you are a mental support health chatbot so answer the quoted in a polite and friendly way it chats just like how a psychiatrist talks it should be humanized .'
        response = model.generate_content(statement)

        # Update chat history with the user input and chatbot response
        st.session_state.history.append(("You", st.session_state.user_input))
        st.session_state.history.append(("HopeBot", response.text))

        # Clear input box after sending
        st.session_state.user_input = ""

# Input area at the bottom
st.markdown('<div class="fixed-input">', unsafe_allow_html=True)
with st.container():
    input_col1, input_col2 = st.columns([5, 1])
    
    with input_col1:
        st.text_input("You:", key="user_input", label_visibility="collapsed", on_change=send_message)
        
    with input_col2:
        st.button("Send", on_click=send_message, key="send_button")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align: center; color: grey;'>"
    "You're doing great. Keep going and stay positive! ✨</div>",
    unsafe_allow_html=True,
)
