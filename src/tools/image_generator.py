"""
小红书 Agent - 图片生成模块（调用本地渲染工具）
"""

import os
import subprocess
import tempfile
from datetime import datetime

class ImageGenerator:
    """图片生成 Agent - 集成本地渲染工具"""
    
    def __init__(self):
        self.name = "视觉设计师"
        self.v1_scripts_dir = os.path.expanduser("~/Projects/jiangzhui-xhs-v1/scripts")
        self.output_dir = os.path.expanduser("~/Projects/jiangzhui-xhs-v2/output")
        self.render_script = os.path.join(self.v1_scripts_dir, "render_xhs.py")
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate(self, content: dict, theme: str = "sketch", mode: str = "auto-split") -> dict:
        """生成小红书图片
        
        调用本地 render_xhs.py 脚本进行渲染
        """
        title = content.get('title', '无标题')
        text_content = content.get('content', '')
        
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
                 '--mode', mode,
                 '--output-dir', output_subdir],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            success = result.returncode == 0
            
            if success:
                # 查找生成的图片
                images = []
                for f in os.listdir(output_subdir):
                    if f.endswith('.png'):
                        images.append(os.path.join(output_subdir, f))
                
                return {
                    "status": "success",
                    "theme": theme,
                    "mode": mode,
                    "markdown_file": md_path,
                    "output_dir": output_subdir,
                    "images": sorted(images),
                    "image_count": len(images)
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr,
                    "markdown_file": md_path
                }
                
        except subprocess.TimeoutExpired:
            return {
                "status": "error",
                "error": "渲染超时"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_available_themes(self) -> list:
        """获取可用主题"""
        return [
            {"id": "default", "name": "默认风格", "desc": "紫色渐变"},
            {"id": "playful-geometric", "name": "活泼几何", "desc": "Memphis 设计风格"},
            {"id": "neo-brutalism", "name": "新粗野主义", "desc": "大胆鲜明"},
            {"id": "botanical", "name": "植物园风格", "desc": "自然清新"},
            {"id": "professional", "name": "专业商务", "desc": "简洁正式"},
            {"id": "retro", "name": "复古风格", "desc": "怀旧色调"},
            {"id": "terminal", "name": "终端风格", "desc": "命令行风格"},
            {"id": "sketch", "name": "手绘素描", "desc": "米白纸网格背景"}
        ]
    
    def get_available_modes(self) -> list:
        """获取可用分页模式"""
        return [
            {"id": "separator", "name": "分隔符模式", "desc": "按 --- 分隔符手动分页"},
            {"id": "auto-fit", "name": "自动缩放", "desc": "自动缩放文字以填满固定尺寸"},
            {"id": "auto-split", "name": "自动切分", "desc": "根据内容高度自动切分"},
            {"id": "dynamic", "name": "动态高度", "desc": "根据内容动态调整高度"}
        ]

__all__ = ["ImageGenerator"]
