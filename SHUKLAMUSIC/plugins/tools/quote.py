from io import BytesIO

from pyrogram import filters
from pyrogram.types import Message
from httpx import AsyncClient, Timeout

from SHUKLAMUSIC import app
import config


# ============================================================
# QUOTE API
# ============================================================

QUOTE_API = "https://quote.yuri.ly/quote/generate.png"

http = AsyncClient(
    timeout=Timeout(30.0),
    follow_redirects=True,
)


# ============================================================
# HELPERS
# ============================================================

def get_name(user):
    if not user:
        return "Unknown"

    name = user.first_name or "Unknown"

    if user.last_name:
        name += f" {user.last_name}"

    return name


def get_username(user):
    if user and user.username:
        return user.username

    return ""


def get_text(message):
    if message.text:
        return message.text

    if message.caption:
        return message.caption

    return ""


async def make_quote(message: Message):
    user = message.from_user

    if user:
        user_id = user.id
        name = get_name(user)
        username = get_username(user)

        photo = ""

        try:
            if user.photo:
                photo = {
                    "small_file_id": user.photo.small_file_id,
                    "small_photo_unique_id": user.photo.small_photo_unique_id,
                    "big_file_id": user.photo.big_file_id,
                    "big_photo_unique_id": user.photo.big_photo_unique_id,
                }
        except Exception:
            photo = ""

    elif message.sender_chat:
        user_id = message.sender_chat.id
        name = message.sender_chat.title or "Unknown"
        username = message.sender_chat.username or ""
        photo = ""

        try:
            if message.sender_chat.photo:
                photo = {
                    "small_file_id": message.sender_chat.photo.small_file_id,
                    "small_photo_unique_id": message.sender_chat.photo.small_photo_unique_id,
                    "big_file_id": message.sender_chat.photo.big_file_id,
                    "big_photo_unique_id": message.sender_chat.photo.big_photo_unique_id,
                }
        except Exception:
            photo = ""

    else:
        user_id = 1
        name = "Unknown"
        username = ""
        photo = ""

    payload = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#1b1429",
        "scale": 2,
        "messages": [
            {
                "entities": [],
                "chatId": user_id,
                "avatar": True,
                "from": {
                    "id": user_id,
                    "name": name,
                    "username": username,
                    "type": "private",
                    "photo": photo,
                },
                "text": get_text(message),
                "replyMessage": {},
            }
        ],
    }

    # Send bot token so API can resolve Telegram file IDs.
    if getattr(config, "BOT_TOKEN", None):
        payload["botToken"] = config.BOT_TOKEN

    response = await http.post(
        QUOTE_API,
        json=payload,
        headers={"Content-Type": "application/json"},
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Quote API HTTP {response.status_code}: {response.text[:300]}"
        )

    content_type = response.headers.get("content-type", "")

    # Direct .webp endpoint returns image bytes.
    if "image" in content_type:
        return response.content

    # Fallback if API returns JSON.
    data = response.json()

    if data.get("error"):
        raise RuntimeError(str(data["error"]))

    image = data.get("image")

    if not image:
        result = data.get("result", {})
        image = result.get("image")

    if not image:
        raise RuntimeError(f"Invalid API response: {data}")

    import base64

    return base64.b64decode(image)


# ============================================================
# /q COMMAND
# ============================================================

@app.on_message(
    filters.command("q") & filters.reply
)
async def quote_command(client, message: Message):

    try:
        replied = message.reply_to_message

        if not replied:
            return await message.reply_text(
                "❌ Reply to a message and use /q"
            )

        # Only text/caption messages for now.
        if not get_text(replied):
            return await message.reply_text(
                "❌ /q currently works with text/caption messages."
            )

        quote = await make_quote(replied)

        sticker = BytesIO(quote)
        sticker.name = "quote.webp"

        await message.reply_sticker(
            sticker,
            reply_to_message_id=replied.id,
        )

    except Exception as e:
        print(f"[QUOTE ERROR] {type(e).__name__}: {e}")

        await message.reply_text(
            f"❌ Quote failed.\n\n"
            f"`{type(e).__name__}: {str(e)[:300]}`"
        )


# ============================================================
# /r COMMAND
# ============================================================

@app.on_message(
    filters.command("r") & filters.reply
)
async def reply_quote_command(client, message: Message):

    try:
        replied = message.reply_to_message

        if not replied:
            return await message.reply_text(
                "❌ Reply to a message and use /r"
            )

        if not get_text(replied):
            return await message.reply_text(
                "❌ /r currently works with text/caption messages."
            )

        quote = await make_quote(replied)

        sticker = BytesIO(quote)
        sticker.name = "quote.webp"

        await message.reply_sticker(
            sticker,
            reply_to_message_id=replied.id,
        )

    except Exception as e:
        print(f"[QUOTE ERROR] {type(e).__name__}: {e}")

        await message.reply_text(
            f"❌ Quote failed.\n\n"
            f"`{type(e).__name__}: {str(e)[:300]}`"
    )
