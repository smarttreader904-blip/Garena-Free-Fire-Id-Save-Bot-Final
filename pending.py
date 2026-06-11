# ==========================================
# pending.py
# FF ID Management Bot Pending System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

import config
import database as db
import keyboards


# ==========================================
# CHECK ADMIN
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# SHOW PENDING LIST
# ==========================================

@Client.on_message(filters.command("pending"))
async def pending_list(client, message: Message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    requests = db.get_pending_requests()

    if not requests:
        return await message.reply_text(
            "✅ No Pending Requests"
        )

    text = "📥 Pending Requests\n\n"

    for req in requests:

    text = (
        f"🆔 UID: {req['uid']}\n"
        f"👤 Name: {req['nickname']}\n"
        f"🏆 Category: {req['category']}\n"
        f"👤 User ID: {req['user_id']}"
    )

    await message.reply_text(
        text,
        reply_markup=keyboards.approve_reject(
            req["uid"]
        )
    )


# ==========================================
# APPROVE REQUEST
# /approve UID
# ==========================================

@Client.on_message(filters.command("approve"))
async def approve_uid(client, message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/approve UID"
        )

    uid = message.command[1]

    data = db.approve_request(uid)

    if not data:
        return await message.reply_text(
            "❌ Pending UID Not Found"
        )

    db.add_log(
        "APPROVE",
        message.from_user.id,
        uid
    )

    # User Notification
    try:
        await client.send_message(
            data[1],
            f"✅ Your FF ID Approved\n\nUID: {uid}"
        )
    except:
        pass

    await message.reply_text(
        f"✅ Approved UID: {uid}"
    )


# ==========================================
# REJECT REQUEST
# /reject UID
# ==========================================

@Client.on_message(filters.command("reject"))
async def reject_uid(client, message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/reject UID"
        )

    uid = message.command[1]

    requests = db.get_pending_requests()

    target_user = None

    for req in requests:
        if req["uid"] == uid:
            target_user = req["user_id"]
            break

    db.reject_request(uid)

    db.add_log(
        "REJECT",
        message.from_user.id,
        uid
    )

    # User Notification
    if target_user:
        try:
            await client.send_message(
                target_user,
                f"❌ Your FF ID Rejected\n\nUID: {uid}"
            )
        except:
            pass

    await message.reply_text(
        f"❌ Rejected UID: {uid}"
    )


# ==========================================
# CLEAR ALL PENDING
# /clearpending
# ==========================================

@Client.on_message(filters.command("clearpending"))
async def clear_pending_cmd(client, message):

    if not is_admin(message.from_user.id):
        return

    db.clear_pending()

    await message.reply_text(
        "🗑 All Pending Requests Cleared"
    )


# ==========================================
# PENDING COUNT
# ==========================================

@Client.on_message(filters.command("pendingcount"))
async def pending_count(client, message):

    if not is_admin(message.from_user.id):
        return

    count = len(
        db.get_pending_requests()
    )

    await message.reply_text(
    f"📥 Total Pending: {count}"
)

# ==========================================
# INLINE APPROVE / REJECT
# ==========================================

@Client.on_callback_query()
async def approve_reject_callback(client, callback: CallbackQuery):

    if callback.from_user.id not in config.ADMIN_IDS:
        return await callback.answer(
            "Not Admin",
            show_alert=True
        )

    data = callback.data

    if data.startswith("approve_"):

        uid = data.replace("approve_", "")

        result = db.approve_request(uid)

        if not result:
            return await callback.answer(
                "UID Not Found"
            )

        db.add_log(
            "APPROVE",
            callback.from_user.id,
            uid
        )

        await callback.message.edit_text(
            f"✅ Approved\n\nUID: {uid}"
        )

        return await callback.answer(
            "Approved"
        )

    elif data.startswith("reject_"):

        uid = data.replace("reject_", "")

        db.reject_request(uid)

        db.add_log(
            "REJECT",
            callback.from_user.id,
            uid
        )

        await callback.message.edit_text(
            f"❌ Rejected\n\nUID: {uid}"
        )

        return await callback.answer(
            "Rejected"
        )
