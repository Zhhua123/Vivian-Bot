import edge_tts
import io
import asyncio
from pydub import AudioSegment

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"

async def text_to_speech_stream(text: str, mode="normal") -> io.BytesIO:
    voice = DEFAULT_VOICE
    rate = "+0%"
    pitch = "+0Hz"
    
    if mode == "sing":
        rate = "+20%" 
        pitch = "+5Hz"
    
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    mp3_buffer = io.BytesIO()
    
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            mp3_buffer.write(chunk["data"])
    
    mp3_buffer.seek(0)
    
    try:
        audio = AudioSegment.from_file(mp3_buffer, format="mp3")
        ogg_buffer = io.BytesIO()
        audio.export(ogg_buffer, format="ogg", codec="libopus", parameters=["-b:a", "24k"])
        ogg_buffer.seek(0)
        return ogg_buffer
    except Exception as e:
        print(f"转码失败: {e}")
        mp3_buffer.seek(0)
        return mp3_buffer