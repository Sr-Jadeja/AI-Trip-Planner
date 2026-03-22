from utils.model_loader import load_llm
from prompt_library.prompt import SYSTEM_PROMPT
from tools.tools import ALL_TOOLS
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition


def build_graph(provider="groq"):
    """Build and return the LangGraph agent"""
    llm = load_llm(provider)
    llm_with_tools = llm.bind_tools(ALL_TOOLS)

    def agent(state: MessagesState):
        messages = [SYSTEM_PROMPT] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    graph = StateGraph(MessagesState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools=ALL_TOOLS))
    graph.add_edge(START, "agent")
    graph.add_conditional_edges("agent", tools_condition)
    graph.add_edge("tools", "agent")
    graph.add_edge("agent", END)

    return graph.compile()
