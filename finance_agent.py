import os
from dotenv import load_dotenv

load_dotenv()


from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_community.chat_models import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun, tool

@tool
def search_ticker(company_name: str) -> str:
    """
    Searches for the stock ticker symbol of a given company using DuckDuckGo.
    It parses search results specifically checking for entries from MarketWatch.
    """
    search = DuckDuckGoSearchRun()
    search_results = search.run(company_name)
    for result in search_results:
        if result["title"] == "Stock Ticker Symbol Lookup - MarketWatch":
            return result["description"].split(" ")[-1]
    return "No ticker found"


llm = ChatOpenAI(temperature=0.0)
tools = load_tools(["search_ticker"], llm=llm)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
output = agent.run("what is the ticker of Amazon")
print(output)

