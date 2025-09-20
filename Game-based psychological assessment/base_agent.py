# base_agent.py
from abc import ABC, abstractmethod
from deepseek_client import DeepSeekClient

class BaseAgent(ABC):
    def __init__(self, client: DeepSeekClient):
        self.client = client

    @abstractmethod
    def run(self, **kwargs):
        pass
