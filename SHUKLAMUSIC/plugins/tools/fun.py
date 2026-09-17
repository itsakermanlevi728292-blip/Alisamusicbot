import random

from pyrogram import filters
from pyrogram.types import Message

from SHUKLAMUSIC import app


def get_name(user):
    if not user:
        return "Unknown"

    name = user.first_name or "User"

    if user.last_name:
        name += f" {user.last_name}"

    return name


def make_bar(score):
    filled = round(score / 10)
    return "█" * filled + "░" * (10 - filled)


def get_level(score):
    if score >= 90:
        return "LEGENDARY 🔥"
    elif score >= 75:
        return "HIGH ⚡"
    elif score >= 50:
        return "MEDIUM ✨"
    elif score >= 25:
        return "LOW 😶"
    else:
        return "CRITICAL 💀"


def get_target(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user

    return message.from_user


async def send_rate(message, title, emoji, label):
    score = random.randint(1, 100)

    await message.reply_text(
        f"{emoji} <b>{title}</b>\n\n"
        f"👤 <b>{get_name(message.from_user)}</b>\n\n"
        f"{emoji} {label}: <b>{score}/100</b>\n"
        f"<code>{make_bar(score)}</code>\n\n"
        f"✨ Level: <b>{get_level(score)}</b>"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# AURA
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("aura", prefixes=["/", "!", "."]))
async def aura_command(client, message: Message):
    await send_rate(
        message,
        "AURA CHECK",
        "⚡",
        "Aura"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# RIZZ
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("rizz", prefixes=["/", "!", "."]))
async def rizz_command(client, message: Message):
    await send_rate(
        message,
        "RIZZ CHECK",
        "🔥",
        "Rizz"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# LUCK
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("luck", prefixes=["/", "!", "."]))
async def luck_command(client, message: Message):
    await send_rate(
        message,
        "LUCK CHECK",
        "🍀",
        "Luck"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# EVIL
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("evil", prefixes=["/", "!", "."]))
async def evil_command(client, message: Message):
    await send_rate(
        message,
        "EVIL CHECK",
        "😈",
        "Evil"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# IQ
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("iq", prefixes=["/", "!", "."]))
async def iq_command(client, message: Message):
    await send_rate(
        message,
        "IQ CHECK",
        "🧠",
        "IQ"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# CHAOS
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("chaos", prefixes=["/", "!", "."]))
async def chaos_command(client, message: Message):
    await send_rate(
        message,
        "CHAOS CHECK",
        "💀",
        "Chaos"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# DRIP
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("drip", prefixes=["/", "!", "."]))
async def drip_command(client, message: Message):
    await send_rate(
        message,
        "DRIP CHECK",
        "🕶️",
        "Drip"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# LOVE
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("love", prefixes=["/", "!", "."]))
async def love_command(client, message: Message):
    user = get_target(message)
    score = random.randint(1, 100)

    await message.reply_text(
        f"💗 <b>LOVE RATE</b>\n\n"
        f"👤 <b>{get_name(user)}</b>\n\n"
        f"❤️ Love: <b>{score}%</b>\n"
        f"<code>{make_bar(score)}</code>\n\n"
        f"💫 Compatibility: <b>{get_level(score)}</b>"
    )


# ━━━━━━━━━━━━━━━━━━━━━
# FULL USER SCAN
# ━━━━━━━━━━━━━━━━━━━━━

@app.on_message(filters.command("scan", prefixes=["/", "!", "."]))
async def scan_command(client, message: Message):
    user = get_target(message)

    aura = random.randint(1, 100)
    iq = random.randint(1, 100)
    evil = random.randint(1, 100)
    luck = random.randint(1, 100)
    rizz = random.randint(1, 100)
    chaos = random.randint(1, 100)

    overall = round(
        (aura + iq + evil + luck + rizz + chaos) / 6
    )

    await message.reply_text(
        f"╭━━━「 🔎 <b>USER SCAN</b> 」━━━╮\n\n"
        f"👤 <b>{get_name(user)}</b>\n\n"
        f"⚡ Aura       <b>{aura}/100</b>\n"
        f"🧠 IQ         <b>{iq}/100</b>\n"
        f"😈 Evil       <b>{evil}/100</b>\n"
        f"🍀 Luck       <b>{luck}/100</b>\n"
        f"🔥 Rizz       <b>{rizz}/100</b>\n"
        f"💀 Chaos      <b>{chaos}/100</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Overall    <b>{overall}/100</b>\n"
        f"<code>{make_bar(overall)}</code>\n\n"
        f"⚠️ Status: <b>{get_level(overall)}</b>\n"
        f"╰━━━━━━━━━━━━━━━━━━━━╯"
    )
