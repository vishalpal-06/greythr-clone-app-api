import asyncio
import logging
import os
from typing import TypedDict, Annotated

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

# Configure basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

logger.info("Starting mcp_client.py script")

load_dotenv()  # Load environment variables from .env file
logger.info("Environment variables loaded")

# llm = ChatOpenAI(model="gpt-5")
# Ensure the model name is correct for the Anthropic library version you have
llm = ChatAnthropic(model="claude-sonnet-4-5")
logger.info(f"LLM initialized with model:")

# Define the explicit path to your mcp_server.py script
# Use an absolute path check to be safe
server_script_path = r"C:\\Users\\VishalP-ardent\\OneDrive - Ardent\Desktop\\Projects\\greythr-clone-app-api\\mcp_server.py"

if not os.path.exists(server_script_path):
    logger.error(f"Server script not found at: {server_script_path}")
    # Consider exiting or raising an error if the path is critical
else:
    logger.info(f"Server script path confirmed: {server_script_path}")


# MCP client for local FastMCP server
logger.info("Initializing MultiServerMCPClient with stdio transport")
client = MultiServerMCPClient(
    {
        "greyhr": {
            "transport": "stdio",
            "command": "python",  # Use 'python' or 'python3' as appropriate for your environment
            "args": [server_script_path],
        }
    }
)
logger.info("MCP Client initialized")


# state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def build_graph():
    logger.info("Starting build_graph function")

    # This is a critical point where the client starts the subprocess and waits for tools
    logger.info(
        "Awaiting client.get_tools() - this might take time while server starts"
    )
    tools = await client.get_tools()
    logger.info(f"Received {len(tools)} tools from server")

    print(tools)

    llm_with_tools = llm.bind_tools(tools)

    # nodes
    async def chat_node(state: ChatState):
        logger.info("Inside chat_node")
        messages = state["messages"]
        response = await llm_with_tools.ainvoke(messages)
        logger.info("LLM responded in chat_node")
        return {"messages": [response]}

    tool_node = ToolNode(tools)

    # defining graph and nodes
    graph = StateGraph(ChatState)
    logger.info("StateGraph initialized")

    graph.add_node("chat_node", chat_node)
    graph.add_node("tools", tool_node)

    # defining graph connections
    graph.add_edge(START, "chat_node")
    graph.add_conditional_edges("chat_node", tools_condition)
    graph.add_edge("tools", "chat_node")

    chatbot = graph.compile()
    logger.info("Chatbot graph compiled")

    return chatbot


async def main():
    logger.info("Starting main function")

    chatbot = await build_graph()

    # running the graph
    user_message = HumanMessage(
        content="my username and password is vishalpal0602@gmail.com and Testing, Give my full details from hr portal"
    )
    logger.info(f"Invoking chatbot with message: '{user_message.content}'")

    # This is another critical async point where the graph runs
    result = await chatbot.ainvoke({"messages": [user_message]})
    logger.info("Chatbot invocation complete")

    final_content = result["messages"][-1].content
    print(final_content)
    logger.info("Script finished successfully")


if __name__ == "__main__":
    # Ensure the event loop runs the async main function
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("An error occurred during asyncio.run(main())")
