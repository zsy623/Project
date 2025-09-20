"""
PsychoGAT主系统模块
协调所有Agent的工作流程
"""

from deepseek_client import DeepSeekClient  # DeepSeek客户端
from game_designer_agent import GameDesignerAgent  # 游戏设计师Agent
from game_controller_agent import GameControllerAgent  # 游戏控制器Agent
# from critic_agent import CriticAgent  # 评论家Agent
# from human_simulator_agent import HumanSimulatorAgent  # 人类模拟器Agent
# from psychometric_evaluator import PsychometricEvaluator  # 心理测量评估器
from config import MAX_CRITIC_ITERATIONS, MAX_PLAYER_ITERATIONS  # 配置参数

class PsychoGAT:
    """PsychoGAT主系统类，协调所有组件工作"""

    def __init__(self, api_key: str):
        """
        初始化PsychoGAT系统

        Args:
            api_key (str): DeepSeek API密钥
        """
        # 创建共享的DeepSeek客户端实例
        client = DeepSeekClient(api_key)

        # 初始化所有Agent，共享同一个客户端
        self.designer = GameDesignerAgent(client)  # 游戏设计师
        self.controller = GameControllerAgent(client)  # 游戏控制器
        # self.critic = CriticAgent(client)  # 评论家
        # self.simulator = HumanSimulatorAgent(client)  # 人类模拟器
        # self.evaluator = PsychometricEvaluator()  # 心理测量评估器

    def run_assessment(self, construct: str, scale_json: str, game_type: str,
                       game_topic: str, max_iter: int = MAX_PLAYER_ITERATIONS) -> tuple:
        """
        运行完整的心理评估流程

        Args:
            construct (str): 要评估的心理构念
            scale_json (str): 原始量表JSON数据
            game_type (str): 游戏类型
            game_topic (str): 游戏主题
            max_iter (int): 最大交互次数，默认为配置值

        Returns:
            tuple: (总得分, 各项目得分列表)
        """
        # Step 1: 游戏设计师生成游戏设计
        design_output = self.designer.run(game_type, game_topic, scale_json, construct)
        print("design_output:\n", design_output)
        # 提取设计结果
        title = design_output["title"]  # 游戏标题
        thought = design_output["thoughts"]
        outline = design_output["outline"]  # 游戏大纲
        redesigned_scale = design_output["redesigned_scale"]  # 重设计后的量表

        # print("title:\n")
        # print(title)
        # print("thought:\n")
        # print(thought)
        # print("outline:\n")
        # print(outline)
        # print("redesigned_scale:\n")
        # print(redesigned_scale)

        # 初始化游戏状态
        memory = ""  # 游戏记忆（剧情摘要）
        prev_paragraph = ""  # 上一个段落
        instruction = ""  # 当前指令
        scores = []  # 得分记录

        # 遍历重设计后的每个量表项目
        for i, scale_item in enumerate(redesigned_scale):
            print("i:\n")
            print(i)
            print("scale_item:\n")
            print(scale_item)

            # 检查是否达到最大迭代次数
            if i >= max_iter:
                break

            # 计算当前进度百分比
            progress = (i / len(redesigned_scale)) * 100

            # Step 2: 游戏控制器生成游戏内容
            controller_output = self.controller.run(
                title, outline, scale_item, memory, prev_paragraph, instruction, progress, round=i, construct=construct
            )
            print("controller_output:\n")
            print(controller_output)

            print("controler_output[paragraphs]:\n")
            print(controller_output["paragraphs"])
            print("controller_output[questions_and_options]:\n")
            print(controller_output["questions_and_options"])
            print("controller_output[summary]:\n")
            print(controller_output["summary"])
            print("controller_output[instructions]:\n")
            print(controller_output["instructions"])

            break


            # Step 3: 评论家优化生成内容（可多轮迭代）
            critic_output = self._run_critic_iterations(
                memory, prev_paragraph, instruction,
                controller_output["question"],
                controller_output["paragraph"],
                controller_output["instructions"]
            )

            # Step 4: 人类模拟器选择指令
            selected_instruction = self.simulator.run(
                construct, memory, prev_paragraph,
                critic_output["paragraph"],
                critic_output["instructions"]
            )

            # Step 5: 更新游戏状态
            memory = critic_output["memory"]  # 更新记忆
            prev_paragraph = critic_output["paragraph"]  # 更新上一个段落
            instruction = selected_instruction  # 更新当前指令

            # Step 6: 记录得分
            # score = self.evaluator.evaluate(scale_item, selected_instruction)
            # scores.append(score)

        # 计算总得分
        total_score = sum(scores)
        return total_score, scores

    def _run_critic_iterations(self, memory: str, prev_paragraph: str, instruction: str,
                               question: str, generated_paragraph: str, next_instructions: list) -> dict:
        """
        运行评论家优化迭代

        Args:
            各个游戏状态参数

        Returns:
            dict: 优化后的游戏内容
        """
        current_output = {
            "paragraph": generated_paragraph,
            "memory": memory,
            "instructions": next_instructions
        }

        # 进行多轮优化迭代
        for iteration in range(MAX_CRITIC_ITERATIONS):
            # 评论家优化当前内容
            critic_output = self.critic.run(
                current_output["memory"], prev_paragraph, instruction,
                question, current_output["paragraph"], current_output["instructions"]
            )

            # 更新优化后的内容
            if critic_output["paragraph"] != "OK":
                current_output["paragraph"] = critic_output["paragraph"]
            if critic_output["memory"] != "OK":
                current_output["memory"] = critic_output["memory"]
            if critic_output["instructions"] != "OK":
                current_output["instructions"] = critic_output["instructions"]

            # 如果所有内容都已优化完成，提前结束
            if all([critic_output["paragraph"] == "OK",
                    critic_output["memory"] == "OK",
                    critic_output["instructions"] == "OK"]):
                break

        return current_output