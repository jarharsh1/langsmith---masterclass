from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import requests
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain import hub
from dotenv import load_dotenv
import os  # ✅ necessary (you use os.environ)

load_dotenv()

search_tool = DuckDuckGoSearchRun()

os.environ['LANGCHAIN_PROJECT'] = "ReAct Agent"

@tool
def get_weather_data(city: str) -> str:
  """
  This function fetches the current weather data for a given city
  """
  url = f'https://api.weatherstack.com/current?access_key=f07d9636974c4120025fadf60678771b&query={city}'

  response = requests.get(url)

  return str(response.json())  # ✅ necessary: tool should return a string

llm = ChatOpenAI()

# Step 2: Pull the ReAct prompt from LangChain Hub
prompt = hub.pull("hwchase17/react")  # pulls the standard ReAct agent prompt

# Step 3: Create the ReAct agent manually with the pulled prompt
agent = create_react_agent(
    llm=llm,
    tools=[search_tool, get_weather_data],
    prompt=prompt
)

# Step 4: Wrap it with AgentExecutor
agent_executor = AgentExecutor(
    agent=agent,
    tools=[search_tool, get_weather_data],
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True,          # ✅ prevents crash on format issues
    return_intermediate_steps=True       # ✅ lets you see where it got stuck
)


# What is the release date of Dhadak 2?
# What is the current temp of gurgaon
# Identify the birthplace city of Kalpana Chawla (search) and give its current temperature.

# Step 5: Invoke
response = agent_executor.invoke({"input": "What is the current temp of gurgaon"})
print(response)

print(response['output'])
