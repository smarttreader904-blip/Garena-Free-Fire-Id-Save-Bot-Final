# ==========================================
# stats.py
# FF ID Management Bot Statistics System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message

import config
import database as db


# ==========================================
# CHECK ADMIN
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# BOT STATS
# /stats
# ==========================================

@Client.on_message(filters.command("stats"))
async def bot_stats(client, message: Message):

    total_ids = db.total_ff_ids()
    total_users = db.total_users()

    pending_count = len(
        db.get_pending_requests()
    )

    most_viewed = db.most_viewed()

    text = (
        "📊 FF ID BOT STATS\n\n"
        f"🆔 Total IDs: {total_ids}\n"
        f"👥 Total Users: {total_users}\n"
        f"📥 Pending Requests: {pending_count}\n"
    )

    if most_viewed:
        text += (
            f"\n🏆 Most Viewed UID: {most_viewed[0]}\n"
            f"👁 Views: {most_viewed[1]}"
        )

    await message.reply_text(text)


# ==========================================
# ADMIN STATS
# /adminstats
# ==========================================

@Client.on_message(filters.command("adminstats"))
async def admin_stats(client, message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    total_ids = db.total_ff_ids()
    total_users = db.total_users()
    total_logs = db.total_logs()

    pending_count = len(
        db.get_pending_requests()
    )

    text = f"""
👑 ADMIN STATS

🆔 Total IDs: {total_ids}
👥 Total Users: {total_users}
📥 Pending: {pending_count}
📜 Total Logs: {total_logs}
"""

    await message.reply_text(text)


# ==========================================
# TOTAL IDS
# /ids
# ==========================================

@Client.on_message(filters.command("ids"))
async def ids_count(client, message):

    count = db.total_ff_ids()

    await message.reply_text(
        f"🆔 Total Saved IDs: {count}"
    )


# ==========================================
# TOTAL USERS
# /users
# ==========================================

@Client.on_message(filters.command("users"))
async def users_count(client, message):

    count = db.total_users()

    await message.reply_text(
        f"👥 Total Users: {count}"
    )


# ==========================================
# TOP UID
# /topuid
# ==========================================

@Client.on_message(filters.command("topuid"))
async def top_uid(client, message):

    data = db.most_viewed()

    if not data:
        return await message.reply_text(
            "❌ No Data Available"
        )

    await message.reply_text(
        f"🏆 Most Viewed UID\n\n"
        f"🆔 UID: {data[0]}\n"
        f"👁 Views: {data[1]}"
    )


# ==========================================
# PENDING COUNT
# /pendingstats
# ==========================================

@Client.on_message(filters.command("pendingstats"))
async def pending_stats(client, message):

    count = len(
        db.get_pending_requests()
    )

    await message.reply_text(
        f"📥 Pending Requests: {count}"
    )
# ==========================================
# TOP 10 VIEWED IDS
# /top10
# ==========================================

@Client.on_message(filters.command("top10"))
async def top10_viewed(client, message):

    data = db.top_10_viewed()

    if not data:
        return await message.reply_text(
            "❌ No Data Available"
        )

    text = "🏆 TOP 10 VIEWED FF IDs\n\n"

    for i, row in enumerate(data, start=1):

        text += (
            f"{i}. 🆔 {row[0]}\n"
            f"👤 {row[1]}\n"
            f"👁 Views: {row[2]}\n\n"
        )

    await message.reply_text(text)
