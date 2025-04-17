from openai import OpenAI

# replace with your actual API key and base URL if different from the default
client = OpenAI(api_key="sk-****", base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

analysis_prompt_template = """
请扮演一位具有政治洞察力和市场分析能力的金融顾问。以下是特朗普在 Truth Social 的发言：

"{content}"

请分析：
1. 核心观点
2. 情绪倾向（积极、中性、消极）
3. 涉及的政策/经济领域
4. 潜在影响的行业或公司
5. 简洁的投资建议

请用简洁、专业的语言输出。
"""

def analyze_content(truths, model="deepseek-r1"):
    results = []
    for idx, content in enumerate(truths, 1):
        print(f"\n🔍 分析 Truth #{idx}")
        prompt = analysis_prompt_template.format(content=content)

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content.strip()
        results.append((content, result))
        print(result)
    return results
