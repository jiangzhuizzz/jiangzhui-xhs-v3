"""
小红书 Agent - 文案生成模块
支持多 LLM: Claude / Gemini / MiniMax
"""

import os
import json

class Copywriter:
    """文案生成 Agent"""
    
    def __init__(self, llm_provider: str = "minimax"):
        self.name = "文案撰稿人"
        self.role = "小红书爆款文案专家"
        self.llm_provider = llm_provider
    
    async def write_post(self, topic: dict) -> dict:
        """根据选题撰写完整文案
        
        Args:
            topic: 选题字典，需包含 title, category, hook, tags 等
            
        Returns:
            文案字典，包含 titles, content, tags, word_count
        """
        title = topic.get('title', '无标题')
        category = topic.get('category', '生活')
        hook = topic.get('hook', '')
        
        # 生成标题变体
        title_variants = self._generate_titles(title, category)
        
        # 生成正文
        content = await self._generate_content_ai(title, category, hook)
        
        # 合并标签
        tags = topic.get('tags', ['#武汉', '#生活'])
        
        return {
            "titles": title_variants,
            "content": content,
            "tags": tags,
            "word_count": len(content),
            "llm_provider": self.llm_provider
        }
    
    async def _generate_content_ai(self, title: str, category: str, hook: str) -> str:
        """调用 LLM 生成内容
        
        这里可以接入 MiniMax/Claude/Gemini API
        目前返回模板内容 + 结构化数据
        """
        
        # TODO: 接入实际 LLM API
        # 示例: result = await call_minimax_api(prompt)
        
        if "早餐" in category or "过早" in category:
            content = self._template_breakfast(title, hook)
        elif "贷款" in category or "金融" in category:
            content = self._template_loan(title, hook)
        else:
            content = self._template_lifestyle(title, hook, category)
        
        return content
    
    def _generate_titles(self, base_title: str, category: str) -> list:
        """生成标题变体"""
        templates = [
            base_title,
            f"绝绝子！{base_title}",
            f"{base_title}（附攻略）",
            f"收藏！{base_title}",
            f"吐血整理！{base_title}"
        ]
        return templates[:3]
    
    def _template_breakfast(self, title: str, hook: str) -> str:
        return f"""
{hook}在武汉，过早不仅仅是为了填饱肚子，更是一种生活仪式感！

今天分享几家我私藏的宝藏早餐店，每一家都让我回购N次！

🏠 **第一家：xxx热干面**
📍 地址：xx路xx号
💰 人均：8元
⭐ 必点：热干面+蛋酒

🏠 **第二家：xxx豆皮**
📍 地址：xx路xx号  
💰 人均：12元
⭐ 必点：三鲜豆皮+面窝

🏠 **第三家：xxx汤包**
📍 地址：xx路xx号
💰 人均：15元
⭐ 必点：鲜肉汤包

❓你们心目中武汉最好吃的早餐是哪家？评论区告诉我！

💡 关注我，带你吃遍武汉！
""".strip()
    
    def _template_loan(self, title: str, hook: str) -> str:
        return f"""
{hook}最近很多朋友问我贷款的问题，今天一次性讲清楚！

【贷款类型大盘点】

1️⃣ **信用贷**
适合：上班族、公积金缴纳者
优点：无需抵押、审批快
参考利率：3.5%-8%

2️⃣ **抵押贷**
适合：有房/有车一族
优点：额度高、利率低
参考利率：3.2%-5%

3️⃣ **企业贷**
适合：企业经营主
优点：额度大、周期长
参考利率：3%-6%

⚠️ **避坑指南**
• 提前还款可能有违约金
• 警惕"0首付"陷阱
• 建议多对比几家银行

❓ 有贷款相关问题，评论区见！

💡 觉得有用记得点赞收藏！
""".strip()
    
    def _template_lifestyle(self, title: str, hook: str, category: str) -> str:
        return f"""
{hook}今天来聊聊{category}的话题！

【正文内容】

1. 开场引入
2. 核心内容分享
3. 实用建议/攻略
4. 互动引导

❓ 你们还想看什么内容？评论区告诉我！

💡 关注我，不错过任何干货！
""".strip()
    
    def check_length(self, content: str) -> dict:
        """检查文案长度"""
        words = len(content)
        return {
            "characters": words,
            "status": "ok" if 300 < words < 1000 else "too_short" if words < 300 else "too_long"
        }

__all__ = ["Copywriter"]
