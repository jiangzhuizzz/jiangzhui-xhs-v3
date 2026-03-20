"""
配置管理模块
"""

import os
import json
from typing import Dict, Any, Optional

class Config:
    """配置管理"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self._config = self._load_config()
    
    def _load_config(self) -> dict:
        """加载配置"""
        default = self._default_config()
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # 合并配置
                default.update(user_config)
        
        return default
    
    def _default_config(self) -> dict:
        """默认配置"""
        return {
            # CLI Proxy API
            "cli_proxy_url": "http://localhost:8317",
            "cli_proxy_key": "",
            
            # LLM 配置
            "default_llm": "minimax",
            "fallback_llm": "claude",
            "minimax_model": "MiniMax-M2.5",
            "claude_model": "claude-sonnet-4.5",
            
            # 图像生成
            "image_engine": "local",
            "local_render_script": os.path.expanduser("~/Projects/jiangzhui-xhs-v1/scripts/render_xhs.py"),
            "default_theme": "sketch",
            "baoyu_api_key": "",
            
            # 飞书配置
            "feishu_app_id": "",
            "feishu_app_secret": "",
            "feishu_table_id": "",
            "feishu_webhook": "",
            
            # 词库配置
            "word_library_path": "src/data/word_library.json",
            "word_library_update_url": "",
            "auto_update_interval": 7,
            
            # 发布配置
            "max_posts_per_day": 2,
            "min_interval_hours": 4,
            "default_publish_time": "12:00"
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置"""
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """设置配置"""
        self._config[key] = value
    
    def save(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
    
    def to_dict(self) -> dict:
        """转为字典"""
        return self._config.copy()

__all__ = ["Config"]
