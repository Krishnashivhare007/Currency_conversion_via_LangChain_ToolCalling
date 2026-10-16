from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
import requests
from dotenv import load_dotenv

load_dotenv()

@tool
def multiply(a:int,b:int)->int:
    """Given 2 numbers a and b this tool return their product"""
    return a * b

# print(multiply.invoke({"a":3,"b":4}))


# Tool bind

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

llm_with_tools = llm.bind_tools([multiply])

# print(llm_with_tools.invoke("hi"))

result2 = llm_with_tools.invoke("can you multiply 3 with 10")#ye khudse call nhi krega just suggestion dega ki aise kr skte 

# Tool execution
# print(multiply.invoke(result2.tool_calls[0]["args"]))

# Tool Message
# print(multiply.invoke(result2.tool_calls[0]))

query = HumanMessage("can you multiply 3 with 10")

mesages = [query]

result = llm_with_tools.invoke(mesages)

mesages.append(result)

mesages.append(multiply.invoke(result.tool_calls[0]))

print(mesages)

print(llm_with_tools.invoke(mesages).content)# ye poora response dega