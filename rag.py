from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_ollama.llms import OllamaLLM
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# 使用ollama服务
llm = OllamaLLM(model="qwen2:7b-instruct-q4_0")
template = """您是问答任务的助理。
使用以下检索到的上下文来回答问题。
如果你不知道答案，就说你不知道。
最多使用三句话，不超过100字，保持答案简洁。
Question: {question} Context: {context} Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
# 创建BAAI的embedding
rag_embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
# 从持久化目录加载向量数据库
vector_store = Chroma(persist_directory="./chroma_langchain_db", embedding_function=rag_embeddings)
# 获取 retriever
retriever = vector_store.as_retriever()


# 生成答案
def generate_answer(question):
    rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    resp = rag_chain.invoke(question)
    print(resp.replace("。", "。\n"))


query = "为什么需要自研trpc"
generate_answer(query)
