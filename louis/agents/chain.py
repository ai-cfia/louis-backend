""""""
import os
import openai
import json

from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms.openai import AzureOpenAI

from louis.tools.smartsearch import SmartSearch

class ChainAgent:
    """ChainAgent is a wrapper around the Louis agent that adds the SmartSearch tool"""

    prompt_prefix = """<|im_start|>system
You are Louis, a french and english bilingual virtual assistant for the Canadian Food Inspection Agency.
The Canadian Food Inspection Agency (CFIA) is a regulatory agency that is responsible for safeguarding Canada's food supply
and protecting the health of Canadians.
The CFIA's mandate includes a wide range of activities related to food safety, animal health, and plant health,
including inspection, testing, and enforcement.
Answer in the langage of the question asked. You can also return a bilingual french and english when specifically requested.
Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know.
Do not generate answers that don't use the sources below.
If asking a clarifying question to the user would help, ask the question.
For tabular information return it as an html table. Do not return markdown format.
Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response.
Use square brakets to reference the source, e.g. [info1.txt].
Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf].

Generate three very brief follow-up questions that the user would likely ask next about laws and regulations related to the agency.
Use double angle brackets to reference the questions, e.g. <<What regulations do I need to be aware of?>>.
Try not to repeat questions that have already been asked.
Only generate questions and do not generate any text before or after the questions, such as 'Next Questions'

<|im_end|>
{chat_history}
"""

    follow_up_questions_prompt_content = """"""

    query_prompt_template = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in a knowledge base.
    Generate a search query based on the conversation and the new question.
    Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
    Do not include any text inside [] or <<>> in the search query terms.

Chat History:
{chat_history}

Question:
{question}

Search query:
"""

    def __init__(self):
        self.llm = AzureOpenAI(deployment_name=os.environ['AZURE_OPENAI_GPT_DEPLOYMENT'], temperature=0.3, openai_api_key=openai.api_key)
        tool_names = [
            'llm-math'
        ]
        self.tools = load_tools(tool_names, llm=self.llm)
        self.tools.append(SmartSearch)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            return_intermediate_steps=True)

    def run(self, history, _overrides={}):
        """Run the agent on a history of messages"""
        prompt = self.prompt_prefix.format(chat_history=history)
        response = self.agent({"input": prompt }, include_run_info=True)
        retvalue = {
            "data_points": json.dumps(response['input'], indent=4),
            "answer": response['output'],
            "thoughts": json.dumps(response['intermediate_steps'], indent=4).replace('\n', '<br>')
        }
        return retvalue
