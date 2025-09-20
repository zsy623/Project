"""
DeepSeek API客户端模块
负责与DeepSeek API进行通信，处理LLM调用
"""

import requests  # 用于发送HTTP请求
# from tenacity import retry, stop_after_attempt, wait_exponential  # 重试机制库
from config import DEEPSEEK_API_KEY, DEEPSEEK_MODEL, DEEPSEEK_TEMPERATURE  # 导入配置


class DeepSeekClient:
    """DeepSeek API客户端类，封装LLM调用逻辑"""

    def __init__(self, api_key: str = DEEPSEEK_API_KEY):
        """
        初始化DeepSeek客户端

        Args:
            api_key (str): DeepSeek API密钥，默认为配置中的密钥
        """
        self.api_key = api_key  # 存储API密钥
        self.base_url = "https://api.deepseek.com/v1/chat/completions"  # DeepSeek API端点

    # @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def call_llm(self, prompt: str, model: str = DEEPSEEK_MODEL, temperature: float = DEEPSEEK_TEMPERATURE) -> str:
        """
        调用DeepSeek LLM API

        Args:
            prompt (str): 输入的提示词
            model (str): 使用的模型名称，默认为配置中的模型
            temperature (float): 生成温度，控制输出的随机性

        Returns:
            str: LLM生成的响应文本

        Raises:
            requests.HTTPError: 当API请求失败时抛出
        """
        # 设置请求头，包含认证信息
        headers = {
            "Authorization": f"Bearer {self.api_key}",  # Bearer token认证
            "Content-Type": "application/json"  # 请求内容类型为JSON
        }

        # 构建请求负载
        payload = {
            "model": model,  # 指定使用的模型
            "messages": [{"role": "user", "content": prompt}],  # 对话消息，当前只有用户输入
            "temperature": temperature  # 设置生成温度
        }

        # 发送POST请求到DeepSeek API
        response = requests.post(self.base_url, json=payload, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，抛出异常

        # 从响应中提取生成的文本内容
        return response.json()["choices"][0]["message"]["content"]