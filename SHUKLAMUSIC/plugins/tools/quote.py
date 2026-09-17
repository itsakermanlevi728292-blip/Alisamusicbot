import asyncio
from io import BytesIO
from pyrogram import filters
from pyrogram.types import Message
from httpx import AsyncClient, Timeout

from SHUKLAMUSIC import app

# Telegram Quotly Webhook Direct Endpoint
API_URL = "https://bot.lynn.workers.dev/generate"

http = AsyncClient(
    timeout=Timeout(20.0),
    follow_redirects=True,
    verify=False
)

def get_text(msg: Message):
    return (msg.text or msg.caption or "").strip()

def get_name(msg: Message):
    if msg.from_user:
        return msg.from_user.first_name or msg.from_user.username or "User"
    if msg.sender_chat:
        return msg.sender_chat.title or "Group"
    return "User"

@app.on_message(filters.command(["q", "quote", "r"]) & filters.reply)
async def quote_command(client, message: Message):
    replied = message.reply_to_message

    if not replied:
        return await message.reply_text("❌ Reply to a message first.")

    text = get_text(replied)

    if not text:
        return await message.reply_text("❌ I can only quote text messages.")

    st_msg = await message.reply_text("🔄 **Generating Quote...**")

    user_id = replied.from_user.id if replied.from_user else 0
    name = get_name(replied)

    payload = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [
            {
                "entities": [],
                "avatar": True,
                "from": {
                    "id": user_id,
                    "name": name,
                },
                "text": text,
            }
        ],
    }

    try:
        res = await http.post(API_URL, json=payload)
        if res.status_code == 200 and len(res.content) > 100:
            sticker = BytesIO(res.content)
            sticker.name = "quote.webp"
            await st_msg.delete()
            return await message.reply_sticker(
                sticker,
                reply_to_message_id=replied.id
            )
    except Exception as e:
        pass

    # Backup Telegram Bot Forward Method
    try:
        await st_msg.edit_text("⏳ *Connecting Telegram Quotly Engine...*")
        
        # Forward message to @QuotLyBot
        fwd = await replied.forward("@QuotLyBot")
        await asyncio.sleep(2)
        
        async for msg in client.get_chat_history("@QuotLyBot", limit=1):
            if msg.sticker:
                await st_msg.delete()
                return await message.reply_sticker(
                    msg.sticker.file_id,
                    reply_to_message_id=replied.id
                )
    except Exception as e:
        pass

    await st_msg.edit_text("❌ Failed to generate quote. Make sure bot is working properly.")
    
