# LangChain Agent Examples

This repository contains examples of using LangChain, a framework for building applications with large language models (LLMs), to create various types of agents. These agents leverage the power of LLMs to perform tasks such as music recommendations, financial data retrieval, and mathematical reasoning.

## Features

- **Music Agent**: This agent uses the Spotify API to recommend songs based on the artists provided by the user. It utilizes the `SpotifyTool` from LangChain to interact with the Spotify API and retrieve top tracks for the given artists.

- **Finance Agent**: This agent can look up the stock ticker symbol for a given company using DuckDuckGo search. It demonstrates how to create a custom tool (`search_ticker`) with LangChain and integrate it into an agent.

- **Math Agent**: This agent can solve mathematical problems and answer logic-based reasoning questions. It showcases the use of `LLMMathChain` and `PromptTemplate` from LangChain to create agents capable of performing numerical calculations and logical reasoning.

## Technologies Used

- **LangChain**: This project utilizes LangChain, a framework for building applications with large language models. It provides tools and utilities for creating agents, tools, and chains to interact with LLMs.

- **AgentOps**: AgentOps is a platform for managing and monitoring LangChain agents. It is used in this project to track and record the agent's activities, enabling better monitoring and debugging.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/langchain-agent-examples.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the necessary environment variables (e.g., Spotify API credentials, OpenAI API key, AgentOps API key).

## Usage

Each agent is implemented in a separate Python file (`music_agent.py`, `finance_agent.py`, `math_agent.py`). You can run these files individually to interact with the respective agents.

For example, to run the Music Agent:

```bash
python music_agent.py
```

Follow the prompts or instructions provided by the agent to interact with it.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.