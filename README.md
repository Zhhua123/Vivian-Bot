# 🦋 Vivian - 薇薇安 (Gemini Telegram Bot)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Zeabur](https://img.shields.io/badge/Deploy-Zeabur-purple?style=for-the-badge&logo=zeabur&logoColor=white)

<h3> 🤖 全能型 · 毒舌系 · 群管机器人 </h3>

</div>

---

## 👶 小白必读：怎么让它跑起来？

**千万不要直接改代码里的 `main.py`！**
这是一个开源项目，为了安全，我们不把密码写在代码里。请按照下面的步骤，把密码填在 **Zeabur 的设置**里。

### 第一步：一键部署
1. 点击右上角的 **Fork** 按钮，把这个项目复制到你的 GitHub。
2. 登录 [Zeabur](https://zeabur.com)，点击 **Create Project**。
3. 选择 **Deploy New Service** -> **Git** -> 选中你刚才 Fork 的 `Vivian-Bot`。
4. 点击 **Deploy**。

### 第二步：填入密码 (最关键！)
部署后服务会报错（显示 Crash），这是正常的！因为你还没给它“钥匙”。
1. 在 Zeabur 点击你的服务卡片。
2. 点击顶部的 **Variables (变量)** 标签。
3. 点击 **Add Variable**，把下面这 3 个填进去：

| 变量名 (Key) | 填什么 (Value) | 例子 |
| :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | 你的机器人 Token (找 BotFather 要) | `123456:ABC-xxxx` |
| `GEMINI_API_KEYS` | 你的 Google Key (多个用逗号隔开) | `AIza1...,AIza2...` |
| `OWNER_ID` | 你的 Telegram ID (在那串数字) | `5016221686` |

**填完保存后，Zeabur 会自动重启，机器人就复活了！**

---

## ✨ 核心功能
* **🧠 聪明**: 11 个 Key 轮流用，不会被封号。
* **🗣️ 会说**: 发送 `/sing` 让她唱歌，或者发语音给她。
* **👀 会看**: 发表情包或图片，她能看懂并吐槽。
* **👑 会管**: 支持 `/ti` (踢人), `/jy` (禁言)。

## 📝 指令大全
| 指令 | 作用 |
| :--- | :--- |
| `/ms` | 切换 **话痨/高冷** 模式 |
| `/act [人设]` | 变身 (例: `/act 猫娘`) |
| `/sing [歌名]` | 让她 Rap 一首 |
| `/ti` | 踢人 (回复某人) |
| `/cw` | 重置记忆 |

## 📄 开源协议
MIT License
