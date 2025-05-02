import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent

# Load environment variables from .env file
load_dotenv()

model = ChatOpenAI(model="gpt-4o")
async def main():
    async with MultiServerMCPClient({
        "opensearch": {
        "url": "http://localhost:9200/_plugins/_ml/mcp/sse?append_to_base_url=true",
        "transport": "sse",
        "headers": {
            "Content-Type": "application/json",
            "Accept-Encoding": "identity",  # ← disable gzip/deflate
        }
    }
    }) as client:
        tools = client.get_tools()
        agent = initialize_agent(
            tools=tools,
            llm=model,
            agent=AgentType.OPENAI_FUNCTIONS,
            verbose=True,
        )
        print(tools)

        await agent.ainvoke({"input": "List all the products from Opensearch"})
if __name__ == "__main__":
    asyncio.run(main())
