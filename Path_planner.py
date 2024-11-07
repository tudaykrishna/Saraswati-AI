from langchain_google_vertexai import VertexAI
from langchain_ollama import ChatOllama
import vertexai
# from langchain_google_vertexai import ChatVertexAI
import streamlit as st

st.title("Path Planner")
# vertexai.init(project="acc", location="us-central1")
# model  = VertexAI(model_name="gemini-pro", convert_system_message_to_human=True)

model = ChatOllama(model="llama3.2",temperature=0.01)

import streamlit as st

from langchain_core.messages import HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools import YouTubeSearchTool
from langchain_core.prompts import PromptTemplate
from youtube_search import YoutubeSearch

def format_headers(text):
    lines = text.split("\n")
    formatted_text = ""
    for line in lines:
        if line.startswith("#:"):
            formatted_text += f"# {line.replace('#', '')}\n"
        elif line.startswith("#"):
            formatted_text += f"# {line.replace('#', '')}\n"
        # elif line.startswith("Time Required:"):
        #     formatted_text += f"# {'Time Required:'}\n"
        # elif line.startswith("Difficulty Level:"):
        #     formatted_text += f"# {'Difficulty Level:'}\n"
        elif line.startswith("**"):
            formatted_text += f"### {line.replace('**', '')}\n"
        else:
            formatted_text += f"{line}\n"
    return formatted_text

api_key = "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"
search = TavilySearchAPIWrapper(tavily_api_key=api_key)

if 'answer1' not in st.session_state:
    st.session_state['answer1'] = []
if 'user1' not in st.session_state:
    st.session_state['user1'] = []
st.header("Path Planner")
topic12 = st.text_input("Enter topic name:")

    

if 'linky' not in st.session_state:
    st.session_state['linky'] = []
if 'linkt' not in st.session_state:
    st.session_state['linkt'] = []

template1 = """     
            "You are a helpful AI assistant, You are a  course planner for user's input course.  Explanation should be about 3 pages long"
            " you also get taviely websearch content and links if provided - {taviely}"
            " you also get provide youtube links - {youtube}"
            "Don;t mention anything about yourself and just give the content based on user's question"
            User's input - {question}
            
        """


prompt = PromptTemplate(
    template=template1,input_variables=['question','taviely','youtube']
)

chain = prompt | model

@st.cache_data
def invoke_api1(topic12):
    inputs = {"question": [HumanMessage(content=topic12)],'youtube':st.session_state['linky'][-1],'taviely':st.session_state['linkt'][-1]}
    response = chain.invoke(inputs)
    # Call the API to get the response
    return response



    
@st.cache_data
def fr(topic12):
    if topic12:
        
        st.session_state['user1'].append(topic12)
        tool1 = YouTubeSearchTool()
        rtt = topic12 + "," + "3"
        re3  = tool1.run(rtt)
        st.session_state['linky'].append(re3)
        re4 =  TavilySearchResults(api_wrapper=search,max_results=3).run(topic12)
        st.session_state['linkt'].append(re4)
        
        provided_text =  invoke_api1(st.session_state['user1'][-1])
        
        formatted_text = format_headers(provided_text)
        
        
        st.session_state['answer1'].append(formatted_text)
        
        st.markdown(st.session_state['answer1'][-1])
        
fr(topic12)
