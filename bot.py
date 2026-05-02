import os
from telethon import TelegramClient, events
import yt_dlp

# Koyeb-এর Settings থেকে এই ভ্যালুগুলো আসবে
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("8207287817:AAEEOHQLeg9_9QHdpHEgYHWwmS7SXjH6R8I")

bot = TelegramClient('Sakib_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply("👋 আসসালামু আলাইকুম ফারহান!\nআমি Koyeb সার্ভার থেকে সচল আছি। ভিডিওর লিঙ্ক দিন।")

@bot.on(events.NewMessage)
async def download_video(event):
    url = event.message.text
    if "http" in url:
        msg = await event.reply("⏳ প্রসেসিং শুরু হয়েছে...")
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'video.mp4',
            'quiet': True,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                await msg.edit("✅ ডাউনলোড শেষ! এখন টেলিগ্রামে পাঠাচ্ছি...")
                await bot.send_file(event.chat_id, 'video.mp4', caption=info.get('title', 'Video'))
            if os.path.exists('video.mp4'): os.remove('video.mp4')
            await msg.delete()
        except Exception as e:
            await event.reply(f"❌ এরর: {str(e)[:100]}")

print("বট সচল হয়েছে...")
bot.run_until_disconnected()
