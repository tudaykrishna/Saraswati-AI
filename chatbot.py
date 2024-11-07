from langgraph.graph import START
from langchain_core.messages import HumanMessage , AIMessage
from langchain_google_vertexai import ChatVertexAI
from langchain_ollama import ChatOllama
import vertexai

# vertexai.init(project="codeignite", location="us-central1")
  
# model = ChatVertexAI(model_name="gemini-pro",temperature=0.01)

model = ChatOllama(model="llama3.2",temperature=0.01)


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are AI assistant chatbot . You can use emoji's if you want but don't use every time . Give the concise content. ",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

workflow = StateGraph(state_schema=MessagesState)


def call_model(state: MessagesState):
    chain = prompt | model
    response = chain.invoke(state)
    return {"messages": response}


workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

conn = sqlite3.connect("History.sqlite",check_same_thread=False)

memory = SqliteSaver(conn)
app = workflow.compile(checkpointer=memory)



# -------------------------------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
from streamlit_chat import message


import streamlit as st
from streamlit_chat import message
from langchain.schema import HumanMessage

query = st.chat_input("Type your message here...")

col1, col2 ,col3 = st.columns([6, 1, 2])
with col1:
    st.title("Chat with Saraswati-AI")
Users = ["User1", "User2", "User3" ,"👤Create User"]
with col3:
    option = st.selectbox(
        "",
        options=Users
    )


if query:
    # Display user's query on the chat UI
    message(query, is_user=True)
    config = {"configurable": {"thread_id": option}}



    # Append user's message to the chat history
    input_messages = [HumanMessage(query)]
    
    # Get the app response
    output = app.invoke({"messages": input_messages}, config)

    # Extract the response content
    response = output["messages"][-1].content

    # Display the app's response in the chat UI
    message(response)








