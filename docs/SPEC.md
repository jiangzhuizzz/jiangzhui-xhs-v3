# 小红书 AI 运营助手 (jiangzhui-xhs-v2) - 技术规格文档

**版本**: v1.0.0  
**日期**: 2026-03-20  
**作者**: 江sir  

---

## 1. 项目概述

### 1.1 产品定位

一款基于多 Agent 协作的小红书内容运营自动化工具，支持从选题、创作、检测到发布的全流程自动化。

### 1.2 目标用户

| 阶段 | 用户群体 |
|:---|:---|
| v1.0 | 开发者、极客、自动化爱好者 |
| v1.5 | 个人小红书博主 |
| v2.0 | MCN 机构、内容团队 |

### 1.3 商业模式

```
v1.0 (开源免费)
    ↓
v1.5 (标准化 SOP 模板付费)
    ↓
v2.0 (SaaS 订阅制)
```

---

## 2. 技术架构

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户层 (Telegram/Web)                  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    调度层 (CrewAI/自定义)                    │
└─────────────────────────────────────────────────────────────┘
          ↓            ↓            ↓            ↓
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│  选题Agent │  │  文案Agent │  │  检测Agent │  │  发布Agent │
└────────────┘  └────────────┘  └────────────┘  └────────────┘
          ↓            ↓            ↓            ↓
┌─────────────────────────────────────────────────────────────┐
│                      工具层                                  │
├──────────┬──────────┬──────────┬──────────┬──────────────────┤
│ 热点API │  LLM API│ 词库检测 │ 生图引擎 │  小红书发布API   │
└──────────┴──────────┴──────────┴──────────┴──────────────────┘
```

### 2.2 技术栈

| 层级 | 技术选型 |
|:---|:---|
| 调度框架 | CrewAI / 自定义多Agent框架 |
| LLM | Claude / Gemini / MiniMax (可切换) |
| 生图 | 本地渲染 / baoyu-xhs-images / 外部API |
| 存储 | SQLite / JSON 文件 |
| 部署 | Docker / OpenClaw Skill |

---

## 3. 功能模块规格

### 3.1 核心流程 (5 大环节)

#### 环节 1: 智能选题

| 功能 | 说明 |
|:---|:---|
| 输入 | 用户偏好（关键词/分类） |
| 输出 | 5-10 个选题建议 |
| 数据源 | 热点API / 知识库 / 用户历史 |
| 智能化 | 基于用户历史选择推荐 |

#### 环节 2: 文案生成

| 功能 | 说明 |
|:---|:---|
| 输入 | 选题 + 风格偏好 |
| 输出 | 标题 3 个 + 正文 1 篇 |
| LLM | Claude/Gemini/MiniMax (可配置) |
| 风格 | 口语化、emoji、段落式 |

#### 环节 3: 违禁词检测

| 功能 | 说明 |
|:---|:---|
| 检测 | 违禁词 + 敏感词 + 风险词 |
| 自动修复 | 智能替换为合规词汇 |
| 词库更新 | 定期从网络获取最新词库 |
| 词库格式 | JSON: {word, replacement, category} |

#### 环节 4: 图片生成 (混合方案)

| 方案 | 触发条件 | 说明 |
|:---|:---|:---|
| 本地渲染 | 默认 | 调用 render_xhs.py，支持 8 种主题 |
| baoyu-xhs-images | 需要AI生图时 | 卡通风格，需要 API |
| 外部API | 可选 | DALL-E/Midjourney |

#### 环节 5: 自动发布

| 功能 | 说明 |
|:---|:---|
| 目标 | 小红书草稿箱 |
| 方式 | OpenClaw 浏览器自动化 |
| 定时 | 支持定时发布 |

---

### 3.2 扩展功能 (v1.5+)

| 功能 | 说明 |
|:---|:---|
| 热点追踪 | 自动抓取小红书热门话题 |
| 数据分析 | 阅读/点赞/收藏统计 |
| 评论回复 | AI 自动回复 |
| 多账号 | 同时运营多账号 |

---

## 4. 数据结构

### 4.1 选题数据结构

```python
{
    "id": "topic_001",
    "title": "武汉人过早指南：这5家早餐店",
    "category": "美食",
    "tags": ["#武汉", "#过早", "#美食"],
    "hook": "说出来你可能不信...",
    "outline": {
        "开头": "痛点引入 + 悬念设置",
        "中间": "3-5个要点 + 案例分享",
        "结尾": "总结 + 互动引导"
    }
}
```

### 4.2 词库数据结构

```python
{
    "version": "2026.03.20",
    "forbidden_words": [
        {"word": "最便宜", "replacement": "比较实惠"},
        {"word": "保证", "replacement": "确保"},
        {"word": "100%", "replacement": "很高比例"}
    ],
    "sensitive_words": [
        {"word": "投资", "category": "金融风险"},
        {"word": "代购", "category": "政策风险"}
    ]
}
```

---

## 5. 配置说明

### 5.1 环境变量

```bash
# LLM 配置 (至少选择一种)
CLAUDE_API_KEY=sk-xxx
GEMINI_API_KEY=xxx
MINIMAX_API_KEY=xxx

# 小红书配置
XHS_COOKIE=xxx
XHS_CREATOR_TOKEN=xxx

# 生图配置
IMAGE_ENGINE=local  # local / baoyu / external
```

### 5.2 配置文件

```yaml
# config.yaml
llm:
  default: claude
  fallback: [gemini, minimax]

image:
  default_engine: local
  theme: sketch
  size: "1080x1440"

compliance:
  auto_fix: true
  update_interval: 7  # 天

publish:
  target: draft  # draft / publish
```

---

## 6. 部署方式

### 6.1 OpenClaw Skill 形式 (v1.0)

```
~/.openclaw/agents/xhs-agent/
├── SOUL.md
├── bot.py
├── config.yaml
└── src/
    ├── agents/
    ├── tools/
    └── workflows/
```

### 6.2 Docker 形式 (v2.0)

```yaml
# docker-compose.yml
services:
  xhs-agent:
    image: jiangzhui/xhs-agent:latest
    volumes:
      - ./config.yaml:/app/config.yaml
    environment:
      - CLAUDE_API_KEY=${CLAUDE_API_KEY}
```

---

## 7. 开发计划

### Phase 1: 核心功能 (MVP)

| 任务 | 优先级 | 状态 |
|:---|:---:|:---:|
| 基础框架搭建 | P0 | ⏳ |
| 选题模块 | P0 | ⏳ |
| 文案生成模块 (Claude) | P0 | ⏳ |
| 违禁词检测 + 自动修复 | P0 | ⏳ |
| 本地生图集成 | P0 | ⏳ |
| 发布到草稿箱 | P0 | ⏳ |

### Phase 2: 增强功能

| 任务 | 优先级 | 状态 |
|:---|:---:|:---:|
| 多模型支持 (Gemini/MiniMax) | P1 | ☐ |
| baoyu-xhs-images 集成 | P1 | ☐ |
| 词库自动更新 | P1 | ☐ |
| 热点追踪 | P2 | ☐ |

### Phase 3: 商业化

| 任务 | 优先级 | 状态 |
|:---|:---:|:---:|
| SOP 模板化 | P2 | ☐ |
| Web 管理后台 | P2 | ☐ |
| 多账号管理 | P3 | ☐ |
| 数据分析 | P3 | ☐ |

---

## 8. 参考资料

- awesome-openclaw-agents: https://github.com/mergisi/awesome-openclaw-agents
- CrewAI 文档: https://docs.crewai.com
- baoyu-xhs-images: 本地安装

---

*文档版本: v1.0.0 | 最后更新: 2026-03-20*
