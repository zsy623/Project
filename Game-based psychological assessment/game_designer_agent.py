# game_designer_agent.py
import json
from base_agent import BaseAgent
from config import get_prompt


class GameDesignerAgent(BaseAgent):
    def run(self, game_type, game_topic, scale_json, construct):
        PROMPT = get_prompt(disease_name=construct, type="design")
        prompt = PROMPT.format(
            type=game_type,
            topic=game_topic,
            self_report_scale=scale_json
        )
        response = self.client.call_llm(prompt)
        parsed_response = self._parse_response(response)
        return parsed_response

    def _parse_response(self,text):
        """
        Parses the text response from the language model into a structured dictionary.

        Args:
            text (str): The raw text response from the language model.

        Returns:
            dict: A dictionary containing the parsed game title, thoughts, outline,
                  and redesigned scale questions, or None if parsing fails.
        """
        try:
            # Extract Name
            name_start = text.find("Name: ")
            if name_start == -1:
                raise ValueError("Response does not contain 'Name: '")
            name_end = text.find("\n", name_start)
            name = text[name_start + len("Name: "):name_end].strip()

            # Extract Thoughts
            thoughts_start = text.find("Thoughts: ")
            if thoughts_start == -1:
                raise ValueError("Response does not contain 'Thoughts: '")
            thoughts_end = text.find("\n\nOutline: ", thoughts_start)
            if thoughts_end == -1:
                # Handle cases where "Outline:" might be on a new line but not separated by a double newline
                thoughts_end = text.find("Outline: ", thoughts_start)
                if thoughts_end == -1:
                    raise ValueError("Response does not contain 'Outline: ' after 'Thoughts: '")
            thoughts = text[thoughts_start + len("Thoughts: "):thoughts_end].strip()

            # Extract Outline
            outline_start = text.find("Outline: ",
                                      thoughts_end if "Outline: " in text[thoughts_end - 1:] else thoughts_end)
            if outline_start == -1:
                raise ValueError("Response does not contain 'Outline: '")
            outline_end = text.find("\n\nScale Questions in Order: ", outline_start)
            if outline_end == -1:
                # Handle cases where "Scale Questions in Order:" might be on a new line but not separated by a double newline
                outline_end = text.find("Scale Questions in Order: ", outline_start)
                if outline_end == -1:
                    raise ValueError("Response does not contain 'Scale Questions in Order: ' after 'Outline: '")
            outline = text[outline_start + len("Outline: "):outline_end].strip()

            # Extract Scale Questions in Order
            scale_start = text.find("Scale Questions in Order: ", outline_end if "Scale Questions in Order: " in text[
                                                                                                                 outline_end - 1:] else outline_end)
            if scale_start == -1:
                raise ValueError("Response does not contain 'Scale Questions in Order: '")
            scale_text = text[scale_start + len("Scale Questions in Order: "):].strip()

            # Parse scale_text as JSONL (each line is a JSON object)
            scale_lines = scale_text.split('\n')
            redesigned_scale = []
            for line in scale_lines:
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        redesigned_scale.append(item)
                    except json.JSONDecodeError as e:
                        print(f"Failed to parse JSON line: {line}, error: {e}")
                        continue

            return {
                "title": name,
                "thoughts": thoughts,
                "outline": outline,
                "redesigned_scale": redesigned_scale
            }
        except Exception as e:
            print(f"Error parsing response: {e}")
            return None