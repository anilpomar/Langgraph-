Phase 1: IMPORTS & DEFINITIONS (Top to Bottom)
📍 Lines 1-4: IMPORTS
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
✓ 1st
📍 Lines 5-6: CLASS DEFINITION
class WithReducerState(TypedDict):
history: Annotated[list, operator.add]
↳ Python CREATES the class object
✓ 2nd
📍 Lines 7-10: FUNCTION DEFINITIONS
def node3(state):
return {"history": ["node3 ran"]}
def node4(state):
↳ Python CREATES function objects, does NOT call them
✓ 3rd
Phase 2: GRAPH CONSTRUCTION (No Execution Yet)
📍 Lines 11-17: BUILD THE GRAPH
graph2 = StateGraph(WithReducerState)
graph2.add_node("n3", node3)
graph2.add_node("n4", node4)
graph2.set_entry_point("n3")
graph2.add_edge("n3", "n4")
graph2.add_edge("n4", END)
app2 = graph2.compile()
↳ These just SET UP the graph structure
✓ 4th
Phase 3: EXECUTION STARTS HERE ⚡
📍 Lines 19-20: MAIN CHECK
if __name__ == "__main__":
↳ Check if script is run directly (YES! ✓)
✓ 5th
📍 Line 21: CALL run_with_reducer()
run_with_reducer()
↳ NOW the function EXECUTES (inside function body)
✓ 6th
📍 Line 18: INSIDE run_with_reducer()
app2.invoke({"history": []})
↳ Invoke the compiled graph
↳ This calls node3() first
✓ 7th
📍 Inside node3() - FUNCTION BODY EXECUTES
def node3(state):
return {"history": ["node3 ran"]}
↳ node3 returns, goes to node4
✓ 8th
📍 Inside node4() - FUNCTION BODY EXECUTES
def node4(state):
return {"history": ["node4 ran"]}
↳ node4 returns, graph reaches END
✓ 9th
📍 Line 18: app2.invoke() RETURNS RESULT
result2 = {"history": ["node3 ran", "node4 ran"]}
↳ Result is stored in result2
✓ 10th
📍 Line 19: PRINT THE RESULT
print(result2)
↳ Output: {"history": ["node3 ran", "node4 ran"]}
✓ 11th
✅ SCRIPT ENDS
All code executed, program terminates
Key Concept: Code Execution Flow
1️⃣ TOP-TO-BOTTOM (Imports → Definitions)
Lines 1-17 are LOADED, not EXECUTED
Functions are created but NOT called yet