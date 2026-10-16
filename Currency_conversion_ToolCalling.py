from langchain_community.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import InjectedToolArg
from typing import Annotated
from dotenv import load_dotenv
import requests

load_dotenv()

@tool
def get_conversion_factor(base_currency:str,target_currency:str)->float:
    """
    This function fetches the currency conversion factor between a given base currency and a target currency
    """
    url = f'https://v6.exchangerate-api.com/v6/ee66a527a76b1de9eda24427/pair/{base_currency}/{target_currency}'

    response = requests.get(url)

    return response.json()['conversion_rate']

# print(get_conversion_factor.invoke({'base_currency':'USD','target_currency':'INR'}))

@tool
def convert(base_currency:int, conversion_rate:Annotated[float,InjectedToolArg])->float: #Annotated[float,InjectedToolArg] isse hmne use ki hallucination se bchne k liye taaki llm koi random value na assume krle conversion rate ki vo hmm hi denge ise bss.
    """
    Given a currency conversion rate this function calculates the target currency value from a given base currency value
    """

    return base_currency*conversion_rate

# Binding

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

llm_with_tools = llm.bind_tools([get_conversion_factor,convert])

messages = [HumanMessage('What is the conversion factor between USD and INR, and based on that can you convert 10 usd to inr')]

# 1st tool calling
ai_message = llm_with_tools.invoke(messages)

messages.append(ai_message)# ye dena jaroori h
# LLM history padh kar hi aage ka answer sochta hai. Agar aap seedhe ToolMessage daal denge, toh LLM confuse ho jayega ki "Maine toh koi tool run karne ko kaha hi nahi tha, toh ye result achanak kahan se aa gaya?" Isse context break hota hai aur aksar API error throw karti hai ya LLM galat answer (hallucination) dene lagta hai.

# for tool_call in ai_message.tool_calls:# filhall ek hi tool aa rha hmare pass to ise use nhi kro
#     print(tool_call)

tool_message1 = get_conversion_factor.invoke(ai_message.tool_calls[0])

messages.append(tool_message1)

# 2nd tool calling
ai_message2 = llm_with_tools.invoke(messages)

messages.append(ai_message2)

ai_message2.tool_calls[0]['args']['conversion_rate'] = float(tool_message1.content)

tool_message2 = convert.invoke(ai_message2.tool_calls[0])

messages.append(tool_message2)

# tool execution
result = llm_with_tools.invoke(messages)

print(result.content)