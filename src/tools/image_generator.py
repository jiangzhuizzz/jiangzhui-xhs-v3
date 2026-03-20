"""
小红书 Agent - 图片生成模块
"""

import os

class ImageGenerator:
    """图片生成 Agent"""
    
    def __init__(self):
        self.name = "视觉设计师"
        self.output_dir = os.path.expanduser("~/Projects/jiangzhui-xhs-v2/output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate(self, content: dict, theme: str = "sketch") -> dict:
        """生成小红书图片
        
        主题选项:
        - sketch: 手绘风格
        - minimalist: 极简风格
        - comic: 漫画风格
        - vintage: 复古风格
        """
        title = content.get('title', '无标题')
        text_content = content.get('content', '')[:500]
        
        # 调用本地已有的渲染脚本
        # 这里生成一个模拟结果，实际会调用 render_xhs.py
        
        result = {
            "status": "success",
            "theme": theme,
            "cover_image": f"{self.output_dir}/cover.png",
            "content_images": [
                f"{self.output_dir}/content_1.png"
            ],
            "metadata": {
                "title": title,
                "theme": theme,
                "size": "1080x1440"
            }
        }
        
        return result
    
    def get_available_themes(self) -> list:
        """获取可用主题"""
        return [
            {"id": "sketch", "name": "手绘风格", "desc": "素描手绘效果"},
            {"id": "minimalist", "name": "极简风格", "desc": "简洁大方"},
            {"id": "comic", "name": "漫画风格", "desc": "卡通趣味"},
            {"id": "vintage", "name": "复古风格", "desc": "怀旧色调"},
            {"id": "paper", "name": "纸张风格", "desc": "米白纸网格背景"},
            {"id": "dark", "name": "暗黑风格", "desc": "深色背景"}
        ]

__all__ = ["ImageGenerator"]
