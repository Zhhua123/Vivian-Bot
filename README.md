      # 🦋 Vivian - 薇薇安 (Gemini Telegram Bot)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5-orange.svg?style=for-the-badge&logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Bot-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Zeabur](https://img.shields.io/badge/Deploy-Zeabur-purple?style=for-the-badge&logo=zeabur&logoColor=white)

<h3> 🤖 全能型 · 毒舌系 · 群管机器人 </h3>

<p>
  <a href="#-核心特性-features">核心特性</a> •
  <a href="#-推荐部署-zeabur-免费--省心">⚡ 一键部署</a> •
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

---

## ⚡ 推荐部署: Zeabur (免费 & 省心)

本项目针对 **Zeabur** 容器平台进行了深度优化，**无需服务器，永不休眠**。

### 1. 准备工作
1. 点击右上角的 **Fork** 按钮，将本仓库复制到你的 GitHub 账号下。
2. 注册并登录 [Zeabur 官网](https://zeabur.com) (支持 GitHub 直接登录)。

### 2. 创建服务
1. 在 Zeabur 控制台点击 **Create Project** (创建项目)，选择一个地区（推荐 US 或 HK）。
2. 点击 **Deploy New Service** (部署新服务) -> 选择 **Git**。
3. 在列表中选中你刚才 Fork 的 `Vivian-Bot` 仓库。
4. 点击 **Deploy**。

### 3. 注入灵魂 (环境变量) 🔴 重要！
部署初期会显示 Crash (因为没填密码)，请不要惊慌：
1. 点击你刚刚创建的服务卡片。
2. 点击顶部的 **Variables (变量)** 标签。
3. 点击 **Add Variable**，依次添加以下 3 个必须的变量：

| 变量名 (Key) | 必填 | 填入内容 (Value) | 示例 |
| :--- | :--- | :--- | :--- |
| `TELEGRAM_BOT_TOKEN` | ✅ | 你的 Bot Token (找BotFather要) | `123456:ABC-xxx` |
| `GEMINI_API_KEYS` | ✅ | Gemini Key 池 (英文逗号分隔，无空格) | `AIza1...,AIza2...,AIza3...` |
| `OWNER_ID` | ✅ | 你的 Telegram ID (数字ID，最高权限) | `5016221686` |
| `GROUP_LINK` | ❌ | 群组链接 (用于拒绝陌生人私聊时展示) | `https://t.me/yourgroup` |

**设置完成后，Zeabur 会自动重启服务。看到绿色的 `Running` 即代表部署成功！**

---

## 🛠️ 其他部署方式 (Docker / VPS)

如果你有自己的服务器 (VPS) 或者想用其他容器平台 (如 Railway, Fly.io)，也可以通过 Docker 运行。

### Docker 运行命令

```bash
# 1. 拉取代码
git clone [https://github.com/你的用户名/Vivian-Bot.git](https://github.com/你的用户名/Vivian-Bot.git)
cd Vivian-Bot

# 2. 构建镜像
docker build -t vivian-bot .

# 3. 启动容器 (请替换环境变量)
docker run -d \
  --name vivian-bot \
  --restart always \
  -e TELEGRAM_BOT_TOKEN="你的Token" \
  -e GEMINI_API_KEYS="Key1,Key2,Key3" \
  -e OWNER_ID=你的数字ID \
  vivian-bot
