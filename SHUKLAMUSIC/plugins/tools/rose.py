import httpx

from pyrogram import filters
from pyrogram.types import Message

from SHUKLAMUSIC import app
import config

OWNER_NAME = "SASUKE"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = 8672927645
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡"

# Put a DIRECT .mp4 URL here.
VIDEO_URL = "https://files.catbox.moe/k7tma6.mp4"

# Custom Premium Emoji IDs
MASTER_EMOJI = "5965325316304933700"
SASUKE_EMOJI = "6152463694296000291"
MINDSET_EMOJI = "5427348098038898331"
HELP_EMOJI = "5976754224279589530"

CONTACT_EMOJI = "6138798143447244059"
CHANNEL_EMOJI = "5879704262790878162"
SUPPORT_EMOJI = "5208748315805499400"

ROSE_TEXT = f"""
<b>𝛢 𝙱 𝙾 ᴜ 𝚃   ϻᴀs𝛕є꧊ꝛ</b>
<tg-emoji emoji-id="{MASTER_EMOJI}">✨</tg-emoji>

<b>𝐍ᴀᴍᴇ</b>  <tg-emoji emoji-id="{SASUKE_EMOJI}">👑</tg-emoji>
<a href="tg://user?id={OWNER_ID}">{OWNER_NAME}</a>

<b>𝐔sᴇʀ  𝐈ᴅ:</b>
<code>{OWNER_ID}</code>

<b>𝐔sᴇʀɴᴀᴍᴇ:</b>
@{OWNER_USERNAME}

<tg-emoji emoji-id="{MINDSET_EMOJI}">🧠</tg-emoji> <b>𝐌ɪɴᴅsᴇᴛ</b>
<i>𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡</i>

━━━━━━━━━━━━━━━━━━━━

<tg-emoji emoji-id="{HELP_EMOJI}">💬</tg-emoji>
<b>Need Help or Support?</b>

Contact the owner using the buttons
below for bot setup, support &amp; queries.
"""

KEYBOARD = {
    "inline_keyboard": [
        [{
            "text": "CONTACT OWNER",
            "url": f"https://t.me/{OWNER_USERNAME}",
            "style": "primary",
            "icon_custom_emoji_id": CONTACT_EMOJI,
        }],
        [{
            "text": "MY CHANNEL",
            "url": "https://t.me/Aw_Music_channel",
            "style": "success",
            "icon_custom_emoji_id": CHANNEL_EMOJI,
        }],
        [{
            "text": "HELP & SUPPORT",
            "url": f"https://t.me/{OWNER_USERNAME}",
            "style": "danger",
            "icon_custom_emoji_id": SUPPORT_EMOJI,
        }],
    ]
}

@app.on_message(filters.command(["rose"], prefixes=["/", "!", "."]))
async def rose_command(client, message: Message):
    bot_token = getattr(config, "BOT_TOKEN", None)

    if not bot_token:
        return await message.reply_text("❌ BOT_TOKEN is missing in config.py")

    if not VIDEO_URL or VIDEO_URL == "PASTE_DIRECT_MP4_URL_HERE":
        return await message.reply_text(
            "⚠️ <b>VIDEO_URL is not set.</b>\n\n"
            "Open <code>rose.py</code> and put your direct "
            "<code>.mp4</code> video URL in VIDEO_URL.",
            parse_mode="HTML",
        )

    api_url = f"https://api.telegram.org/bot{bot_token}/sendVideo"

    payload = {
        "chat_id": message.chat.id,
        "video": VIDEO_URL,
        "caption": ROSE_TEXT,
        "parse_mode": "HTML",
        "supports_streaming": True,
        "reply_markup": KEYBOARD,
        "reply_parameters": {"message_id": message.id},
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as http:
            response = await http.post(api_url, json=payload)

        result = response.json()
        if not result.get("ok"):
            error = result.get("description", "Unknown Telegram API error")
            await message.reply_text(
                "❌ <b>Rose Command Error</b>\n\n"
                f"<code>{error[:1000]}</code>",
                parse_mode="HTML",
            )
    except Exception as e:
        print(f"[ROSE ERROR] {e}")
        try:
            await message.reply_text(
                "❌ <b>Rose Command Error</b>\n\n"
                f"<code>{str(e)[:1000]}</code>",
                parse_mode="HTML",
            )
        except Exception:
            pass
