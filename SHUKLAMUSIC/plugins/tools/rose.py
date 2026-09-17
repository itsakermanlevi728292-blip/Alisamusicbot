from pyrogram import filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity
from SHUKLAMUSIC import app

# Owner Configuration
OWNER_NAME = "ටිαѕυкє"
OWNER_USERNAME = "sasuke_qt"
OWNER_ID = 8672927645
OWNER_BIO = "𝐅ʀᴏᴍ 𝐒ᴜғғᴇʀɪɴɢ 𝐂ᴏᴍᴇs 𝐆ʟᴏʀʏ ⚡"

# Telegram Premium Animated Emoji ID (Change if you have another ID)
PREMIUM_EMOJI_ID = 5431520286083341812  # Integer format

@app.on_message(filters.command(["rose", "Rose"], prefixes=["/", "!", "."]))
async def rose_owner_info(client, message: Message):
    # Base Text Formatting
    text = (
        "🌹 OWNER DETAILS & PROFILE 🌹\n\n"
        f"👤 Name: {OWNER_NAME}\n"
        f"🆔 User ID: {OWNER_ID}\n"
        f"💬 Username: @{OWNER_USERNAME}\n"
        f"📝 Bio: {OWNER_BIO}\n\n"
        "✨ For any queries, bot setup, or support, click the buttons below!"
    )

    # Offsets for links and bolding
    name_start = text.find(OWNER_NAME)
    name_length = len(OWNER_NAME)
    
    id_start = text.find(str(OWNER_ID))
    id_length = len(str(OWNER_ID))

    # Constructing Entities manually so Bot can render Custom Premium Emojis
    entities = [
        # Bold Header
        MessageEntity(type=enums.MessageEntityType.BOLD, offset=0, length=30),
        
        # Premium Custom Emoji on the First Rose
        MessageEntity(
            type=enums.MessageEntityType.CUSTOM_EMOJI,
            offset=0,
            length=2,
            custom_emoji_id=str(PREMIUM_EMOJI_ID)
        ),
        
        # Profile Link on Name (Tap on Name opens profile)
        MessageEntity(
            type=enums.MessageEntityType.TEXT_MENTION,
            offset=name_start,
            length=name_length,
            user=await client.get_users(OWNER_ID)
        ),
        
        # Code block on User ID
        MessageEntity(
            type=enums.MessageEntityType.CODE,
            offset=id_start,
            length=id_length
        ),
        
        # Italic on footer
        MessageEntity(
            type=enums.MessageEntityType.ITALIC,
            offset=text.find("✨"),
            length=len("✨ For any queries, bot setup, or support, click the buttons below!")
        )
    ]

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🌹 Contact Owner", url=f"https://t.me/{OWNER_USERNAME}"),
            ],
            [
                InlineKeyboardButton("✨ Share Info", switch_inline_query="owner"),
            ]
        ]
    )

    # Message sent directly from Bot (app)
    await message.reply_text(
        text=text,
        entities=entities,
        reply_markup=buttons,
        disable_web_page_preview=True
    )
    
