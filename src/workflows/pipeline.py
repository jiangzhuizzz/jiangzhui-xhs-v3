"""
小红书 Agent - 完整工作流
整合：选题 → 文案 → 违禁词检测 → 图片生成 → 发布
"""

import asyncio
from src.agents import TopicPlanner
from src.agents.copywriter import Copywriter
from src.tools.compliance import ComplianceChecker
from src.tools.image_generator import ImageGenerator
from src.tools.publisher import Publisher

class XHSPipeline:
    """小红书内容生成完整流水线"""
    
    def __init__(self):
        self.topic_planner = TopicPlanner()
        self.copywriter = Copywriter()
        self.compliance_checker = ComplianceChecker()
        self.image_generator = ImageGenerator()
        self.publisher = Publisher()
    
    async def run(self, preferences: list, auto_publish: bool = False) -> dict:
        """执行完整流水线
        
        Args:
            preferences: 选题偏好列表
            auto_publish: 是否自动发布
            
        Returns:
            完整流程结果
        """
        result = {
            "steps": {},
            "status": "running"
        }
        
        # Step 1: 选题
        print("📌 Step 1: 智能选题...")
        topics = await self.topic_planner.generate_topics(preferences, count=3)
        result["steps"]["topic"] = topics[0]
        print(f"   ✓ 选题: {topics[0]['title']}")
        
        # Step 2: 文案生成
        print("✍️ Step 2: 生成文案...")
        post = await self.copywriter.write_post(topics[0])
        result["steps"]["copywriting"] = post
        print(f"   ✓ 字数: {post['word_count']}")
        
        # Step 3: 违禁词检测
        print("🔍 Step 3: 违禁词检测...")
        check_result = await self.compliance_checker.check(post['content'])
        result["steps"]["compliance"] = check_result
        print(f"   ✓ 状态: {check_result['status']} | 风险: {check_result['risk_level']}")
        
        # 如果有违禁词，自动修复
        if check_result["status"] == "fail":
            print("   ⚠️ 发现违禁词，自动修复中...")
            fix_result = await self.compliance_checker.auto_fix(post['content'])
            post['content'] = fix_result["fixed"]
            result["steps"]["compliance"]["fixed"] = fix_result
            print(f"   ✓ 已修复: {len(fix_result['replacements'])} 处")
        
        # Step 4: 图片生成
        print("🎨 Step 4: 生成图片...")
        image_result = await self.image_generator.generate({
            "title": post['titles'][0],
            "content": post['content'],
            "category": topics[0]["category"]
        })
        result["steps"]["image"] = image_result
        print(f"   ✓ 引擎: {image_result.get('engine', 'local')}")
        print(f"   ✓ 图片: {image_result.get('image_count', 0)} 张")
        
        # Step 5: 发布
        if auto_publish:
            print("📤 Step 5: 发布到草稿箱...")
            can_pub = self.publisher.can_publish()
            
            if can_pub["can_publish"]:
                publish_result = await self.publisher.publish({
                    "title": post['titles'][0],
                    "content": post['content'],
                    "images": image_result.get("images", []),
                    "tags": post['tags']
                })
                result["steps"]["publish"] = publish_result
                print(f"   ✓ 状态: {publish_result['status']}")
            else:
                result["steps"]["publish"] = {"status": "skipped", "reason": can_pub["reason"]}
                print(f"   ⊘ 跳过: {can_pub['reason']}")
        
        result["status"] = "completed"
        return result

__all__ = ["XHSPipeline"]
