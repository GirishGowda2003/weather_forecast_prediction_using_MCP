class MCPController:
    def __init__(self, model, registry):
        self.model = model
        self.registry = registry

    def handle(self, query):
        if "weather" in query.lower():
            city = self._extract_city(query)
            result = self.registry.call_tool("get_weather", city)
            return f"Temperature in {city}: {result:.1f}°C"
        return self.model(query)

    def _extract_city(self, query):
        words = query.split()
        for i, word in enumerate(words):
            if word.lower() in ("in", "for", "at") and i + 1 < len(words):
                return words[i + 1].strip("?.,!")
        return "Bangalore"
