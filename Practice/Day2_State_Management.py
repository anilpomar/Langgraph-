# State is Backbone of every Langgraph application.
# Every Node Receives the Entire State as Input and Returns an Updated State(Which can be Partial.)
# Lets Understand Reducers where Functions that merge Partial Updates which unlocks patterns like appending to lists without overwriting them.


from langgraph.graph import StateGraph, END
from typing import TypedDict,Annotated
import operator


#Without Reducers (Annotated)
class WithoutState(TypedDict):
    history:list  #Plain List -No Reducer

def WithoutReducer():  #Step 2 No Execution of Function Starts here
    def node1(state): # Step 4 Function Body execution starts where node 1 is invoked first.
        return {"history":["node1 ran"]}
    
    def node2 (state):  # Step 4 Function Body executes where node 2 is invoked after node 1 and Graph Ends.
        return {"history":["node2 ran2"]}

#Define Graph
    graph=StateGraph(WithoutState)

#Add Nodes
    graph.add_node("n1", node1)
    graph.add_node("n2",node2)

    graph.set_entry_point("n1")
    graph.add_edge("n1","n2")
    graph.add_edge("n2", END)

    app =graph.compile()    
    result=app.invoke({"history":[]})  #Step 3 Invokes Compiled Graph
                                        #Step 5 Result from Nodes State is captured in Result
    print(result) #Output: {'history': ['node2 ran2']} - #Script Execution Ends


##With Reducers (Annotated)

class WithStateReducer(TypedDict):
       history:Annotated[list,operator.add] #List with Reducer that appends instead of overwriting

def WithReducer():
    def node3(state):
       return{"history":["node3 ran"]}

    def node4(state):
       return{"history":["node4 ran"]}

    graph2=StateGraph(WithStateReducer)
    graph2.add_node("n3", node3)
    graph2.add_node("n4", node4)

    graph2.set_entry_point("n3")
    graph2.add_edge("n3","n4")
    graph2.add_edge("n4", END)

    app2=graph2.compile()
    result2=app2.invoke({"history":[]})
    print(result2) #Output: {'history': ['node3 ran', 'node4 ran']}

if __name__ == "__main__": #Execution of program  starts here  (Step 1)
    print("Without Reducer:")
    WithoutReducer()
    print("\nWith Reducer:")
    WithReducer()