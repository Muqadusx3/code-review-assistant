import streamlit as st
import os
from dotenv import load_dotenv
import openai
MAX_CHARS = 4000
def get_code_review(code, api_key, tone):
    openai.api_key = api_key
    if tone == 'Supportive':
        tone_instruction = "You are kind and encouraging code review assistant."
    elif tone == 'Direct':
        tone_instruction = "You are a blunt, no-fluff code reviewer. Be short and clear."
    elif tone == 'Humorous':
        tone_instruction = "You are a funny but helpful coach. Use a light and witty tone."
    else:
        tone_instruction = "You are a helpful and friendly code review assistant."
    prompt = f'''
    You are a helpful and friendly code review assistant.
    Please review the following code and provide feedback in three clearly labeled sections:
    1. Style: Comment on formatting, naming, and structure.
    2. Errors: Point out any bugs or logical errors.
    3. Clarity: Suggest ways to make the code easier to understand.
    here is the code:
    {code}
    '''
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message['content']
load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')
st.set_page_config(page_title="Code Review Assistant",layout="wide")
st.write("Key Loaded", api_key is not None)

st.title("Code Review Assistant")
st.write("Welcome to the Code Review Assistant! Upload your code files and get instant feedback.")  

col1,col2=st.columns([1,1])

with col1:
    st.subheader('Paste Your Code')
    code_input=st.text_area('Your Code Here',height=300)

with col2:
    st.subheader('Review Output')

if st.session_state.get('feedback'):
    st.markdown("### AI Code Review:")
    st.write(st.session_state['feedback'])
elif code_input:
    st.write("Review will appear here.")
else:
    st.info("Paste your code in the left box or upload a file to get started.")

uploaded_file=st.file_uploader('Or upload a code file',type=['py','js','java','cpp','txt'])
if uploaded_file:
    try:
        code_input=uploaded_file.read().decode('utf-8')
        st.code(code_input,language='python')
    except Exception as e:
        st.error("Could not read file: "+str(e))

tone = st.selectbox('Select Tone for Feedback', ['Supportive', 'Direct', 'Humorous'])

if st.button('Run Review'):
    if not code_input.strip():
        st.warning("Please provide some code to review.")
    elif len(code_input) > MAX_CHARS:
        st.error(f"Code exceeds maximum length of {MAX_CHARS} characters.")
    elif not api_key:
        st.error("API key is missing.")
    else:
        with st.spinner('Reviewing your code...'):
            try:
                feedback = get_code_review(code_input, api_key, tone)
                st.session_state['feedback'] = feedback
            except Exception as e:
                st.error("Error occurred while reviewing code: " + str(e))