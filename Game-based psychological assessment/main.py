import json
from psychogat import PsychoGAT
from config import DEEPSEEK_API_KEY

psychogat = PsychoGAT(DEEPSEEK_API_KEY)

# # 读入游戏类型和游戏主题
# print("Please input game type you desired:\n")
# game_type = input()
# print("Please input game topic you desired:\n")
# game_topic = input()

game_type = "Romance"
game_topic = "Love"
construct = "all_or_nothing"

# 准备原始评估量表
with open("self_report_scales.json", "r") as file:
    self_report_scales = json.load(file)

self_report_scale = self_report_scales["cognitive_distortions_scale"]["all_or_nothing"]

total_score, item_scores = psychogat.run_assessment(
    construct=construct,
    scale_json=self_report_scale,
    game_type="Fantasy",
    game_topic="Adventure"
)
#
# print(f"Total Score: {total_score}")
# print(f"Item Scores: {item_scores}")