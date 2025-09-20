# critic_agent.py
from base_agent import BaseAgent
from prompt_templates import CRITIC_PROMPT

class CriticAgent(BaseAgent):
    def run(self, memory, prev_paragraph, instruction, question, generated_paragraph, next_instructions):
        prompt = CRITIC_PROMPT.format(
            short_memory=memory,
            previous_paragraph=prev_paragraph,
            current_instruction=instruction,
            current_question=question,
            generated_paragraph=generated_paragraph,
            next_instructions=next_instructions
        )
        response = self.client.call_llm(prompt)
        return self._parse_response(response)

    def _parse_response(self, text):
        # 解析响应，提取 refined_paragraph, refined_memory, refined_instructions
        pass