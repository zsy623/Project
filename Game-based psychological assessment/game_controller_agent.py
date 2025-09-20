# game_controller_agent.py
import json
import re
from base_agent import BaseAgent
from config import get_prompt


class GameControllerAgent(BaseAgent):
    def run(self, title, outline, scale_item, memory, prev_paragraph, instruction, progress, round, construct):
        # This part of the code is already correct based on your previous snippets.
        if round == 0:
            PROMPT = get_prompt(disease_name=construct, type="initial")
            prompt = PROMPT.format(
                title=title,
                outline=outline,
                scale_item=scale_item
            )
        else:
            PROMPT = get_prompt(disease_name=construct, type="subsequent")
            prompt = PROMPT.format(
                title=title,
                outline=outline,
                scale_item=scale_item,
                short_memory=memory,
                input_paragraph=prev_paragraph,
                input_instruction=instruction,
                progress=progress
            )
        response = self.client.call_llm(prompt)
        return self._parse_response(response)

    def _parse_response(self, text):
        try:
            # Check if it's the initial iteration by looking for "Paragraph 1"
            if text.startswith("Paragraph 1:"):
                # Initial iteration parsing
                p1_start = text.find("Paragraph 1:") + len("Paragraph 1:")
                p1_end = text.find("\n\nParagraph 2:")
                paragraph1 = text[p1_start:p1_end].strip()

                p2_start = text.find("Paragraph 2:") + len("Paragraph 2:")
                p2_end = text.find("\n\nQuestion and its Options:")
                paragraph2 = text[p2_start:p2_end].strip()

                q_start = text.find("Question and its Options:") + len("Question and its Options:")
                q_end = text.find("\n\nParagraph 3:")
                question_options = json.loads(text[q_start:q_end].strip())

                p3_start = text.find("Paragraph 3:") + len("Paragraph 3:")
                p3_end = text.find("\n\nSummary:")
                paragraph3 = text[p3_start:p3_end].strip()

                sum_start = text.find("Summary:") + len("Summary:")
                sum_end = text.find("\n\nInstruction 1:")
                summary = text[sum_start:sum_end].strip()

                inst1_start = text.find("Instruction 1:") + len("Instruction 1:")
                inst1_end = text.find("\n\nInstruction 2:")
                instruction1 = text[inst1_start:inst1_end].strip()

                inst2_start = text.find("Instruction 2:") + len("Instruction 2:")
                instruction2 = text[inst2_start:].strip()

                return {
                    "paragraphs": [paragraph1, paragraph2, paragraph3],
                    "question_and_options": question_options,
                    "summary": summary,
                    "instructions": [instruction1, instruction2]
                }

            else:
                # Subsequent iteration parsing
                q_start = text.find("Question and its Options:") + len("Question and its Options:")
                q_end = text.find("\n\nOutput Paragraph:")
                question_options = json.loads(text[q_start:q_end].strip())

                p_start = text.find("Output Paragraph:") + len("Output Paragraph:")
                p_end = text.find("\n\nOutput Memory:")
                output_paragraph = text[p_start:p_end].strip()

                mem_start = text.find("Output Memory:") + len("Output Memory:")
                mem_end = text.find("\n\nOutput Instruction:")
                memory_text = text[mem_start:mem_end].strip()

                # Use regex to find Rational and Updated Memory
                rational_match = re.search(r"Rational: (.*?);", memory_text, re.DOTALL)
                updated_mem_match = re.search(r"Updated Memory: (.*)", memory_text, re.DOTALL)

                rational = rational_match.group(1).strip() if rational_match else ""
                updated_memory = updated_mem_match.group(1).strip() if updated_mem_match else ""

                inst_start = text.find("Output Instruction:") + len("Output Instruction:")
                instructions_text = text[inst_start:].strip()

                inst1_start = instructions_text.find("Instruction 1:") + len("Instruction 1:")
                inst1_end = instructions_text.find("\n\nInstruction 2:")
                instruction1 = instructions_text[inst1_start:inst1_end].strip()

                inst2_start = instructions_text.find("Instruction 2:") + len("Instruction 2:")
                instruction2 = instructions_text[inst2_start:].strip()

                return {
                    "question_and_options": question_options,
                    "output_paragraph": output_paragraph,
                    "output_memory": {
                        "rational": rational,
                        "updated_memory": updated_memory
                    },
                    "instructions": [instruction1, instruction2]
                }

        except Exception as e:
            print(f"Error parsing game controller response: {e}")
            return None