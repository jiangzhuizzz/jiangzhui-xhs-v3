"""
小红书 Agent - 违禁词检测模块
支持：自动检测 + 自动替换 + 定期更新
"""

import json
import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ComplianceChecker:
    """合规审查 Agent"""
    
    def __init__(self,词库路径: str = None):
        self.name = "合规审查官"
        self.词库路径 = 词库路径 or "src/data/word_library.json"
        self.词库 = self._加载词库()
        self.last_update = getattr(self.词库, 'last_update', None)
    
    def _加载词库(self) -> dict:
        """加载词库，如果没有则创建默认词库"""
        default_words = {
            "version": "2026.03.20",
            "last_update": datetime.now().isoformat(),
            "forbidden_words": [
                {"word": "最便宜", "replacement": "比较实惠", "category": "绝对化用语"},
                {"word": "最划算", "replacement": "很划算", "category": "绝对化用语"},
                {"word": "第一", "replacement": "领先", "category": "绝对化用语"},
                {"word": "顶级", "replacement": "高品质", "category": "绝对化用语"},
                {"word": "绝对", "replacement": "非常", "category": "绝对化用语"},
                {"word": "100%", "replacement": "很高比例", "category": "绝对化用语"},
                {"word": "保证", "replacement": "确保", "category": "承诺用语"},
                {"word": "稳赚", "replacement": "有保障", "category": "承诺用语"},
                {"word": "包过", "replacement": "有把握", "category": "承诺用语"},
                {"word": "秒批", "replacement": "快速审批", "category": "承诺用语"}
            ],
            "sensitive_words": [
                {"word": "投资", "replacement": "理财", "category": "金融风险"},
                {"word": "赌博", "replacement": "娱乐", "category": "政策风险"},
                {"word": "彩票", "replacement": "抽奖", "category": "政策风险"},
                {"word": "代购", "replacement": "采购", "category": "政策风险"},
                {"word": "高仿", "replacement": "相似款", "category": "侵权风险"},
                {"word": "黑户", "replacement": "信用受损", "category": "金融风险"}
            ]
        }
        
        # 如果词库文件存在，读取它
        if os.path.exists(self.词库路径):
            try:
                with open(self.词库路径, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 保存默认词库
        self._保存词库(default_words)
        return default_words
    
    def _保存词库(self, 词库: dict):
        """保存词库到文件"""
        os.makedirs(os.path.dirname(self.词库路径), exist_ok=True)
        with open(self.词库路径, 'w', encoding='utf-8') as f:
            json.dump(词库, f, ensure_ascii=False, indent=2)
    
    async def check(self, content: str) -> dict:
        """检查内容合规性
        
        Args:
            content: 待检测文本
            
        Returns:
            检测结果字典
        """
        issues = []
        warnings = []
        
        # 获取词库
        forbidden = self.词库.get('forbidden_words', [])
        sensitive = self.词库.get('sensitive_words', [])
        
        # 检查违禁词
        for item in forbidden:
            if item['word'] in content:
                issues.append({
                    "type": "forbidden",
                    "word": item['word'],
                    "category": item.get('category', '未知'),
                    "replacement": item.get('replacement', '')
                })
        
        # 检查敏感词
        for item in sensitive:
            if item['word'] in content:
                warnings.append({
                    "type": "sensitive",
                    "word": item['word'],
                    "category": item.get('category', '未知'),
                    "replacement": item.get('replacement', '')
                })
        
        # 风险评估
        risk_level = "high" if issues else "medium" if warnings else "low"
        
        return {
            "status": "pass" if not issues else "fail",
            "risk_level": risk_level,
            "issues": issues,
            "warnings": warnings,
            "suggestions": self._get_suggestions(issues, warnings),
            "version": self.词库.get('version', 'unknown')
        }
    
    async def auto_fix(self, content: str) -> dict:
        """自动修复问题内容
        
        Args:
            content: 原始内容
            
        Returns:
            修复后的内容 + 检测报告
        """
        # 先检测
        check_result = await self.check(content)
        
        # 自动替换
        fixed = content
        all_replacements = []
        
        for item in self.词库.get('forbidden_words', []) + self.词库.get('sensitive_words', []):
            if item['word'] in fixed:
                replacement = item.get('replacement', '')
                if replacement:
                    fixed = fixed.replace(item['word'], replacement)
                    all_replacements.append({
                        "from": item['word'],
                        "to": replacement
                    })
        
        return {
            "original": content,
            "fixed": fixed,
            "replacements": all_replacements,
            "check_result": check_result
        }
    
    async def update_library(self, source: str = "remote") -> dict:
        """更新词库
        
        TODO: 接入第三方 API 定期更新词库
        
        Args:
            source: 词库来源 ("remote" / "manual")
            
        Returns:
            更新结果
        """
        # TODO: 从远程 API 获取最新词库
        # 示例: new_words = await fetch_remote_words()
        
        # 目前只更新版本号
        self.词库['version'] = datetime.now().strftime("%Y.%m.%d")
        self.词库['last_update'] = datetime.now().isoformat()
        self._保存词库(self.词库)
        
        return {
            "status": "success",
            "version": self.词库['version'],
            "last_update": self.词库['last_update']
        }
    
    def _get_suggestions(self, issues: list, warnings: list) -> list:
        """获取修改建议"""
        suggestions = []
        
        if issues:
            suggestions.append("⚠️ 发现违禁词，请移除或替换")
        
        if warnings:
            suggestions.append("⚡ 发现敏感词，建议谨慎使用")
        
        if not suggestions:
            suggestions.append("✅ 内容合规性良好，可以发布")
        
        return suggestions

__all__ = ["ComplianceChecker"]
