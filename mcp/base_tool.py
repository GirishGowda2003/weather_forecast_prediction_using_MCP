from abc import ABC, abstractmethod

class MCPTool(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, input):
        pass