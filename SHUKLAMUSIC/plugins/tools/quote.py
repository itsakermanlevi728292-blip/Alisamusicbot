from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message
from httpx import AsyncClient, Timeout

from SHUKLAMUSIC import app


# Alternate Working Quotly API Endpoint
QUOTE_API = "https://quotly.mjh.nz/generate"

http = AsyncClient(
    timeout=Timeout(30.0),
    follow_redirects=True,
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
                "replyMessage": {},
            }
        ],
    }

    try:
        response = await http.post(
            QUOTE_API,
            json=payload,
        )

        if response.status_code != 200:
            return await message.reply_text(
                f"❌ Quote API Error\n\n"
                f"Status: {response.status_code}\n"
                f"API Server Down or Busy."
            )

        data = response.content

        if not data:
            return await message.reply_text(
                "❌ Quote API returned empty image."
            )

        sticker = BytesIO(data)
        sticker.name = "quote.webp"

        await message.reply_sticker(
            sticker,
            reply_to_message_id=replied.id,
        )

    except Exception as e:
        await message.reply_text(
            "❌ Quote Error\n\n"
            f"`{str(e)[:500]}`"
        )
