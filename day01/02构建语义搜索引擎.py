from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings


def demo1():
    # 使用document
    # 主要包含三个属性：page_content、metadata、id
    documents = [
        Document(
            page_content="Hello, world!",
            metadata={"source": "https://example.com"}
        ),
        Document(
            page_content="Hello, langchain!",
            metadata={"source": "https://langchain.com"}
        ),
    ]
    print(documents)


def demo2():
    # 加载pdf文档
    loader = PyPDFLoader("./nke-10k-2023.pdf")
    docs = loader.load()
    print(len(docs))
    print(f"{docs[0].page_content[:200]}\n")
    print(docs[0].metadata)


def demo3():
    # 基于文本结构拆分
    loader = PyPDFLoader("./nke-10k-2023.pdf")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    len(all_splits)


def demo4():
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
    vector_1 = embeddings.embed_query("hello world")
    vector_2 = embeddings.embed_query("hello langchain")
    assert len(vector_1) == len(vector_2)
    print(f"Generated vectors of length {len(vector_1)}\n")
    print(vector_1[:10])


if __name__ == '__main__':
    # demo1()
    # demo2()
    # demo3()
    demo4()
