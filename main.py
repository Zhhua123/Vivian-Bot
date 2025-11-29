import logging
import asyncio
import io
import os
import sys
import datetime
from collections import deque, defaultdict
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from ai_agent import GeminiAgent
from tts_engine import text_to_speech_stream

# ======================================================================
# 🟢【小白请看这里】配置读取区
# 这里的代码会自动去读取你在 Zeabur "Variables" 里填的内容。
# ⚠️ 警告：千万不要直接在这里把 'TOKEN' 改成你的密码！那样不安全！
# ======================================================================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OWNER_ID = int(os.getenv("OWNER_ID", "0"))
GROUP_LINK = os.getenv("GROUP_LINK", "群聊")

# 检查一下你有没有在 Zeabur 里填 Token，没填就报错提醒你
if not TOKEN:
    print("❌ 【启动失败】你忘记设置环境变量了！")
    print("👉 请去 Zeabur -> Variables -> 添加 TELEGRAM_BOT_TOKEN")
    sys.exit(1)

# 配置日志（让你在后台能看到它在干嘛）
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
ai_bot = None

# 全局数据（存聊天记录和违规次数的地方）
VIOLATIONS = defaultdict(int)
GROUP_HISTORY = defaultdict(lambda: deque(maxlen=50))
CHAT_MODES = defaultdict(bool) 

# --- 👇 下面是功能逻辑区，小白不需要改动 👇 ---

# 1. 检查是不是主人或者管理员
async def check_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    if user_id == OWNER_ID: return True # 主人最大
    if update.message.chat.type == 'private': return True

    try:
        admins = await context.bot.get_chat_administrators(chat_id)
        if user_id in [admin.user.id for admin in admins]: return True
    except:
        pass
    
    await update.message.reply_text("💢 杂鱼，你没有权限命令本小姐！")
    return False

# 2. 拦截陌生人私聊
async def check_private_access(update: Update) -> bool:
    if update.message.chat.type != 'private': return True
    if update.effective_user.id == OWNER_ID: return True
    await update.message.reply_text(f"🚫 **访问拒绝**\n我是私人助理，只服务主人。\n请去 {GROUP_LINK} 找我。", parse_mode='Markdown')
    return False

# 3. 判断要不要回消息
def should_reply_check(update, context):
    user_input = update.message.text or ""
    chat_type = update.message.chat.type
    chat_id = update.effective_chat.id
    
    if chat_type == 'private': return True # 私聊必回
    
    is_talkative = CHAT_MODES[chat_id] # 看是不是话痨模式
    is_reply_bot = (update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id)
    is_called = ("薇薇安" in user_input or "gemini" in user_input.lower())
    
    if is_talkative: return True
    return is_called or is_reply_bot

# --- 🎮 指令区 (这里定义了 /ms /act 这些命令) ---

async def ms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """切换高冷/话痨模式"""
    if not await check_admin(update, context): return
    chat_id = update.effective_chat.id
    CHAT_MODES[chat_id] = not CHAT_MODES[chat_id]
    state = "🗣️ 话痨模式 (开启)" if CHAT_MODES[chat_id] else "❄️ 高冷模式 (默认)"
    await update.message.reply_text(f"📢 **模式切换**：{state}")

async def act_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """变身指令"""
    if not ai_bot: return
    if not context.args:
        await update.message.reply_text("🎭 请输入人设，例如：`/act 猫娘`", parse_mode='Markdown')
        return
    persona = " ".join(context.args)
    ai_bot.set_persona(update.effective_user.id, persona)
    await update.message.reply_text(f"🎭 变身成功！现在我是：**{persona}**", parse_mode='Markdown')

async def cw_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """重置记忆"""
    if not ai_bot: return
    ai_bot.set_persona(update.effective_user.id, "reset")
    await update.message.reply_text("🧹 记忆已清理，焕然一新！")

# --- 🛡️ 管理员指令 (踢人/禁言) ---

async def ti_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_admin(update, context): return
    if not update.message.reply_to_message:
        await update.message.reply_text("🙄 请回复你要踢的那个人！")
        return
    target = update.message.reply_to_message.from_user
    if target.id == OWNER_ID:
        await update.message.reply_text("💢 大胆！竟敢踢主人？")
        return
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target.id)
        await update.message.reply_text(f"👋 走好不送！**{target.first_name}** 已被踢出。", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ 踢人失败：{e}")

async def jy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_admin(update, context): return
    if not update.message.reply_to_message: return
    minutes = 5
    if context.args:
        try: minutes = int(context.args[0])
        except: pass
    target = update.message.reply_to_message.from_user
    if target.id == OWNER_ID: return
    try:
        perm = ChatPermissions(can_send_messages=False)
        until = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, perm, until_date=until)
        await update.message.reply_text(f"🤐 **{target.first_name}** 禁言 {minutes} 分钟。", parse_mode='Markdown')
    except: pass

async def jj_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_admin(update, context): return
    if not update.message.reply_to_message: return
    try:
        target = update.message.reply_to_message.from_user
        perm = ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_other_messages=True)
        await context.bot.restrict_chat_member(update.effective_chat.id, target.id, perm)
        await update.message.reply_text("😤 已解禁。")
    except: pass

async def zd_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_admin(update, context): return
    if not update.message.reply_to_message: return
    try:
        await context.bot.pin_chat_message(update.effective_chat.id, update.message.reply_to_message.message_id)
        await update.message.reply_text("📌 消息已置顶！")
    except: pass

# --- 🔧 功能指令 (总结/翻译/唱歌/审判) ---

async def zj_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_private_access(update): return
    chat_id = update.effective_chat.id
    history = GROUP_HISTORY.get(chat_id, [])
    if len(history) < 3: 
        await update.message.reply_text("没啥好总结的。")
        return
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    summary = await ai_bot.summarize("\n".join(history))
    await update.message.reply_text(f"📝 **省流日报**：\n\n{summary}", parse_mode='Markdown')

async def fy_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_private_access(update): return
    if not update.message.reply_to_message: return
    text = update.message.reply_to_message.text
    if not text: return
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    result = await ai_bot.translate_text(text)
    await update.message.reply_text(result)

async def cha_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = update.message.reply_to_message.from_user if update.message.reply_to_message else update.effective_user
    msg = f"🔍 **档案**: {target.first_name}\n🆔 ID: `{target.id}`\n⚠️ 违规: {VIOLATIONS[target.id]}"
    await update.message.reply_text(msg, parse_mode='Markdown')

async def sing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("你想听什么歌？例：`/sing 恭喜发财`", parse_mode='Markdown')
        return
    topic = " ".join(context.args)
    await context.bot.send_chat_action(update.effective_chat.id, "record_voice")
    lyrics = await ai_bot.generate_song(update.effective_user.id, topic)
    await update.message.reply_text(f"🎵 **正在演唱**：\n\n{lyrics}", parse_mode='Markdown')
    voice_bio = await text_to_speech_stream(lyrics, mode="sing")
    await update.message.reply_voice(voice_bio, caption="🎤 Vivian Live")

async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("请回复你要审判的人！")
        return
    target_msg = update.message.reply_to_message.text or "这个人的存在就是个槽点"
    await context.bot.send_chat_action(update.effective_chat.id, "typing")
    roast = await ai_bot.generate_roast(update.effective_user.id, target_msg)
    await update.message.reply_text(roast)

# --- 💬 消息处理中心 ---

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_private_access(update): return
    
    user_input = update.message.text
    user_name = update.effective_user.first_name
    chat_id = update.effective_chat.id
    
    # 记录群聊历史
    if update.message.chat.type != 'private':
        GROUP_HISTORY[chat_id].append(f"{user_name}: {user_input}")

    if not should_reply_check(update, context): return

    # 快捷指令拦截
    if user_input.startswith('/act '):
        if ai_bot: ai_bot.set_persona(update.effective_user.id, user_input.replace('/act ', ''))
        await update.message.reply_text("🎭 变身！")
        return
    if user_input == '/cw':
        if ai_bot: ai_bot.set_persona(update.effective_user.id, "reset")
        await update.message.reply_text("🧹 记忆重置")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    if ai_bot:
        response = await ai_bot.send_text(update.effective_user.id, user_input)
        await update.message.reply_text(response)
        
        # 语音朗读 (检测关键词)
        if any(k in user_input for k in ["语音", "读", "念", "说"]):
            await context.bot.send_chat_action(chat_id=chat_id, action="record_voice")
            voice_bio = await text_to_speech_stream(response)
            await update.message.reply_voice(voice=voice_bio)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_private_access(update): return
    if not should_reply_check(update, context): return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="record_voice")
    f = await update.message.voice.get_file()
    b = io.BytesIO()
    await f.download_to_memory(b)
    resp = await ai_bot.send_multimodal_audio(update.effective_user.id, b.getvalue())
    voice = await text_to_speech_stream(resp)
    await update.message.reply_voice(voice=voice, caption=resp[:50]+"...")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_private_access(update): return
    if not should_reply_check(update, context): return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        p = await update.message.photo[-1].get_file()
        b = io.BytesIO()
        await p.download_to_memory(b)
        caption = update.message.caption
        r = await ai_bot.send_image(update.effective_user.id, b.getvalue(), caption)
        await update.message.reply_text(r)
    except Exception as e:
        await update.message.reply_text(f"💢 图片读取失败：{e}")

async def handle_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_private_access(update): return
    if not should_reply_check(update, context): return

    try:
        sticker = update.message.sticker
        if not sticker.thumbnail: return 
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        f = await sticker.thumbnail.get_file()
        b = io.BytesIO()
        await f.download_to_memory(b)
        prompt = "用户发了一个表情包。请评价这个表情包的含义和情绪，并用毒舌语气吐槽。"
        r = await ai_bot.send_image(update.effective_user.id, b.getvalue(), prompt)
        await update.message.reply_text(r)
    except Exception as e:
        print(f"表情包错误: {e}")

async def post_init(app):
    """防止 webhook 冲突，自动清理"""
    await app.bot.delete_webhook(drop_pending_updates=True)

if __name__ == '__main__':
    # 尝试连接 AI
    try:
        ai_bot = GeminiAgent()
        print(f"✅ 薇薇安 (开源版) 启动成功")
    except Exception as e:
        print(f"❌ AI 初始化失败: {e}")
        print("💡 提示：请检查 Zeabur 里的 GEMINI_API_KEYS 变量是否填对。")

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    # 注册所有指令
    app.add_handler(CommandHandler('start', lambda u,c: u.message.reply_text("薇薇安驾到！")))
    
    app.add_handler(CommandHandler('ms', ms_command))
    app.add_handler(CommandHandler('act', act_command))
    app.add_handler(CommandHandler('cw', cw_command))
    
    app.add_handler(CommandHandler('ti', ti_command))
    app.add_handler(CommandHandler('jy', jy_command))
    app.add_handler(CommandHandler('jj', jj_command))
    app.add_handler(CommandHandler('zd', zd_command))
    
    app.add_handler(CommandHandler('zj', zj_command))
    app.add_handler(CommandHandler('fy', fy_command))
    app.add_handler(CommandHandler('cha', cha_command))
    app.add_handler(CommandHandler('sing', sing_command))
    app.add_handler(CommandHandler('roast', roast_command))
    
    # 注册消息处理
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, lambda u,c: u.message.reply_text("哟，新人？报上三围！")))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Sticker.ALL, handle_sticker))
    
    print("🚀 Bot Running...")
    app.run_polling()
