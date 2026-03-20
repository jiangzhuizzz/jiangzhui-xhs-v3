"""
小红书 Agent - 图片生成模块（混合方案）
支持：本地渲染 + baoyu-xhs-images + 外部API
"""

import os
import subprocess
import json
from datetime import datetime
from typing import Dict, List, Optional

class ImageGenerator:
    """图片生成 Agent - 混合方案"""
    
    def __init__(self, config: dict = None):
        self.name = "视觉设计师"
        self.config = config or {}
        
        # 路径配置
        self.v1_scripts_dir = os.path.expanduser("~/Projects/jiangzhui-xhs-v1/scripts")
        self.render_script = os.path.join(self.v1_scripts_dir, "render_xhs.py")
        self.output_dir = os.path.expanduser("~/Projects/jiangzhui-xhs-v2/output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 贷款中介自媒体风格映射
        self.style_mapping = {
            "贷款干货": {"engine": "local", "theme": "sketch"},
            "公积金": {"engine": "local", "theme": "sketch"},
            "信用贷": {"engine": "local", "theme": "professional"},
            "抵押贷": {"engine": "local", "theme": "professional"},
            "利率": {"engine": "local", "theme": "sketch"},
            "武汉": {"engine": "local", "theme": "sketch"},
            "早餐": {"engine": "baoyu", "style": "cute"},
            "生活": {"engine": "baoyu", "style": "fresh"},
            "情感": {"engine": "baoyu", "style": "cute"},
            "案例": {"engine": "baoyu", "style": "comic"},
            "默认": {"engine": "local", "theme": "sketch"}
        }
    
    async def generate(self, content: dict, force_engine: str = None, force_theme: str = None) -> dict:
        """生成小红书图片
        
        Args:
            content: 包含 title, content, category 等
            force_engine: 强制使用某引擎 (local/baoyu)
            force_theme: 强制使用某主题
            
        Returns:
            生成结果
        """
        title = content.get('title', '无标题')
        text_content = content.get('content', '')
        category = content.get('category', '默认')
        
        # 自动判断风格
        style_config = self._get_style_config(category, text_content)
        
        # 允许覆盖
        engine = force_engine or style_config.get('engine', 'local')
        theme = force_theme or style_config.get('theme', 'sketch')
        
        if engine == "local":
            return await self._generate_local(title, text_content, theme)
        elif engine == "baoyu":
            return await self._generate_baoyu(title, text_content, style_config.get('style', 'cute'))
        else:
            return await self._generate_local(title, text_content, 'sketch')
    
    def _get_style_config(self, category: str, text_content: str = "") -> dict:
        """根据内容类型自动判断风格配置"""
        # 检查关键词匹配
        combined_text = f"{category} {text_content}"
        
        for keyword, config in self.style_mapping.items():
            if keyword in combined_text:
                return config
        
        return self.style_mapping["默认"]
    
    async def _generate_local(self, title: str, text_content: str, theme: str) -> dict:
        """本地渲染方案"""
        # 创建临时 markdown 文件
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_title = title[:30].replace('/', '-').replace(' ', '-')
        md_filename = f"{timestamp}-{safe_title}.md"
        md_path = os.path.join(self.output_dir, md_filename)
        
        # 写入 markdown 内容
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(text_content)
        
        # 调用渲染脚本
        output_subdir = os.path.join(self.output_dir, f"{timestamp}-{safe_title}")
        
        try:
            result = subprocess.run(
                ['python3', self.render_script, md_path, 
                 '--theme', theme, 
                 '--mode', 'auto-split',
                 '--output-dir', output_subdir],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                images = [os.path.join(output_subdir, f) 
                         for f in os.listdir(output_subdir) if f.endswith('.png')]
                return {
                    "status": "success",
                    "engine": "local",
                    "theme": theme,
                    "output_dir": output_subdir,
                    "images": sorted(images),
                    "image_count": len(images)
                }
            else:
                return {
                    "status": "error",
                    "engine": "local",
                    "error": result.stderr
                }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    async def _generate_baoyu(self, title: str, text_content: str, style: str) -> dict:
        """baoyu-xhs-images 方案
        
        TODO: 接入 baoyu API
        目前返回提示信息
        """
        return {
            "status": "pending",
            "engine": "baoyu",
            "style": style,
            "message": "baoyu 图像生成待配置 API Key",
            "suggestion": "请配置图像生成 API 后使用"
        }
    
    def get_available_themes(self) -> list:
        """获取本地可用主题"""
        return [
            {"id": "sketch", "name": "手绘素描", "desc": "米白纸网格背景"},
            {"id": "default", "name": "默认风格", "desc": "紫色渐变"},
            {"id": "playful-geometric", "name": "活泼几何", "desc": "Memphis 设计"},
            {"id": "neo-brutalism", "name": "新粗野主义", "desc": "大胆鲜明"},
            {"id": "botanical", "name": "植物园风格", "desc": "自然清新"},
            {"id": "professional", "name": "专业商务", "desc": "简洁正式"},
            {"id": "retro", "name": "复古风格", "desc": "怀旧色调"},
            {"id": "terminal", "name": "终端风格", "desc": "命令行风格"}
        ]
    
    def get_style_recommendation(self, category: str) -> dict:
        """获取风格推荐"""
        return self._get_style_config(category)

__all__ = ["ImageGenerator"]
