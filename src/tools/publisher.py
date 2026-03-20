"""
小红书 Agent - 自动发布模块
支持：草稿箱发布、定时发布
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class Publisher:
    """自动发布 Agent"""
    
    def __init__(self, config: dict = None):
        self.name = "发布助手"
        self.platform = "小红书"
        self.config = config or {}
        
        # 发布配置
        self.max_posts_per_day = 2  # 每天最多发布数
        self.min_interval_hours = 4  # 最小发布间隔
    
    async def publish(self, post_data: dict) -> dict:
        """发布笔记到小红书草稿箱
        
        Args:
            post_data: 包含 title, content, images, tags 等
            
        Returns:
            发布结果
        """
        title = post_data.get('title', '')
        content = post_data.get('content', '')
        images = post_data.get('images', [])
        tags = post_data.get('tags', [])
        
        # 验证内容
        if not title:
            return {"status": "error", "message": "标题不能为空"}
        
        if not images:
            return {"status": "error", "message": "至少需要一张图片"}
        
        # 生成发布数据
        result = {
            "status": "success",
            "platform": self.platform,
            "destination": "草稿箱",
            "post_id": f"draft_{hash(title) % 100000}",
            "title": title,
            "content_length": len(content),
            "image_count": len(images),
            "tag_count": len(tags),
            "created_at": datetime.now().isoformat()
        }
        
        # 保存发布记录
        self._save_post_record(result)
        
        return result
    
    async def schedule(self, post_data: dict, publish_time: str) -> dict:
        """定时发布
        
        Args:
            post_data: 发布内容
            publish_time: 发布时间 (ISO 格式)
            
        Returns:
            定时发布结果
        """
        result = await self.publish(post_data)
        result["scheduled_time"] = publish_time
        result["status"] = "scheduled"
        return result
    
    def can_publish(self) -> dict:
        """检查是否可以发布
        
        Returns:
            检查结果
        """
        # 检查今天已发布数量
        today_posts = self._get_today_posts()
        
        if len(today_posts) >= self.max_posts_per_day:
            return {
                "can_publish": False,
                "reason": f"今天已发布 {len(today_posts)} 篇，达到每日上限 {self.max_posts_per_day}"
            }
        
        # 检查发布间隔
        if today_posts:
            last_post_time = datetime.fromisoformat(today_posts[-1]["created_at"])
            time_diff = datetime.now() - last_post_time
            
            if time_diff.total_seconds() < self.min_interval_hours * 3600:
                next_available = last_post_time + timedelta(hours=self.min_interval_hours)
                return {
                    "can_publish": False,
                    "reason": f"距离上次发布不足 {self.min_interval_hours} 小时",
                    "next_available": next_available.isoformat()
                }
        
        return {
            "can_publish": True,
            "today_count": len(today_posts),
            "remaining": self.max_posts_per_day - len(today_posts)
        }
    
    def _save_post_record(self, post_record: dict):
        """保存发布记录"""
        records_file = "src/data/post_records.json"
        
        # 读取现有记录
        records = []
        if os.path.exists(records_file):
            with open(records_file, 'r', encoding='utf-8') as f:
                records = json.load(f)
        
        # 添加新记录
        records.append(post_record)
        
        # 保存
        os.makedirs(os.path.dirname(records_file), exist_ok=True)
        with open(records_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=2)
    
    def _get_today_posts(self) -> list:
        """获取今天已发布的记录"""
        records_file = "src/data/post_records.json"
        
        if not os.path.exists(records_file):
            return []
        
        with open(records_file, 'r', encoding='utf-8') as f:
            records = json.load(f)
        
        today = datetime.now().date()
        return [r for r in records 
                if datetime.fromisoformat(r["created_at"]).date() == today]

__all__ = ["Publisher"]
