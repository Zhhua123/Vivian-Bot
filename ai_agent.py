import os
import random
import logging
import datetime
from google import genai
from google.genai import types

class GeminiAgent:
    def __init__(self):
        # 🟢【小白请注意】这里不再直接写 Key，而是去读 Zeabur 里的变量
        keys_str = os.getenv("GEMINI_API_KEYS", "")
        # 兼容单 Key 写法
        if not keys_str: keys_str = os.getenv("GEMINI_API_KEY", "")
            
        # 把逗号分隔的字符串变成列表
        self.api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        
        if not self.api_keys:
            print("❌ 警告：未检测到 GEMINI_API_KEYS 变量！AI 无法工作。")
            self.valid_keys = []
        else:
            self.valid_keys = self.api_keys

        self.current_key_index = random.randint(0, len(self.valid_keys) - 1) if self.valid_keys else 0
        self.client = None
        self.model_name = "gemini-2.5-flash"
        
        # 🎭 人设
        self.persona_name = "薇薇安 (Vivian)"
        self.system_instruction = f"""
        你叫{self.persona_name}，是全能型的Telegram群组管家。
        性格：傲娇、毒舌、自信。
        职责：管理群聊，回答问题，看图说话，唱歌(写词)。
        严禁说自己是模型。
        """
        
        self.user_chats = {}
        if self.valid_keys: self._init_client()

    def _init_client(self):
        current_key = self.valid_keys[self.current_key_index]
        self.client = genai.Client(api_key=current_key)

    def _rotate_key(self):
        if not self.valid_keys: return
        self.current_key_index = (self.current_key_index + 1) % len(self.valid_keys)
        self._init_client()

    def set_persona(self, user_id, persona_desc):
        if persona_desc in ["默认", "normal", "reset"]:
            if user_id in self.user_personas: del self.user_personas[user_id]
        else:
            self.user_personas[user_id] = f"请全程扮演：{persona_desc}。"
        if user_id in self.user_chats: del self.user_chats[user_id]

    def _get_or_refresh_chat(self, user_id):
        if user_id not in self.user_chats:
            self.user_chats[user_id] = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction,
                    temperature=1.2,
                    max_output_tokens=1500,
                    # 🔥 关闭安全审查，防止看图报错
                    safety_settings=[
                        types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                        types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                        types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                        types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                    ]
                )
            )
        return self.user_chats[user_id]

    async def _execute_with_retry(self, user_id, func_type, content):
        if not self.valid_keys: return "❌ 未配置 API Key，请去 Zeabur 填写。"
        max_retries = len(self.valid_keys)
        now_time = datetime.datetime.now().strftime("%H:%M")
        
        for _ in range(max_retries):
            try:
                chat = self._get_or_refresh_chat(user_id)
                prompt_suffix = f"\n(Time: {now_time})"
                
                if func_type == 'text':
                    response = chat.send_message(content + prompt_suffix)
                elif func_type == 'sing':
                    prompt = f"请以“{content}”为主题，创作一段押韵的Rap歌词。不要前言后语，直接给词。"
                    response = chat.send_message(prompt)
                elif func_type == 'roast':
                    response = chat.send_message(f"请狠狠地吐槽、审判这个内容：{content}。")
                elif func_type == 'audio':
                    response = chat.send_message([types.Part.from_bytes(data=content[0], mime_type=content[1]), "听语音并回复"])
                elif func_type == 'image':
                    prompt = content[1] or "评价这张图，如果它是表情包，请解读含义。"
                    response = chat.send_message([types.Part.from_bytes(data=content[0], mime_type="image/jpeg"), prompt])
                
                if not response.text: return "🚫 无法评价此内容。"
                return response.text
            except Exception as e:
                error_str = str(e)
                if any(x in error_str for x in ["429", "403", "Quota", "valid"]):
                    if user_id in self.user_chats: del self.user_chats[user_id]
                    self._rotate_key()
                    continue
                return f"💢 错误: {error_str}"
        return "😴 系统过载，所有 Key 都休息了。"

    async def send_text(self, user_id, text): return await self._execute_with_retry(user_id, 'text', text)
    async def generate_song(self, user_id, topic): return await self._execute_with_retry(user_id, 'sing', topic)
    async def generate_roast(self, user_id, text): return await self._execute_with_retry(user_id, 'roast', text)
    async def send_multimodal_audio(self, user_id, data, mime): return await self._execute_with_retry(user_id, 'audio', (data, mime))
    async def send_image(self, user_id, data, caption): return await self._execute_with_retry(user_id, 'image', (data, caption))
    
    async def summarize(self, text):
        prompt = f"请总结以下群聊内容，提取重点和八卦，用幽默的风格写成日报：\n{text}"
        try:
            return self.client.chats.create(model=self.model_name).send_message(prompt).text
        except: return "无法总结"
    async def translate_text(self, text):
        try:
            return self.client.chats.create(model=self.model_name).send_message(f"翻译成中文并毒舌点评：{text}").text
        except: return "无法翻译"
