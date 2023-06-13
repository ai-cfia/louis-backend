""""""
import os
import openai

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms.openai import AzureOpenAI

from louis.tool.smartsearch import smartsearch

class ChainAgent:
    def __init__(self):
        self.llm = AzureOpenAI(deployment_name=os.environ['AZURE_OPENAI_GPT_DEPLOYMENT'], temperature=0.3, openai_api_key=openai.api_key)
        tool_names = [
            'llm-math',
            'wikipedia'
        ]
        self.tools = load_tools(tool_names, llm=self.llm)
        self.tools.append(smartsearch)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True)

    def run(self, query):
        return self.agent.run(query)
