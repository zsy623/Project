"""
配置文件模块
包含系统常量、API配置、游戏类型和主题配置、心理构念定义等
"""
import json

# DeepSeek API 配置
DEEPSEEK_API_KEY = "sk-6acd4ca5d18d44838b4c1a5199176e2e"  # DeepSeek API密钥，实际使用时替换为真实密钥
DEEPSEEK_MODEL = "deepseek-chat"  # 使用的DeepSeek模型名称
DEEPSEEK_TEMPERATURE = 0.5  # 模型生成温度，控制输出的随机性（0-1之间）

# 系统运行参数
MAX_CRITIC_ITERATIONS = 3  # 评论家Agent最大迭代次数（生成-优化循环）
MAX_PLAYER_ITERATIONS = 10  # 玩家交互最大迭代次数（游戏回合数）

# 游戏类型配置
GAME_TYPES = ["Fantasy", "Romance", "Science Fiction", "Slice of Life", "Horror"]

# 游戏主题配置，每种游戏类型对应的主题列表
GAME_TOPICS = {
    "Fantasy": ["Adventure", "Magic"],  # 奇幻类游戏主题：冒险、魔法
    "Romance": ["Love", "Marriage"],  # 浪漫类游戏主题：爱情、婚姻
    "Science Fiction": ["Space Exploration", "Time Travel"],  # 科幻类游戏主题：太空探索、时间旅行
    "Slice of Life": ["Family", "School"],  # 生活类游戏主题：家庭、学校
    "Horror": ["Haunted House", "Paranormal Investigation"]  # 恐怖类游戏主题：鬼屋、超自然调查
}

# 支持的心理构念类型
PSYCHOLOGICAL_CONSTRUCTS = [
    "extroversion",  # 外向性人格特质
    "depression",  # 抑郁程度
    "all_or_nothing",  # 全有或全无认知扭曲
    "mind_reading",  # 读心术认知扭曲
    "should_statements"  # 应该陈述认知扭曲
]


def get_prompt(disease_name, type):
    with open('new.json', 'r') as file:
        prompts_data = json.load(file)
    return prompts_data[disease_name][type]

