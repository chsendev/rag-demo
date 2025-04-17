# 准备知识库数据，建立索引
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 准备知识库数据，建索引
def prepare_data():
    file_path = "./tRPC项目介绍.txt"
    loader = TextLoader(file_path, encoding='utf-8')
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(chunks[0].page_content)
    return chunks


# embedding 知识库，保存到向量数据库
def embedding_data(chunks):
    # 创建BAAI的embedding
    rag_embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    # embed保存知识到向量数据库
    vector_store = Chroma.from_documents(documents=chunks, embedding=rag_embeddings,
                                         persist_directory="./chroma_langchain_db")
    return vector_store
