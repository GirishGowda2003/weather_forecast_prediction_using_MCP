class MCPRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def call_tool(self, name, input):
        if name not in self.tools:
            raise Exception(f"Tool '{name}' not found in registry.")
        return self.tools[name].run(input)

    def list_tools(self):
        return [{"name": t.name, "description": t.description} for t in self.tools.values()]