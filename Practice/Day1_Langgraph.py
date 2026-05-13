# LangGraph does not instantiate your class at all. It only uses it as a hint to read the field names.#  Internally LangGraph always stores and #  passes state as a plain Python dict — your class is never actually created as an object.
# In this case TypedDict gives you ZERO runtime difference.
# Removing it changes nothing you can observe.
# This is completely normal and expected

#How Exactly the flow works Moment By Moment
# app.invoke({"message": "world", "count": 0})
#                ↓
#   LangGraph takes this dict
#                ↓
#   calls greet({"message": "world", "count": 0})
#                ↓
#   inside greet — state = {"message": "world", "count": 0}
#                ↓
#   you access state["message"] → "world"
#                ↓
#   you return {"message": "Hello, world!"}
#                ↓
#   LangGraph merges that back into state
#                ↓
#   calls next node with updated state


from langgraph.graph import StateGraph, END #stategraph is the main class that represents the graph, and END is a special constant that represents the end of the graph.
from typing import TypedDict #TypedDict is standard Python type that define a dictionary with keys and values. Langgraph uses it to know Shape of your State.(What Fields exist and what type each holds)

# 1. Define your state
class State():
    message: str #Field that entire graph with read and write 
    count:int

# 2. Define nodes (just plain Python functions)
def greet(state: State) -> State: #state is just the variable that receives the current dict LangGraph passes in. The : State hint is just a label so your IDE knows what fields to suggest when you type state["..."].
    return {"message": f"Hello, {state['message']}!"}

def shout(state: State) -> State:
    return {"message": state["message"].upper()}

# 3. Build the graph
#Creates new graph instance and tells it to use State as its data Schema. 
# This is just Blueprint. Langgraph knows what fields to Track.
graph = StateGraph(State) 
# Registers the greet and Shout function as a node. 
# First Argument is the string name  used to connect edges, 
# Second is the actual function to call.  
# Name and Function dont have to match. Keep it matched for readabolity.
graph.add_node("greet", greet) 
graph.add_node("shout", shout)

# 4. Connect the nodes
# Tells Langgraph which node to run first when you call invoke().
# Every Graph needs exactly one entry point. Internally this adds an edge from a special START node to greet.
graph.set_entry_point("greet") 

# Adds a Fixed Edge after greet finishes it goes to  shout node. 
# Fixed Edge always go to the same destination. 
# IF we want to choose different node based on the state values we should use add_conditional_edges() instead.
graph.add_edge("greet", "shout")

# Here we mention Graphs Terminal Node. Without this Graph doesnt know when to stop.(After Shout finishes it stops Graph execution)
# END is just the string "__end__" a convention Langgraph recognises as the exit Signal.
graph.add_edge("shout", END)

# 5. Compile and run
# Validates the Graph(Check for missing unreachable nodes,edges) and returns a CompliedGraph Object call app. This is the object that actually runs.
# You can also pass a checkpointer= here to add memory(Covered in Day 5)
app = graph.compile()

# Starts the graph with initial state {message: "world", count: 0}, runs every node in order (greet → shout) and returns the final state.
# invoke() is synchronous  and blocking it waits for the entire graph (All Nodes) to finish and return.
result = app.invoke({"message": "world","count": 0})

#Print the final state after all nodes ran, that always holds the entire full state.
print(result)
print (result["count"])  # Should print 1
print (result["message"])  # Should print "HELLO, WORLD!"
print(result.keys())
# print(app.get_graph().draw_ascii())


