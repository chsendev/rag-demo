# 使用llama-index来连接到Neo4j，以构建和查询知识图谱，将文档中的信息转化为知识图谱
from llama_index.graph_stores.neo4j import Neo4jGraphStore
from llama_index.core import KnowledgeGraphIndex

username = "neo4j-test"
password = "neo4j-test"

