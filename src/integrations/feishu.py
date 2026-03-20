"""
飞书集成模块
功能：多维表格管理、消息通知
"""

import os
import json
import asyncio
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime

class FeishuClient:
    """飞书客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expires_at = 0
    
    async def get_access_token(self) -> str:
        """获取 access_token"""
        now = datetime.now().timestamp()
        
        # 检查是否过期
        if self.access_token and now < self.token_expires_at:
            return self.access_token
        
        # 获取新 token
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                data = await resp.json()
                
                if data.get("code") == 0:
                    self.access_token = data["tenant_access_token"]
                    self.token_expires_at = now + data.get("expire", 7200) - 300
                    return self.access_token
                else:
                    raise Exception(f"获取 token 失败: {data}")
    
    async def create_bitable(self, app_token: str, table_name: str, fields: List[dict]) -> str:
        """创建多维表格"""
        token = await self.get_access_token()
        
        url = f"https://open.feishu.cn/open-apis/bitable/v1/databases/{app_token}/tables"
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {
            "table_name": table_name,
            "fields": fields
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                data = await resp.json()
                if data.get("code") == 0:
                    return data["data"]["table_id"]
                else:
                    raise Exception(f"创建表格失败: {data}")
    
    async def send_message(self, webhook: str, message: dict) -> bool:
        """发送消息"""
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook, json=message) as resp:
                return resp.status == 200

class FeishuManager:
    """飞书多维表格管理器"""
    
    # 表格字段定义
    TOPIC_FIELDS = [
        {"field_name": "选题标题", "field_type": "Text"},
        {"field_name": "选题分类", "field_type": "SingleSelect", 
         "options": ["贷款干货", "武汉生活", "案例分享", "热点蹭流"]},
        {"field_name": "优先级", "field_type": "SingleSelect",
         "options": ["高", "中", "低"]},
        {"field_name": "选题来源", "field_type": "SingleSelect",
         "options": ["AI生成", "热点追踪", "对标分析"]},
        {"field_name": "状态", "field_type": "SingleSelect",
         "options": ["待创作", "创作中", "已通过", "已废弃"]},
        {"field_name": "创建时间", "field_type": "DateTime"},
        {"field_name": "计划发布时间", "field_type": "DateTime"}
    ]
    
    CONTENT_FIELDS = [
        {"field_name": "笔记标题", "field_type": "Text"},
        {"field_name": "选题关联", "field_type": "Text"},
        {"field_name": "内容分类", "field_type": "SingleSelect",
         "options": ["贷款干货", "武汉生活", "案例分享", "热点蹭流"]},
        {"field_name": "正文内容", "field_type": "RichText"},
        {"field_name": "封面图", "field_type": "Attachment", "mime_type": "image/*"},
        {"field_name": "内容配图", "field_type": "Attachment", "mime_type": "image/*"},
        {"field_name": "话题标签", "field_type": "MultiSelect"},
        {"field_name": "状态", "field_type": "SingleSelect",
         "options": ["初稿", "待审核", "已发布"]},
        {"field_name": "发布平台", "field_type": "MultiSelect"},
        {"field_name": "笔记链接", "field_type": "Url"},
        {"field_name": "发布时间", "field_type": "DateTime"},
        {"field_name": "阅读量", "field_type": "Number"},
        {"field_name": "点赞数", "field_type": "Number"},
        {"field_name": "收藏数", "field_type": "Number"},
        {"field_name": "评论数", "field_type": "Number"}
    ]
    
    HOT_FIELDS = [
        {"field_name": "热点话题", "field_type": "Text"},
        {"field_name": "热度指数", "field_type": "Number"},
        {"field_name": "话题分类", "field_type": "SingleSelect"},
        {"field_name": "相关标签", "field_type": "MultiSelect"},
        {"field_name": "数据来源", "field_type": "Text"},
        {"field_name": "更新时间", "field_type": "DateTime"}
    ]
    
    COMPETITOR_FIELDS = [
        {"field_name": "账号名称", "field_type": "Text"},
        {"field_name": "账号ID", "field_type": "Text"},
        {"field_name": "平台", "field_type": "SingleSelect",
         "options": ["小红书", "抖音", "视频号"]},
        {"field_name": "粉丝数", "field_type": "Number"},
        {"field_name": "近期爆款笔记", "field_type": "Text"},
        {"field_name": "更新时间", "field_type": "DateTime"}
    ]
    
    ANALYTICS_FIELDS = [
        {"field_name": "日期", "field_type": "Date"},
        {"field_name": "新增粉丝", "field_type": "Number"},
        {"field_name": "总粉丝数", "field_type": "Number"},
        {"field_name": "发布笔记数", "field_type": "Number"},
        {"field_name": "曝光量", "field_type": "Number"},
        {"field_name": "阅读量", "field_type": "Number"},
        {"field_name": "互动率", "field_type": "Number"}
    ]
    
    def __init__(self, app_id: str, app_secret: str):
        self.client = FeishuClient(app_id, app_secret)
        self.app_token = None
    
    async def create_all_tables(self, app_token: str) -> dict:
        """创建所有表格"""
        self.app_token = app_token
        
        tables = {}
        
        # 1. 选题管理表
        tables["topic"] = await self.client.create_bitable(
            app_token, "选题管理", self.TOPIC_FIELDS)
        
        # 2. 内容管理表
        tables["content"] = await self.client.create_bitable(
            app_token, "内容管理", self.CONTENT_FIELDS)
        
        # 3. 热点数据表
        tables["hot"] = await self.client.create_bitable(
            app_token, "热点数据", self.HOT_FIELDS)
        
        # 4. 对标账号表
        tables["competitor"] = await self.client.create_bitable(
            app_token, "对标账号", self.COMPETITOR_FIELDS)
        
        # 5. 数据分析表
        tables["analytics"] = await self.client.create_bitable(
            app_token, "数据分析", self.ANALYTICS_FIELDS)
        
        return tables
    
    async def send_notification(self, webhook: str, title: str, message: str):
        """发送飞书通知"""
        msg = {
            "msg_type": "interactive_card",
            "card": {
                "header": {
                    "title": {"tag": "plain_text", "content": title},
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "markdown",
                        "content": message
                    }
                ]
            }
        }
        await self.client.send_message(webhook, msg)

__all__ = ["FeishuClient", "FeishuManager"]
