from env import * 
from neo4j import GraphDatabase
from pydantic import BaseModel
from openai import OpenAI

driver = GraphDatabase.driver("bolt://localhost:7687", auth=(GRAPH_USERNAME, GRAPH_PASSWORD))
client = OpenAI(api_key=OPENAI_KEY)
