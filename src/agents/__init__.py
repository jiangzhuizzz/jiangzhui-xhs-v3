"""
小红书 Agent - 选题策划模块
"""

class TopicPlanner:
    """选题策划 Agent - 智能版本"""
    
    def __init__(self):
        self.name = "选题策划师"
        self.role = "小红书内容策划专家，擅长发现热点话题和用户痛点"
        
        # 默认选题分类
        self.categories = [
            "武汉本地生活",
            "贷款金融知识", 
            "早餐美食推荐",
            "热点话题分析"
        ]
    
    async def generate_topics(self, preferences: list, count: int = 5) -> list:
        """根据用户偏好生成选题列表
        
        Args:
            preferences: 用户偏好列表，如 ["武汉早餐", "贷款知识"]
            count: 生成数量
            
        Returns:
            选题列表，每项包含 id, title, category, tags, hook, outline
        """
        topics = []
        
        for i in range(count):
            category = preferences[i % len(preferences)] if preferences else "生活"
            
            # 根据分类生成对应选题
            if "早餐" in category or "武汉" in category:
                title = self._get_breakfast_topic(i)
            elif "贷款" in category or "金融" in category:
                title = self._get_loan_topic(i)
            else:
                title = self._get_lifestyle_topic(i)
            
            topics.append({
                "id": f"topic_{i+1:03d}",
                "title": title,
                "category": category,
                "tags": self._get_tags(category),
                "hook": self._generate_hook(title),
                "outline": self._generate_outline(title),
                "source": "ai_generate"  # 数据来源
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

# 兼容接口
async def generate_topics(preferences: list, count: int = 5) -> list:
    planner = TopicPlanner()
    return await planner.generate_topics(preferences, count)

__all__ = ["TopicPlanner", "generate_topics"]
