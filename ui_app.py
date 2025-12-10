import streamlit as st
import asyncio
import logging
import os
from typing import TypedDict, Annotated

# Ensure you have these libraries installed:
# pip install streamlit langchain-google-genai langchain-core langchain-mcp-adapters langgraph python-dotenv

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()

# --- Configuration ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

server_script_path = r"C:\\Users\\VishalP-ardent\\OneDrive - Ardent\\Desktop\\Projects\\greythr-clone-app-api\\mcp_server.py"

if not os.path.exists(server_script_path):
    st.error(f"Server script not found at: {server_script_path}")
    st.stop()

client = MultiServerMCPClient(
    {
        "greyhr": {
            "transport": "stdio",
            "command": "python",
            "args": [server_script_path],
        }
    }
)


# --- LangGraph Setup ---
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def run_async_in_sync(async_func):
    """Helper to run an async function within a sync context."""
    # This checks if an event loop is already running (e.g., Streamlit's webserver)
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        # If not, create a new loop for this specific task
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Run the function within the appropriate loop context
    return loop.run_until_complete(async_func)


@st.cache_resource
def load_chatbot():
    """Builds and compiles the LangGraph chatbot asynchronously."""

    async def build_graph_async():
        # These operations are inherently async
        tools = await client.get_tools()
        llm_with_tools = llm.bind_tools(tools)

        async def chat_node(state: ChatState):
            response = await llm_with_tools.ainvoke(state["messages"])
            return {"messages": [response]}

        tool_node = ToolNode(tools)
        graph = StateGraph(ChatState)
        graph.add_node("chat_node", chat_node)
        graph.add_node("tools", tool_node)
        graph.add_edge(START, "chat_node")
        graph.add_conditional_edges("chat_node", tools_condition)
        graph.add_edge("tools", "chat_node")
        chatbot = graph.compile()
        return chatbot

    # Use the helper function to run the async build operation
    # This avoids explicitly closing the loop with the previous "finally: loop.close()"
    return run_async_in_sync(build_graph_async())


# --- Streamlit UI ---
st.title("GreyHR Clone MCP Chatbot")

# Initialize session state for messages and chatbot if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Load the chatbot using the cached function
chatbot = load_chatbot()

# Display chat messages from history
for message in st.session_state["messages"]:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# Accept user input
if prompt := st.chat_input(
    "Enter your request, e.g., 'my username is... give me details'"
):
    st.session_state["messages"].append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process response
    with st.chat_message("assistant"):
        # We use our helper function again to invoke the async chatbot method
        response = run_async_in_sync(
            chatbot.ainvoke({"messages": st.session_state["messages"]})
        )

        ai_message_content = response["messages"][-1].content
        st.markdown(ai_message_content)
        st.session_state["messages"].append(AIMessage(content=ai_message_content))
