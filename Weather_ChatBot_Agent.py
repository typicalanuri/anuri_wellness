from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

openai_api_key = os.getenv("OPENAI_API_KEY")
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")

llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def get_city_cooridinates(city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={openweather_api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    raise ValueError("City not found")

def get_weather(city: str):
    lat, lon = get_city_cooridinates(city)
    url = f"http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={openweather_api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    temp = data["current"]["temp"]
    conidtion = data["current"]["weather"][0]["desciption"]
    return f"The weather in {city} is {temp}C with {conidtion}"

weather_tool = Tool(
    name="Weather Fetcher",
    func=get_weather,
    description="Fetches the current weather for a specified city.",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    ("human", "{input}"),
    ("placeholder", "chat_history")
])
tools = weather_tool

# Create the agent
agent = create_react_agent(llm, tools, prompt)

# Create an AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)





# Run the agent
result = agent_executor.invoke({"input": "What's the weather like in New York?"})
print(result)
