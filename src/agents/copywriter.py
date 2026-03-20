"""
小红书 Agent - 文案创作模块
"""

class Copywriter:
    """文案创作 Agent"""
    
    def __init__(self):
        self.name = "文案撰稿人"
        self.role = "小红书爆款文案专家"
    
    async def write_post(self, topic: dict) -> dict:
        """根据选题撰写完整文案"""
        title = topic.get('title', '无标题')
        category = topic.get('category', '生活')
        
        # 生成标题
        title_variants = self._generate_titles(title, category)
        
        # 生成正文
        content = self._generate_content(title, category, topic.get('hook', ''))
        
        # 生成标签
        tags = topic.get('tags', ['#武汉', '#生活'])
        
        return {
            "titles": title_variants,
            "content": content,
            "tags": tags,
            "word_count": len(content)
        }
    
    def _generate_titles(self, base_title: str, category: str) -> list:
        """生成多个标题变体"""
        templates = [
            base_title,
            f"绝绝子！{base_title}",
            f"{base_title}（附攻略）",
            f"收藏！{base_title}",
            f"吐血整理！{base_title}"
        ]
        return templates[:3]
    
    def _generate_content(self, title: str, category: str, hook: str) -> str:
        """生成正文内容"""
        
        if "早餐" in category or "过早" in category:
            content = f"""
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
"""
        elif "贷款" in category or "金融" in category:
            content = f"""
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
"""
        else:
            content = f"""
{hook}今天来聊聊{category}的话题！

【正文内容】

1. 开场引入
2. 核心内容分享
3. 实用建议/攻略
4. 互动引导

❓ 你们还想看什么内容？评论区告诉我！

💡 关注我，不错过任何干货！
"""
        return content.strip()
    
    def check_length(self, content: str) -> dict:
        """检查文案长度"""
        words = len(content)
        lines = content.count('\n')
        return {
            "characters": words,
            "lines": lines,
            "status": "ok" if 300 < words < 1000 else "too_short" if words < 300 else "too_long"
        }

__all__ = ["Copywriter"]
