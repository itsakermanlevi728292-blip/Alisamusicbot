from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message
from httpx import AsyncClient, Timeout

from SHUKLAMUSIC import app


QUOTE_API = "https://bot.lynn.workers.dev/generate"

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


async def get_user_avatar(client, msg: Message):
    try:
        user_id = get_user_id(msg)
        if not user_id:
            return None
            
        photos = [p async for p in client.get_chat_photos(user_id, limit=1)]
        if photos:
            file_id = photos[0].file_id
            file_info = await client.get_file(file_id)
            if hasattr(file_info, "file_path") and file_info.file_path:
                return f"https://api.telegram.org/file/bot{client.token}/{file_info.file_path}"
    except Exception:
        pass
    return None


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
    avatar_url = await get_user_avatar(client, replied)

    msg_obj = {
        "entities": [],
        "avatar": True,
        "from": {
            "id": user_id,
            "name": name,
        },
        "text": text,
    }

    if avatar_url:
        msg_obj["from"]["photo"] = {"url": avatar_url}

    payload = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [msg_obj],
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
                f"{response.text[:200]}"
            )

        res_json = response.json()
        
        if not res_json.get("ok"):
            return await message.reply_text(
                "❌ Failed to generate quote sticker."
            )

        # Base64 sticker decoding or fetching result
        result = res_json.get("result", {})
        image_url = result.get("image") or result.get("url")

        if image_url:
            img_res = await http.get(image_url)
            data = img_res.content
        else:
            # Fallback direct bytes
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
        
