# ==========================================
# users.py
# FF ID Management Bot Users System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message

import database as db
import keyboards


# ==========================================
# START
# ==========================================

@Client.on_message(filters.command("start"))
async def start_cmd(client, message: Message):

    user = message.from_user

    db.add_user(
        user.id,
        user.first_name
    )

    await message.reply_text(
        "🎮 Welcome To FF ID Management Bot",
        reply_markup=keyboards.home_menu()
    )


# ==========================================
# TOTAL IDS
# ==========================================

@Client.on_message(filters.command("totalids"))
async def total_ids(client, message):

    total = db.total_ff_ids()

    await message.reply_text(
        f"📊 Total Saved IDs: {total}"
    )


# ==========================================
# TOTAL USERS
# ==========================================

@Client.on_message(filters.command("totalusers"))
async def total_users(client, message):

    total = db.total_users()

    await message.reply_text(
        f"👥 Total Users: {total}"
    )


# ==========================================
# SEARCH UID
# ==========================================

@Client.on_message(filters.command("search"))
async def search_uid(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/search UID"
        )

    uid = message.command[1]

    data = db.get_ff_by_uid(uid)

    if not data:
        return await message.reply_text(
            "❌ UID Not Found"
        )

    db.increase_view(uid)

    text = f"""
🎮 FF ID Details

🆔 UID: {data[2]}
👤 Nickname: {data[3]}
🏆 Category: {data[4]}
👁 Views: {data[6]}
⭐ Favorite: {data[7]}
📅 Saved: {data[8]}
"""

    await message.reply_text(
        text
    )


# ==========================================
# SEARCH NAME
# ==========================================

@Client.on_message(filters.command("searchname"))
async def search_name(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/searchname NAME"
        )

    name = " ".join(
        message.command[1:]
    )

    results = db.search_nickname(name)

    if not results:
        return await message.reply_text(
            "❌ No Result Found"
        )

    text = "🔍 Results\n\n"

    for row in results:

        text += (
            f"🆔 {row[2]}\n"
            f"👤 {row[3]}\n"
            f"🏆 {row[4]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# SHOW IDS
# ==========================================

@Client.on_message(filters.command("showids"))
async def show_ids(client, message):

    data = db.get_all_ff_ids()

    if not data:
        return await message.reply_text(
            "❌ No IDs Saved"
        )

    text = "📋 Saved FF IDs\n\n"

    for row in data:

        text += (
            f"🆔 {row[2]}\n"
            f"👤 {row[3]}\n"
            f"🏆 {row[4]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# MOST VIEWED
# ==========================================

@Client.on_message(filters.command("top"))
async def top_viewed(client, message):

    data = db.most_viewed()

    if not data:
        return await message.reply_text(
            "❌ No Data"
        )

    await message.reply_text(
        f"🏆 Most Viewed UID\n\n"
        f"🆔 {data[0]}\n"
        f"👁 Views: {data[1]}"
)
