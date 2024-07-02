import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Set title
st.title('My Chatbot')

# Generating chatbot response
def generate_response(prompt_input, email, pwd):
    # Login to HuggingFace
    sign = Login(email, pwd)
    cookies = sign.login()
    # Create ChatBot                        
    bot = hugchat.ChatBot(cookies=cookies.get_dict())
    return bot.chat(prompt_input)

# Login to HuggingFace
with st.sidebar:
    st.title('Login HugChat')
    hf_email = st.text_input('Enter E-mail:')
    hf_pass = st.text_input('Enter Password:', type='password')
    if not (hf_email and hf_pass):
        st.warning('Please login to your account!')
    else:
        st.success('Proceed to entering your prompt message')

# Store chatbot generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Welcome ! I'm glad to be your assistant !"}]

# Output bot responses
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Prompt from user
if prompt := st.chat_input(disabled = not(hf_email and hf_pass)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Generating..."):
            response = generate_response(prompt, hf_email, hf_pass) 
            st.write(response) 
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)