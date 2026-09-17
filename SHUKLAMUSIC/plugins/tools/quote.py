from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message
from httpx import AsyncClient, Timeout

from SHUKLAMUSIC import app


# Primary and Backup API Endpoints
QUOTE_API_PRIMARY = "https://bot.lynn.workers.dev/generate"
QUOTE_API_BACKUP = "https://quotly.mishra.workers.dev/generate"

http = AsyncClient(
    timeout=Timeout(30.0),
    follow_redirects=True,
    verify=False,
)


def get_text(msg: Message):
    return (
        msg.text
        or msg.caption
        or ""
    ).strip()


def get_name(msg: Message):
    if msg.from_user:
        return (
            msg.from_user.first_name
            or msg.from_user.username
            or "Unknown"
        )

    if msg.sender_chat:
        return msg.sender_chat.title or "Unknown"

    return "Unknown"


def get_user_id(msg: Message):
    if msg.from_user:
        return msg.from_user.id

    if msg.sender_chat:
        return msg.sender_chat.id

    return 0


@app.on_message(
    filters.command(["q", "quote", "r"])
    & filters.reply
)
async def quote_command(client, message: Message):
    replied = message.reply_to_message

    if not replied:
        return await message.reply_text(
            "❌ Reply to a message first."
        )

    text = get_text(replied)

    if not text:
        return await message.reply_text(
            "❌ I can only quote text messages."
        )

    user_id = get_user_id(replied)
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

    # Primary API Request
    try:
        response = await http.post(
            QUOTE_API_PRIMARY,
            json=payload,
        )
        if response.status_code == 200 and response.content:
            sticker = BytesIO(response.content)
            sticker.name = "quote.webp"
            return await message.reply_sticker(
                sticker,
                reply_to_message_id=replied.id,
            )
    except Exception:
        pass

    # Backup API Request
    try:
        response = await http.post(
            QUOTE_API_BACKUP,
            json=payload,
        )
        if response.status_code == 200 and response.content:
            sticker = BytesIO(response.content)
            sticker.name = "quote.webp"
            return await message.reply_sticker(
                sticker,
                reply_to_message_id=replied.id,
            )
        else:
            return await message.reply_text("❌ Quote API is currently down. Try again later.")
    except Exception as e:
        return await message.reply_text(f"❌ Quote Error: `{str(e)[:200]}`")
        
