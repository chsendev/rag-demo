from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

model = init_chat_model("qwen2:7b-instruct-q4_0", model_provider="ollama")


def demo1():
    messages = [
        SystemMessage("请将以下内容翻译成英文"),
        HumanMessage("你好"),
    ]
    resp = model.invoke(messages)
    """
    除了以上的方式外，还支持以下方式
    cache.invoke("Hello")
    cache.invoke([{"role": "user", "content": "Hello"}])
    cache.invoke([HumanMessage("Hello")])
    """
    print(resp)


# 流式调用大模型
def demo2():
    for token in model.stream("hello"):
        print(token.content, end="\n")


# 使用消息模板
def demo3():
    system_template = "请将以下内容翻译成{lang}"
    prompt_template = ChatPromptTemplate(
        [("system", system_template), ("user", "{text}")]
    )
    prompt = prompt_template.invoke({"lang": "英文", "text": "你好"})
    print(prompt.to_messages()) # [SystemMessage(content='请将以下内容翻译成英文', additional_kwargs={}, response_metadata={}), HumanMessage(content='你好', additional_kwargs={}, response_metadata={})]
    resp = model.invoke(prompt)
    print(resp.content)


if __name__ == '__main__':
    # demo1()
    # demo2()
    demo3()
