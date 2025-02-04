from env import * 
from neo4j import GraphDatabase
from pydantic import BaseModel
from openai import OpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

from tool import *


driver = GraphDatabase.driver("bolt://localhost:7687", auth=(GRAPH_USERNAME, GRAPH_PASSWORD))
client = OpenAI(api_key=OPENAI_KEY)
model = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_KEY)
checkpointer = MemorySaver()

tools = [style_check, security_check, performance_check]
app = create_react_agent(model, tools=tools, checkpointer=checkpointer)
