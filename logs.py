# ==========================================
# logs.py
# FF ID Management Bot Logs System
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
# SHOW LOGS
# /logs
# ==========================================

@Client.on_message(filters.command("logs"))
async def show_logs(client, message: Message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    logs = db.get_logs()

    if not logs:
        return await message.reply_text(
            "📜 No Logs Found"
        )

    text = "📜 Latest Logs\n\n"

    for log in logs[:30]:

        text += (
            f"🆔 UID: {log[3]}\n"
            f"⚡ Action: {log[1]}\n"
            f"👑 Admin: {log[2]}\n"
            f"📅 Date: {log[4]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# LOGS BY UID
# /loguid UID
# ==========================================

@Client.on_message(filters.command("loguid"))
async def logs_by_uid(client, message):

    if not is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/loguid UID"
        )

    uid = message.command[1]

    logs = db.get_logs_by_uid(uid)

    if not logs:
        return await message.reply_text(
            "❌ No Logs Found"
        )

    text = f"📜 Logs For UID {uid}\n\n"

    for log in logs:

        text += (
            f"⚡ {log[1]}\n"
            f"👑 Admin: {log[2]}\n"
            f"📅 {log[4]}\n\n"
        )

    await message.reply_text(text)


# ==========================================
# TOTAL LOGS
# /totallogs
# ==========================================

@Client.on_message(filters.command("totallogs"))
async def total_logs(client, message):

    if not is_admin(message.from_user.id):
        return

    count = db.total_logs()

    await message.reply_text(
        f"📊 Total Logs: {count}"
    )


# ==========================================
# CLEAR LOGS
# /clearlogs
# ==========================================

@Client.on_message(filters.command("clearlogs"))
async def clear_logs(client, message):

    if not is_admin(message.from_user.id):
        return

    db.clear_logs()

    await message.reply_text(
        "🗑 All Logs Cleared"
    )


# ==========================================
# EXPORT LOGS
# /exportlogs
# ==========================================

@Client.on_message(filters.command("exportlogs"))
async def export_logs(client, message):

    if not is_admin(message.from_user.id):
        return

    logs = db.get_logs()

    text = ""

    for log in logs:

        text += (
            f"UID: {log[3]}\n"
            f"ACTION: {log[1]}\n"
            f"ADMIN: {log[2]}\n"
            f"DATE: {log[4]}\n"
            f"{'-'*30}\n"
        )

    with open(
        "logs.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)

    await message.reply_document(
        "logs.txt"
        )
