#Why do we need docstring here?
# 1.A docstring (documentation string) is a special text written inside triple quotes """...""" placed right after a function, class, or module definition. It describes what the code does.
# 2.Docstrings serve three main audiences, each with their own purpose:
    # - For developers: They provide a clear explanation of what the function/class/module does, its parameters, return values, and any exceptions it might raise. This helps other developers (or your future self) understand the code quickly without having to read through the implementation details.
    # -IDEs and tools Show tooltips, autocomplete help() command works
    # -LLMs and AI agents Decide which tool to call Most important for you!  Without docstring LLM does not know what tool does @tool decorator throws an error Agent cannot choose correctly
# 3.For LLM tools, docstrings are 100% MANDATORY ✅

#What is create_react_agent?
# It is Prebuilt Agent Template.
    # React=Reason + Act
        # 1.Reason- Thinks what to do
        # 2.Act- It calls tools 
        # 3.Observe- It Observe Result (Learning)
        # 4.Repeats untill tas is Complete
#🛠️ Automatically handles tool calling, results, and final answers
#It Implements REACT Pattern(Reason → Act → Observe → Repeat)

#  Step-StepWhat Happens
# 1.Receives your question
# 2.Sends question + tool descriptions to LLM
# 3.LLM decides which tool to call (or none)
# 4.Executes the tool with chosen arguments
# 5.Sends result back to LLM
# 6.LLM decides: more tools needed OR final answer
# 7.Returns complete conversation history

#What is messages dict and Humanmessage Object inside agent.invoke?
# 1.messages-: Because create_react_agent is desigend look for conversation history under "messages" key.
#   ..Conversation can have multiple back and forth intercations like below.
#               "messages": [
#                HumanMessage(content="My name is John"),      # User asked
#                AIMessage(content="Nice to meet you, John!"),               # AI replied
#                   HumanMessage(content="What's my name?"), # User again Now Agent will remember "John"
#   ]
# 2.HumanMessage-: This is an LangChain message Object which tells LLM this is from Human User.
# 3.There are 4 message types in LangChain:
#     - HumanMessage: From user (Yor input to agent)
#     - AIMessage: From AI (LLM's Response)
#     - SystemMessage: Instructions for AI (like "You are a helpful assistant") (Tells LLM how to behave)
#     - ToolMessage: When tool is called, it can also be part of messages history. (Results from tool calls)
# ***System Message Example:***
#                   result = agent.invoke({
#                           "messages": [
#                        SystemMessage(content="You are a math teacher. Explain steps clearly."),
#                        HumanMessage(content="What is 5 * 10?")
#                   ]
#                }) # Now agent will respond like a teacher with step-by-step explanation


from ast import For

from langchain_core import tools
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq


load_dotenv() # Load environment variables from .env file

# Here Am using generic name to function with No association with DocString and Operation it performs. See Result and how DOCstring helps LLM.
#The LLM ignored the actual tool result (-5) because the docstring promised multiplication. It used the expected result (50), not the actual result.
# The LLM never used -5! from Calca function It "imagined" the answer was 50 based on the docstring promise.

# @tool 
# def Calca(a:int ,b:int)->int:
#     """Multiplies two numbers and returns the result.""" #Why do we need docstring here?
#     return a-b

# @tool 
# def Calc(a:int,b:int)->int:
#     """Adds two numbers and returns the result."""
#     return a+b
@tool
def Multiply(a:int ,b:int)->int:
    """Multiplies two numbers and returns the result.""" #Why do we need docstring here?
    return a*b

@tool 
def Add(a:int,b:int)->int:
    """Adds two numbers and returns the result."""
    return a+b
llm = ChatGroq(model="llama-3.3-70b-versatile") #Add GROQ_API_KEY under.env file while program execution.
agent=create_react_agent(llm,tools=[Multiply,Add ]) #what is create_react_agent?

result=agent.invoke({"messages":[HumanMessage(content="Calculate 5 multiplied by 10 and then add 20 to the result") ]}) #What is message Format here ?

# print(result)

print(result["messages"][-1].content)

#Each Steps of Agents Execution
for msg in result["messages"]:
    msg.pretty_print()
               
# You ask a question
#       ↓
#    LLM thinks
#       ↓
#    calls tool       ← multiply(47, 83)
#       ↓
#    reads result     ← 3901
#       ↓
#    calls tool       ← add(3901, 22)
#       ↓
#    reads result     ← 3923
#       ↓
#    LLM decides: done, no more tools needed
#       ↓
#    returns answer   ← "The answer is 3923"