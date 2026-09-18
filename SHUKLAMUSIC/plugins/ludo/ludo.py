from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from SHUKLAMUSIC import app


# Active Ludo games
ludo_games = {}


def game_text(game):
    players = "\n".join(
        f"🎮 {i + 1}. {name}"
        for i, name in enumerate(game["names"])
    )

    return (
        "🎲 **LUDO ROOM**\n\n"
        f"👑 Host: {game['names'][0]}\n\n"
        f"{players}\n\n"
        f"👥 Players: {len(game['players'])}/4\n\n"
        "Waiting for players..."
    )


def game_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "👥 JOIN GAME",
                    callback_data="ludo_join"
                )
            ],
            [
                InlineKeyboardButton(
                    "🚀 START GAME",
                    callback_data="ludo_start"
                )
            ],
        ]
    )


@app.on_message(filters.command("ludo"))
async def ludo_command(client, message):

    chat_id = message.chat.id

    if chat_id in ludo_games:
        await message.reply_text(
            "⚠️ **A Ludo game is already active!**\n\n"
            "Join the existing room below.",
            reply_markup=game_buttons()
        )
        return

    user = message.from_user

    ludo_games[chat_id] = {
        "players": [user.id],
        "names": [user.first_name],
        "host": user.id,
    }

    await message.reply_text(
        game_text(ludo_games[chat_id]),
        reply_markup=game_buttons()
    )


@app.on_callback_query(filters.regex("^ludo_join$"))
async def ludo_join(client, query):

    chat_id = query.message.chat.id
    user = query.from_user

    if chat_id not in ludo_games:
        await query.answer(
            "❌ No active Ludo game!",
            show_alert=True
        )
        return

    game = ludo_games[chat_id]

    # Already joined
    if user.id in game["players"]:
        await query.answer(
            "⚠️ You are already in this game!",
            show_alert=True
        )
        return

    # Game full
    if len(game["players"]) >= 4:
        await query.answer(
            "❌ Game is full!",
            show_alert=True
        )
        return

    # Add player
    game["players"].append(user.id)
    game["names"].append(user.first_name)

    await query.message.edit_text(
        game_text(game),
        reply_markup=game_buttons()
    )

    await query.answer(
        "✅ You joined the Ludo game!"
    )


@app.on_callback_query(filters.regex("^ludo_start$"))
async def ludo_start(client, query):

    chat_id = query.message.chat.id
    user = query.from_user

    if chat_id not in ludo_games:
        await query.answer(
            "❌ No active game!",
            show_alert=True
        )
        return

    game = ludo_games[chat_id]

    # Only host can start
    if user.id != game["host"]:
        await query.answer(
            "👑 Only the host can start the game!",
            show_alert=True
        )
        return

    # Minimum 2 players
    if len(game["players"]) < 2:
        await query.answer(
            "👥 At least 2 players are required!",
            show_alert=True
        )
        return

    await query.message.edit_text(
        "🎲 **LUDO GAME STARTED!**\n\n"
        + "\n".join(
            f"🎮 {i + 1}. {name}"
            for i, name in enumerate(game["names"])
        )
        + "\n\n"
        "🔥 Players connected successfully!\n\n"
        "🎯 **Next:** Ludo Board + Dice"
    )

    await query.answer("🎲 Game started!")
