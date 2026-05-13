from langgraph.graph import StateGraph, END
from typing import TypedDict


class State (TypedDict):
    score:int
    result:str

def evaluate(state): return {"score": state["score"]}

def approve(state): return {"result":"APPROVED"}
def review(state): return {"result":"NEEDS REVIEW"}
def reject(state): return {"result":"REJECTED"}

def router(state):
       if state["score"] >= 80:
          return "approve1"
       elif state["score"] >= 50:
        return "review1"
       else:
        return "reject1"
       

graph=StateGraph(State)
graph.add_node("evaluate", evaluate)
graph.add_node("approve_node", approve)
graph.add_node("review_node", review)
graph.add_node("reject_node",reject)

graph.set_entry_point("evaluate")     # graph STARTS at preprocess
graph.add_conditional_edges("evaluate",    # routing happens AFTER evaluate
        router,
    {
       "approve1":"approve_node",
       "review1":"review_node", 
        "reject1":"reject_node"
    }
)

graph.add_edge("approve_node", END)
graph.add_edge("review_node", END)
graph.add_edge("reject_node", END)

app=graph.compile();
result =app.invoke({"score": 90, "result": ""})
print(result)
                            


#Different Node on Set_Entry_Point and Conditional_Edges First Param (Node)
# from langgraph.graph import StateGraph, END
# from typing import TypedDict

# class State(TypedDict):
#     score: int
#     result: str

# # Node 1 — entry point (just prepares data)
# def preprocess(state):
#     print("Step 1: preprocess ran")
#     return {"score": state["score"] * 2}  # doubles the score

# # Node 2 — conditional edge is attached here
# def evaluate(state):
#     print("Step 2: evaluate ran")
#     return {"score": state["score"]}

# # Destination nodes
# def approve(state): return {"result": "APPROVED"}
# def reject(state):  return {"result": "REJECTED"}

# # Router — attached to evaluate, NOT preprocess
# def router(state):
#     if state["score"] >= 7:
#         return "approve"
#     else:
#         return "reject"

# g = StateGraph(State)
# g.add_node("preprocess", preprocess)
# g.add_node("evaluate",   evaluate)
# g.add_node("approve_node", approve)
# g.add_node("reject_node",  reject)

# g.set_entry_point("preprocess")           # graph STARTS at preprocess
# g.add_edge("preprocess", "evaluate")      # preprocess goes to evaluate
# g.add_conditional_edges(                  # routing happens AFTER evaluate
#     "evaluate",
#     router,
#     {"approve": "approve_node",
#      "reject":  "reject_node"}
# )
# g.add_edge("approve_node", END)
# g.add_edge("reject_node",  END)

# app = g.compile()

# result = app.invoke({"score": 4, "result": ""})
# print(result)