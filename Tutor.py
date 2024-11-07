import streamlit as st
import json
from langchain_core.prompts import PromptTemplate
# from langchain.chains import LLMChain
from langchain_google_vertexai import VertexAI
import vertexai
vertexai.init(project="acc", location="us-central1")
  
model = VertexAI(model_name="gemini-pro")

st.title("Galileo AI 🤖")

if 'depth' not in st.session_state:
    st.session_state['depth'] = 'Elementary (Grade 1-6)'

if 'Learning' not in st.session_state:
    st.session_state['Learning'] = 'Verbal'

if 'Tone' not in st.session_state:
    st.session_state['Tone'] = 'Encouraging)'
if 'Reasoning' not in st.session_state:
    st.session_state['Reasoning'] = 'Deductive'

st.session_state['depth'] = st.sidebar.selectbox(
    "Depth",
    ("Elementary (Grade 1-6)", "Middle School (Grade 7-9)", "Highschool (10-12)","College Prep","Undergraduate","Graduate")
)
st.session_state['Learning'] = st.sidebar.selectbox(
    "Learning Styles",
    ("Verbal", "Active", "Intuitive)","Reflective","Global")
)

st.session_state['Tone'] = st.sidebar.selectbox(
    "Tone Styles",
    ("Encouraging", "Neutral", "Informative","Friendly","Humorous")
)
st.session_state['Reasoning'] = st.sidebar.selectbox(
    "Reasoning Frameworks",
    ("Deductive", "Inductive", "Abductive","Analogical","Causal")
)

#Template

template = """
.
You are an AI Tutor assistant. your name is Galileo. Strict rule is that always don't greet user . just focus on conversation and content . Your goal is to have a friendly, helpful, and engaging conversation with the human to help them learn about the topic they want to study.

Then, based on the human's input about what they want to learn, you will provide a comprehensive and conversational tutorial, guiding them through the topic step-by-step.

Your responses should be tailored to the human's profile and learning style, and you should aim to make the interaction feel natural and interactive, as if you were a knowledgeable tutor teaching a student.

Please generate a response that demonstrates this conversational tutoring approach. YOu also move forward based on User personalization learning - 

Depth - {depth} , Learning Styles - {learning} , Tone Styles - {tone} , Reasoning Framework - {reasoning}
Previous conversation:
{chat_history}


New human question: {question}
Response:"""


prompt = PromptTemplate(
    template=template,input_variables=['question','chat_history','depth','learning','tone','reasoning']
)
chain = prompt | model

@st.cache_data
def conversation_chat(query):
    result = chain.invoke({"question": query,'chat_history':st.session_state['history1'],'depth':st.session_state['depth'],'learning':st.session_state['Learning'],'tone':st.session_state['Tone'],'reasoning':st.session_state['Reasoning']})
    st.session_state['history1'].append((st.session_state['past1'][-1], st.session_state['generated1'][-1]))
    
    
    return result

def initialize_session_state():

    if 'generated1' not in st.session_state:
        st.session_state['generated1'] = ["Hello! Ask me anything about 🤗"]
    if 'past1' not in st.session_state:
        st.session_state['past1'] = ["hey"]
    if 'history1' not in st.session_state:
        st.session_state['history1'] = []

def display_chat_history():

    with st.form(key='my_form', clear_on_submit=False):
        user_input = st.text_input("Question:", placeholder="Your Query", key='input122')

        configure = st.sidebar.button('configure')
        submit_button = st.form_submit_button(label='Send')
        st.session_state['past1'].append(user_input)

    if (submit_button and user_input) or (configure and user_input):
        output = conversation_chat(user_input)
    
        
        st.session_state['generated1'].append(output)
        
        
            

        st.write(st.session_state['generated1'][-1])


initialize_session_state()

display_chat_history()