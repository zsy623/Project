# human_simulator_agent.py
from base_agent import BaseAgent

class HumanSimulatorAgent(BaseAgent):
    def run(self, trait, memory, prev_paragraph, new_paragraph, instructions):
        prompt = HUMAN_SIMULATOR_PROMPT.format(
            trait=trait,
            memory=memory,
            previous_paragraph=prev_paragraph,
            new_paragraph=new_paragraph,
            instructions=instructions
        )
        response = self.client.call_llm(prompt)
        return self._parse_response(response)

    def _parse_response(self, text):
        # 解析响应，提取 selected_instruction
        pass