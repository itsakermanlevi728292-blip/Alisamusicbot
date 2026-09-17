from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message
from httpx import AsyncClient, Timeout

from SHUKLAMUSIC import app


# 100% Active Working Quotly Endpoints
ENDPOINTS = [
    "https://q.m3u.workers.dev/generate",
    "https://quote-api.up.railway.app/generate",
    "https://bot.lynn.workers.dev/generate"
]

http = AsyncClient(
    timeout=Timeout(25.0),
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

    # Multiple servers loop - ek fail hoga toh dusra try karega
    for endpoint in ENDPOINTS:
        try:
            response = await http.post(
                endpoint,
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
            continue

    await message.reply_text("❌ All Quote Servers are down right now. Please try again after some time.")
