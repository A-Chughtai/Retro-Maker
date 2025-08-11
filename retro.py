import os
from dotenv import load_dotenv
load_dotenv()

import sys

import asyncio
import json

# --------------------------- ========== LLM ========== --------------------------- #

from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)



# --------------------------- ========== Graph State ========== --------------------------- #

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

# --------------------------- ========== MCP server ========== --------------------------- #

from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient({
    "github": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "-e",
        "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
      },
      "transport": "stdio",
    },
})

# --------------------------- ========== Functions to get tools ========== --------------------------- #

async def get_tools():
    tools = await client.get_tools()
    
    return tools

def clean_schema(schema):
    """Remove unsupported keys from a schema dict, recursively."""
    if not isinstance(schema, dict):
        return schema
    schema = dict(schema)  # Make a copy
    schema.pop('additionalProperties', None)
    schema.pop('$schema', None)
    # Recursively clean nested schemas
    for key, value in schema.items():
        if isinstance(value, dict):
            schema[key] = clean_schema(value)
        elif isinstance(value, list):
            schema[key] = [clean_schema(item) for item in value]
    return schema

async def get_tools_and_clean():
    tools = await get_tools()
    for tool in tools:
        if hasattr(tool, 'args_schema') and isinstance(tool.args_schema, dict):
            tool.args_schema = clean_schema(tool.args_schema)
    return tools

# --------------------------- ========== Memory Saver ========== --------------------------- #

from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# --------------------------- ========== AGENTS ========== --------------------------- #

from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


def my_agent(tools):
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )

    return agent

# --------------------------- ========== INITIALIZING NAME, REMO AND INPUT ========== --------------------------- #

user_name = sys.argv[1]
repo_name = sys.argv[2]

my_input=   f"""
                From the repository {repo_name} 
                Fetch my todays commits (my username is {user_name})
                Retrieve the full code diffs for each commit
                Review the changes in detail
                Summarize your findings in the following format:
                
                **What went well**
                * ---
                * ---
                
                **What could be improved**
                * ---
                * ---
                
                **Overall Observations**
                * ---
                * ---
            """
        

async def main():

    
    print("Your Name:", sys.argv[1])
    print("Target Repo:", sys.argv[2])


    ## ----- ( I am getting all the tools and passing them to agents ) ----- ##

    tools = await get_tools()

    agent = my_agent(tools)
    
    config = {"configurable": {"thread_id": "1"}}

    workflow = StateGraph(State)
    workflow.add_node("agent", agent)
    workflow.set_entry_point("agent")
    workflow.set_finish_point("agent")
    graph = workflow.compile(checkpointer=memory)

    user_input = my_input
    print("Start chatting with the agent. Type 'q' or 'quit' to exit.")
    while True:        

        if user_input.lower() in {"q", "quit"}:
            print("Exiting chat.")
            break

        print("Assistant:")
        async for resp in graph.astream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="values",
        ):
            if resp["messages"]:
                resp["messages"][-1].pretty_print()
        
        user_input = input("You: ")


if __name__ == "__main__":
    asyncio.run(main())