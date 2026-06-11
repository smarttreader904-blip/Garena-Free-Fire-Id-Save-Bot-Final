# ==========================================
# logs.py
# FF ID Management Bot Logs System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import config
import database as db


# ==========================================
# 👑 ADMIN CHECK
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# 📜 VIEW LOGS COMMAND
# ==========================================

@Client.on_message(filters.command("logs"))
def view_logs(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    logs = db.get_logs()

    if not logs:
        return message.reply("📭 No Logs Found")

    text = "📜 Approval / Reject Logs\n\n"

    for log in logs[:20]:
        text += (
            f"🆔 UID: {log[3]}\n"
            f"⚙️ Action: {log[1]}\n"
            f"👑 Admin: {log[2]}\n"
            f"📅 Date: {log[4]}\n\n"
        )

    message.reply(text)


# ==========================================
# 📊 LOG STATS
# ==========================================

@Client.on_message(filters.command("logstats"))
def log_stats(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    logs = db.get_logs()

    total_logs = len(logs)

    approve_count = 0
    reject_count = 0
    delete_count = 0

    for log in logs:

        action = str(log[1]).lower()

        if action == "approve":
            approve_count += 1

        elif action == "reject":
            reject_count += 1

        elif action == "delete":
            delete_count += 1

    message.reply(
        f"📊 Log Statistics\n\n"
        f"📜 Total Logs: {total_logs}\n"
        f"✅ Approvals: {approve_count}\n"
        f"❌ Rejects: {reject_count}\n"
        f"🗑 Deletes: {delete_count}"
    )


# ==========================================
# 🧹 CLEAR LOGS
# ==========================================

@Client.on_message(filters.command("clearlogs"))
def clear_logs(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🧹 Confirm",
                callback_data="confirm_clear_logs"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Cancel",
                callback_data="cancel_clear_logs"
            )
        ]
    ])

    message.reply(
        "⚠️ Are you sure you want to clear all logs?",
        reply_markup=buttons
    )


# ==========================================
# ✅ CONFIRM CLEAR LOGS
# ==========================================

@Client.on_callback_query(
    filters.regex("^confirm_clear_logs$")
)
def confirm_clear_logs(client, callback_query):

    if not is_admin(callback_query.from_user.id):
        return callback_query.answer(
            "Not Allowed",
            show_alert=True
        )

    try:
        db.clear_logs()
    except:
        pass

    callback_query.message.edit_text(
        "✅ All logs cleared successfully."
    )


# ==========================================
# ❌ CANCEL CLEAR LOGS
# ==========================================

@Client.on_callback_query(
    filters.regex("^cancel_clear_logs$")
)
def cancel_clear_logs(client, callback_query):

    callback_query.message.edit_text(
        "❌ Log clear cancelled."
    )


# ==========================================
# 🔍 SEARCH LOG BY UID
# ==========================================

@Client.on_message(filters.command("searchlog"))
def search_log(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    args = message.text.split()

    if len(args) < 2:
        return message.reply(
            "Usage:\n/searchlog UID"
        )

    uid = args[1]

    logs = db.get_logs()

    result = []

    for log in logs:
        if str(log[3]) == uid:
            result.append(log)

    if not result:
        return message.reply(
            "📭 No log found for this UID."
        )

    text = f"🔍 Logs for UID: {uid}\n\n"

    for log in result[:20]:
        text += (
            f"⚙️ {log[1]}\n"
            f"👑 {log[2]}\n"
            f"📅 {log[4]}\n\n"
        )

    message.reply(text)


# ==========================================
# 📁 EXPORT LOGS TXT
# ==========================================

@Client.on_message(filters.command("exportlogs"))
def export_logs(client, message):

    if not is_admin(message.from_user.id):
        return message.reply("❌ Not Allowed")

    logs = db.get_logs()

    if not logs:
        return message.reply("📭 No Logs Found")

    with open("logs_export.txt", "w", encoding="utf-8") as f:

        for log in logs:

            f.write(
                f"UID: {log[3]} | "
                f"Action: {log[1]} | "
                f"Admin: {log[2]} | "
                f"Date: {log[4]}\n"
            )

    client.send_document(
        message.chat.id,
        "logs_export.txt",
        caption="📤 Logs Export"
)
