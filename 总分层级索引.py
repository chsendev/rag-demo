from llama_index.core import SummaryIndex, SimpleDirectoryReader
from llama_index.core.async_utils import run_jobs
from llama_index.llms.openai import OpenAI
from llama_index.core.schema import IndexNode
from llama_index.core.schema import Document
from llama_index.core.vector_stores import (
    FilterOperator,
    MetadataFilter,
    MetadataFilters
)
from llama_index.llms.ollama import Ollama

llm = Ollama(model="qwen2:7b-instruct-q4_0")


async def aprocess_doc(doc: Document, include_summary: bool = True):
    metadata = doc.metadata

    data_tokens = metadata["created_at"].split("T")[0].split("-")
    year = int(data_tokens[0])
    month = int(data_tokens[1])
    day = int(data_tokens[1])

    assignee = (
        "" if "assignee" not in doc.metadata else doc.metadata["assignee"]
    )
    size = ""
    if len(doc.metadata["labels"]) > 0:
        size_arr = [l for l in doc.metadata["labels"] if "size:" in l]
        size = size_arr[0].split(":")[1] if len(size_arr) > 0 else ""
        new_metadata = {
            "state": metadata["state"],
            "year": year,
            "month": month,
            "day": day,
            "assignee": assignee,
            "size": size,
        }

        # 提取文档总结摘要
        summary_index = SummaryIndex.from_documents([doc])
        query_str = "Give a one-sentence concise summary of this issue."
        query_engine = summary_index.as_query_engine(
            llm=llm
        )
        summary_txt = await query_engine.query(query_str)
        summary_txt = str(summary_txt)

        index_id = doc.metadata["index_id"]
        # 通过doc id过滤出对应的文档
        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key="index_id",
                    operator=FilterOperator.EQ,
                    value=int(index_id)
                )
            ]
        )

        # 创建的一个索引节点，包括有元数据和摘要总结文本
        index_node = IndexNode(
            text=summary_txt,
            metadata=new_metadata,
            obj=doc,
            index_id=doc.id_
        )
        return index_node


async def aprocess_docs(docs: list[Document]):
    index_nodes = []
    tasks = []
    for doc in docs:
        task = aprocess_doc(doc)
        tasks.append(task)
    index_nodes = await run_jobs(tasks, show_progress=True, workers=3)

    return index_nodes

documents = SimpleDirectoryReader(input_files=["./tRPC项目介绍.txt"]).load_data()
