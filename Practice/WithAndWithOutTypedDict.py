from langgraph.graph import StateGraph, END
from typing import TypedDict,Annotated
import operator

class WithStateReducer(TypedDict):
    history: Annotated[list, operator.add]
    message: str

def Node1(state:WithStateReducer):
    return {"history": ["Node1 ran"], "message": "Hello from Node1"}

class WithOutState():
    msg:str

def Node3(state:WithOutState):
    return {"msg":"Hello"}