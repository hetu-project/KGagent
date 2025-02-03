from env import * 
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=(GRAPH_USERNAME, GRAPH_PASSWORD))
