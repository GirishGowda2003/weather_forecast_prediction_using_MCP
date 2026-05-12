from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI

def get_weather(city: str) -> str:
    return "28°C"  # mock — replace with WeatherTool().run(city) for real data

weather_tool = Tool(
    name="Weather Tool",
    func=get_weather,
    description="Get current weather info for a city"
)

llm = ChatOpenAI(model="gpt-4")

agent = initialize_agent(
    tools=[weather_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    print(agent.run("Weather in Bangalore"))