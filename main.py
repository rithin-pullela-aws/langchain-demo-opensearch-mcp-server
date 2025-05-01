import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor, AgentType, initialize_agent
from langchain import hub

# Load environment variables from .env file
load_dotenv()

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/react")
model = ChatOpenAI(model="gpt-4o", temperature=0)
async def main():
    # 1) Connect to your SSE MCP server
    async with MultiServerMCPClient({
        "opensearch": {
        "url": "http://localhost:9200/_plugins/_ml/mcp/sse?append_to_base_url=true",
        "transport": "sse",
        "headers": {
            "Content-Type": "application/json",
            "Accept-Encoding": "identity",  # ← disable gzip/deflate
        },
        "sse_read_timeout": 10,
    }
    }) as client:
        tools = client.get_tools()
        agent = initialize_agent(
            tools=tools,
            llm=model,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
        )

        # note: with function‐calling agent, .ainvoke() still expects a dict
        result = await agent.ainvoke({"input": "List Opensearch indices"})
        # result will be something like {"output": "... final answer ..."}
        print(result)
        print(result["output"])
if __name__ == "__main__":
    asyncio.run(main())
