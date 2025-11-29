# 🦋 Vivian - 薇薇安 (Gemini Telegram Bot)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange.svg?style=for-the-badge&logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Bot-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Zeabur](https://img.shields.io/badge/Deploy-Zeabur-purple?style=for-the-badge&logo=zeabur&logoColor=white)

<h3> 🤖 全能型 · 毒舌系 · 群管机器人 </h3>

<p>
  <a href="#-核心特性-features">核心特性</a> •
  <a href="#-部署到-zeabur-推荐">⚡ 一键部署</a> •
  <a href="#-指令列表-commands">指令列表</a>
</p>

</div>

---

> **"哼，居然还要本小姐亲自来教你部署？"**
> 
> 一个基于 **Google Gemini 2.5 Flash** 的全能型 Telegram 群管机器人。
> 她拥有**傲娇毒舌**的独立人格，支持 **11 Key 负载均衡**、**多模态交互**、**语音通话**及**铁腕群管**功能。
> 
> **专为免费容器 (如 Zeabur) 优化，不休眠，响应快。**

## ✨ 核心特性 (Features)

| 模块 | 功能描述 |
| :--- | :--- |
| **🧠 超强大脑** | 集成 Gemini 2.5，内置 **11 Key 轮询池**，自动处理限流，保证 24/7 在线。 |
| **🎭 沉浸人设** | 默认“傲娇毒舌”性格，支持 `/act` 指令随时变身猫娘、女仆或任何角色。 |
| **👑 铁腕群管** | 智能识别垃圾广告，执行“警告-禁言-踢出”三级制裁；支持 `/ti`, `/mute` 等快捷指令。 |
| **🗣️ 全感官交互** | **听**语音条、**看**图片表情包、**说** Edge-TTS 高清语音 (支持 Rap/朗诵)。 |
| **🛡️ 安全机制** | 私聊白名单（只服务主人），最高权限控制，防止额度被盗刷。 |

## ⚡ 部署到 Zeabur (推荐)

本项目完美适配 **Zeabur**，支持 Docker 一键构建，**完全免费**且**无需服务器**。

### 1. 准备工作
* Fork 本仓库到你的 GitHub。
* 注册/登录 [Zeabur](https://zeabur.com)。

### 2. 开始部署
1. 进入 Zeabur 控制台，点击 **Create Project**。
2. 点击 **Deploy New Service** -> 选择 **Git**。
3. 选中你 Fork 的 `Vivian-Bot` 仓库。
4. 点击 **Deploy** (Zeabur 会自动识别 Dockerfile)。

### 3. 注入灵魂 (环境变量)
部署后服务会报错（因为没 Key），请点击服务卡片 -> **Variables**，添加以下变量：

| 变量名 (Key) | 必填 | 填入内容 (Value) | 示例 |
| :--- | :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | ✅ | 你的 Bot Token | `123456:ABC-xxx` |
| `GEMINI_API_KEYS` | ✅ | Gemini Key 池 (英文逗号分隔) | `AIza1...,AIza2...` |
| `OWNER_ID` | ✅ | 你的 Telegram ID (最高权限) | `5016221686` |
| `GROUP_LINK` | ❌ | 群组链接 (拒绝陌生人时展示) | `https://t.me/yourgroup` |

*保存变量后，Zeabur 会自动重启服务，看到绿色的 **Running** 即为成功！*

---

## 🛠️ 本地 / Docker 部署

如果你有自己的服务器 (VPS)，也可以直接运行：

```bash
# 1. 克隆仓库
git clone [https://github.com/你的用户名/Vivian-Bot.git](https://github.com/你的用户名/Vivian-Bot.git)

# 2. 构建镜像
docker build -t vivian-bot .

# 3. 运行容器
docker run -d \
  -e TELEGRAM_BOT_TOKEN="your_token" \
  -e GEMINI_API_KEYS="key1,key2,key3" \
  -e OWNER_ID=123456 \
  vivian-bot
