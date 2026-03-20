"""
小红书 Agent - 违禁词检测模块
"""

class ComplianceChecker:
    """合规审查 Agent"""
    
    def __init__(self):
        self.name = "合规审查官"
        # 小红书常见违禁词库（简化版）
        self.forbidden_words = [
            "最便宜", "最划算", "第一", "顶级", "国家级",
            "绝对", "100%", "保证", "稳赚", "包过",
            "秒批", "无条件", "黑户", "洗白", "代操作",
            "关系户", "内部渠道", "走后门", "有关系"
        ]
        
        self.sensitive_words = [
            "投资", "理财", "赌博", "彩票", "套现",
            "代购", "走私", "水货", "高仿", "A货"
        ]
    
    async def check(self, content: str) -> dict:
        """检查内容合规性"""
        issues = []
        warnings = []
        
        # 检查违禁词
        for word in self.forbidden_words:
            if word in content:
                issues.append(f"违禁词: '{word}'")
        
        # 检查敏感词
        for word in self.sensitive_words:
            if word in content:
                warnings.append(f"敏感词: '{word}' (建议谨慎使用)")
        
        # 检查敏感话题
        if "贷款" in content or "借款" in content:
            warnings.append("涉及金融话题，需确保有相关资质")
        
        # 风险评估
        risk_level = "high" if issues else "medium" if warnings else "low"
        
        return {
            "status": "pass" if not issues else "fail",
            "risk_level": risk_level,
            "issues": issues,
            "warnings": warnings,
            "suggestions": self._get_suggestions(issues, warnings)
        }
    
    def _get_suggestions(self, issues: list, warnings: list) -> list:
        """获取修改建议"""
        suggestions = []
        
        if issues:
            suggestions.append("请移除或替换违禁词汇")
            suggestions.append("避免使用绝对化用语")
        
        if warnings:
            suggestions.append("涉及敏感话题，请适度调整表达方式")
            suggestions.append("建议添加风险提示或免责声明")
        
        if not suggestions:
            suggestions.append("内容合规性良好，可以发布")
        
        return suggestions
    
    async def auto_fix(self, content: str) -> str:
        """自动修复问题内容"""
        fixed = content
        
        # 替换违禁词
        replacements = {
            "最便宜": "比较实惠",
            "最划算": "很划算",
            "第一": "领先",
            "顶级": "高品质",
            "绝对": "非常",
            "100%": "很高比例",
            "保证": "确保",
            "稳赚": "有保障",
            "包过": "有把握",
            "秒批": "快速审批"
        }
        
        for old, new in replacements.items():
            fixed = fixed.replace(old, new)
        
        return fixed

__all__ = ["ComplianceChecker"]
