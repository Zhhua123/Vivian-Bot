# 🦋 Vivian - 薇薇安 (Gemini Telegram Bot)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange.svg?style=for-the-badge&logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Bot-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

<h3> 🤖 全能型 · 毒舌系 · 群管机器人 </h3>

<p>
  <a href="#-核心特性-features">核心特性</a> •
  <a href="#-快速部署-deploy">快速部署</a> •
  <a href="#-指令列表-commands">指令列表</a>
</p>

</div>

---

> **"哼，居然还要本小姐亲自来教你部署？"**
> 
> 一个基于 **Google Gemini 2.5 Flash** 的全能型 Telegram 群管机器人。
> 她拥有**傲娇毒舌**的独立人格，支持 **11 Key 负载均衡**、**多模态交互**、**语音通话**及**铁腕群管**功能。

## ✨ 核心特性 (Features)

| 模块 | 功能描述 |
| :--- | :--- |
| **🧠 超强大脑** | 集成 Gemini 2.5，内置 **11 Key 轮询池**，自动处理限流，保证 24/7 在线。 |
| **🎭 沉浸人设** | 默认“傲娇毒舌”性格，支持 `/act` 指令随时变身猫娘、女仆或任何角色。 |
| **👑 铁腕群管** | 智能识别垃圾广告，执行“警告-禁言-踢出”三级制裁；支持 `/ti`, `/mute` 等快捷指令。 |
| **🗣️ 全感官交互** | **听**语音条、**看**图片表情包、**说** Edge-TTS 高清语音 (支持 Rap/朗诵)。 |
| **🛡️ 安全机制** | 私聊白名单（只服务主人），最高权限控制，防止额度被盗刷。 |

## 🚀 快速部署 (Deploy)

推荐使用 **Zeabur** 或 **Docker** 进行一键部署。

### 1. 环境变量 (Environment Variables)

在部署平台设置以下变量：

| 变量名 | 必填 | 描述 | 示例 |
| :--- | :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | ✅ | 你的 Bot Token | `123456:ABC-xxx` |
| `GEMINI_API_KEYS` | ✅ | Gemini API Key 池 (逗号分隔) | `AIza1...,AIza2...,AIza3...` |
| `OWNER_ID` | ✅ | 机器人的主人 ID (最高权限) | `5016221686` |
| `GROUP_LINK` | ❌ | 群组链接 (用于拒绝陌生人时展示) | `https://t.me/yourgroup` |

### 2. 启动指令
```bash
python main.py
