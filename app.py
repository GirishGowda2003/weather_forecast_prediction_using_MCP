import streamlit as st
from mcp.controller import MCPController
from mcp.registry import MCPRegistry
from mcp.tools.weather_tool import WeatherTool

# ── Setup — NO @st.cache_resource so controller is always fresh ────────────────
def dummy_llm(query):
    return "This query is outside the scope of registered tools."

def build_mcp():
    registry = MCPRegistry()
    registry.register(WeatherTool())
    return MCPController(dummy_llm, registry)

mcp = build_mcp()
weather_tool = WeatherTool()

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="MCP Weather Dashboard", page_icon="🌤️", layout="centered")

st.title("🌤️ MCP Weather Dashboard")
st.caption("Powered by the Model Context Protocol (MCP) + OpenWeatherMap")

# ── Registered Tools ───────────────────────────────────────────────────────────
with st.expander("🔧 Registered MCP Tools"):
    _reg = MCPRegistry()
    _reg.register(WeatherTool())
    for tool in _reg.list_tools():
        st.markdown(f"**`{tool['name']}`** — {tool['description']}")

st.divider()

# ── City Lookup ────────────────────────────────────────────────────────────────
st.subheader("City Weather Lookup")

city = str(st.text_input("Enter city name", value="Bangalore", key="city_input")).strip()

if st.button("Get Weather", key="btn_get_weather"):
    if city:
        with st.spinner(f"Fetching weather for {city}..."):
            try:
                data = weather_tool.get_full_weather(city)
                col1, col2, col3 = st.columns(3)
                col1.metric("🌡️ Temperature", f"{data['temp']}°C")
                col2.metric("🤔 Feels Like", f"{data['feels_like']}°C")
                col3.metric("💧 Humidity", f"{data['humidity']}%")
                col4, col5 = st.columns(2)
                col4.metric("💨 Wind Speed", f"{data['wind_speed']} m/s")
                col5.metric("🔵 Pressure", f"{data['pressure']} hPa")
                st.info(f"**Condition:** {data['description']}  |  📍 {data['city']}, {data['country']}")
            except Exception as e:
                st.error(f"Error fetching weather: {e}")
    else:
        st.warning("Please enter a city name.")

st.divider()

# ── MCP Query Interface ────────────────────────────────────────────────────────
st.subheader("MCP Query Interface")
st.caption("Ask a natural language question — the controller routes it to the right tool.")

query = str(st.text_input(
    "Ask the MCP controller",
    placeholder="What is the weather in Mumbai?",
    key="mcp_query_input"
)).strip()

if st.button("Send Query", key="btn_send_query"):
    if query:
        with st.spinner("Processing via MCP controller..."):
            try:
                response = mcp.handle(query)
                st.success(f"**Response:** {response}")
            except Exception as e:
                st.error(f"Controller error: {e}")
    else:
        st.warning("Please enter a query.")

st.divider()

# ── Multi-City Comparison ──────────────────────────────────────────────────────
st.subheader("Multi-City Comparison")

cities_input = str(st.text_input(
    "Enter cities (comma-separated)",
    value="Bangalore, Mumbai, Delhi, Chennai",
    key="cities_input"
))

if st.button("Compare Cities", key="btn_compare"):
    cities = [c.strip() for c in cities_input.split(",") if c.strip()]
    if cities:
        results = []
        progress = st.progress(0)
        for i, c in enumerate(cities):
            try:
                d = weather_tool.get_full_weather(c)
                results.append(d)
            except Exception as e:
                st.warning(f"Could not fetch data for {c}: {e}")
            progress.progress((i + 1) / len(cities))
        if results:
            cols = st.columns(len(results))
            for col, d in zip(cols, results):
                col.metric(f"📍 {d['city']}", f"{d['temp']}°C", d['description'])
