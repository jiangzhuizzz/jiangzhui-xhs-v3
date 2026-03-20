"""
小红书 Agent - Agent 定义模块
"""

import os

class TopicPlanner:
    """选题策划 Agent - 智能版本"""
    
    def __init__(self):
        self.name = "选题策划师"
        self.role = "小红书内容策划专家，擅长发现热点话题和用户痛点"
        self.expertise = [
            "武汉本地生活",
            "贷款金融知识", 
            "早餐美食推荐",
            "热点话题分析"
        ]
    
    async def generate_topics_ai(self, preferences: list, count: int = 5) -> list:
        """使用 AI 生成高质量选题"""
        # 这里可以接入 OpenAI / Claude 等 API
        # 暂时返回基于偏好的智能推荐
        
        topics = []
        for i in range(count):
            category = preferences[i % len(preferences)] if preferences else "生活"
            
            # 根据不同分类生成对应选题
            if "早餐" in category or "武汉" in category:
                title = self._get_breakfast_topic(i)
            elif "贷款" in category or "金融" in category:
                title = self._get_loan_topic(i)
            else:
                title = self._get_lifestyle_topic(i)
            
            topics.append({
                "id": i + 1,
                "title": title,
                "category": category,
                "tags": self._get_tags(category),
                "hook": self._generate_hook(title),
                "outline": self._generate_outline(title)
            })
        return topics
    
    def _get_breakfast_topic(self, index: int) -> str:
        topics = [
            "武汉人过早指南：这5家早餐店本地人从小吃到大",
            "在武汉过早，10块钱能吃到撑",
            "武汉过早的100种可能",
            "碳水炸弹预警！武汉早餐图鉴",
            "早上6点的武汉街头，全是宝藏"
        ]
        return topics[index % len(topics)]
    
    def _get_loan_topic(self, index: int) -> str:
        topics = [
            "贷款被拒3次后，我终于找到了秒批的方法",
            "武汉公积金贷款最新政策解读",
            "信用贷还是抵押贷？一篇讲清楚",
            "上班族贷款避坑指南",
            "利率对比：武汉哪家银行最划算"
        ]
        return topics[index % len(topics)]
    
    def _get_lifestyle_topic(self, index: int) -> str:
        topics = [
            "武汉周末好去处推荐",
            "在武汉生活必须知道的10件事",
            "武汉人私藏的小众打卡地",
            "武汉租房指南",
            "武汉过早文化探索"
        ]
        return topics[index % len(topics)]
    
    def _get_tags(self, category: str) -> list:
        base_tags = ["#武汉", "#生活"]
        if "早餐" in category or "美食" in category:
            base_tags.extend(["#武汉美食", "#过早"])
        elif "贷款" in category or "金融" in category:
            base_tags.extend(["#贷款知识", "#金融"])
        else:
            base_tags.extend(["#本地生活", "#攻略"])
        return base_tags
    
    def _generate_hook(self, title: str) -> str:
        hooks = [
            "说出来你可能不信...",
            "这个问题我被问了100遍！",
            "后悔没早知道系列！",
            "答应我，一定要看完！",
            "这个秘密我只告诉你！"
        ]
        return hooks[len(title) % len(hooks)]
    
    def _generate_outline(self, title: str) -> dict:
        return {
            "开头": "痛点引入 + 悬念设置",
            "中间": "3-5个要点 + 案例分享",
            "结尾": "总结 + 互动引导"
        }

# 兼容旧接口
def generate_topics(user_preferences: list, count: int = 5) -> list:
    planner = TopicPlanner()
    import asyncio
    return asyncio.run(planner.generate_topics_ai(user_preferences, count))

__all__ = ["TopicPlanner", "generate_topics"]
