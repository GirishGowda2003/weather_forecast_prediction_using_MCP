from mcp.controller import MCPController
from mcp.registry import MCPRegistry
from mcp.tools.weather_tool import WeatherTool

def dummy_llm(query):
    return "LLM fallback response"

registry = MCPRegistry()
registry.register(WeatherTool())

mcp = MCPController(dummy_llm, registry)

print(mcp.handle("What is the weather in Bangalore?"))