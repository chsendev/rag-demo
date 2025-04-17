from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor
)
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 加载ollama模型
llm = Ollama(model="qwen2:7b-instruct-q4_0")
# 加载embedding模型
rag_embeddings = HuggingFaceEmbedding(model_name="BAAI/bge-small-zh-v1.5", cache_folder="./model")

# 读取文档
documents = SimpleDirectoryReader(input_files=["./tRPC项目介绍.txt"]).load_data()

# 定义文本分割器配置
# 使用句号作为分隔符，每个chunk最大512个token，重叠128个token
text_splitter = TokenTextSplitter(
    separator="。", chunk_size=512, chunk_overlap=128
)

# 对每个节点生成5个标题
title_extractor = TitleExtractor(nodes=5, llm=llm)
# 对每个节点生成3个相关问题
qa_extractor = QuestionsAnsweredExtractor(questions=3, llm=llm)

# 提取节点
pipeline = IngestionPipeline(
    transformations=[text_splitter, title_extractor, qa_extractor]
)

nodes = pipeline.run(
    documents=documents,
    in_place=True,
    show_progress=True,
)

print(nodes)

# 保存到chromadb
chroma_client = chromadb.PersistentClient(path="./chroma_llama_index_db")
# 创建集合，相当于数据库中的表
chroma_collection = chroma_client.create_collection("my_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=rag_embeddings)
print("数据已存入向量数据库")
