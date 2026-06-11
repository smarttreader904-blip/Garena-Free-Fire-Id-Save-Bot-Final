# ==========================================
# admin.py
# FF ID Management Bot Admin System
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import Message
import csv

import config
import database as db


# ==========================================
# CHECK ADMIN
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# ADMIN PANEL
# ==========================================

@Client.on_message(filters.command("admin"))
async def admin_panel(client, message: Message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "❌ You Are Not Admin"
        )

    await message.reply_text(
        "👑 Admin Panel\n\n"
        "/pending - Pending Requests\n"
        "/stats - Bot Statistics\n"
        "/logs - View Logs\n"
        "/broadcast - Broadcast Message"
    )


# ==========================================
# ADMIN ADD ID
# /adminadd UID NAME CATEGORY
# ==========================================

@Client.on_message(filters.command("adminadd"))
async def admin_add(client, message):

    if not is_admin(message.from_user.id):
        return

    if len(message.command) < 4:
        return await message.reply_text(
            "Usage:\n/adminadd UID NAME CATEGORY"
        )

    uid = message.command[1]
    nickname = message.command[2]
    category = message.command[3]

    if db.uid_exists(uid):
        return await message.reply_text(
            "❌ UID Already Exists"
        )

    db.add_ff_id(
        message.from_user.id,
        uid,
        nickname,
        category
    )

    db.add_log(
        "ADMIN_ADD",
        message.from_user.id,
        uid
    )

    await message.reply_text(
        f"✅ FF ID Added\n\nUID: {uid}"
    )


# ==========================================
# DELETE FF ID
# /delete UID
# ==========================================

@Client.on_message(filters.command("delete"))
async def delete_id(client, message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/delete UID"
        )

    uid = message.command[1]

    data = db.get_ff_by_uid(uid)

    if not data:
        return await message.reply_text(
            "❌ UID Not Found"
        )

    db.delete_ff_id(uid)

    db.add_log(
        "DELETE",
        message.from_user.id,
        uid
    )

    await message.reply_text(
        f"🗑 Deleted UID: {uid}"
    )


# ==========================================
# EDIT FF ID
# /edit UID NEW_NAME
# ==========================================

@Client.on_message(filters.command("edit"))
async def edit_id(client, message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    if len(message.command) < 3:
        return await message.reply_text(
            "Usage:\n/edit UID NEW_NAME"
        )

    uid = message.command[1]
    new_name = " ".join(
        message.command[2:]
    )

    db.edit_ff_id(
        uid,
        new_name
    )

    db.add_log(
        "EDIT",
        message.from_user.id,
        uid
    )

    await message.reply_text(
        f"✏️ Updated\n\nUID: {uid}\nNew Name: {new_name}"
    )


# ==========================================
# BROADCAST
# ==========================================

@Client.on_message(filters.command("broadcast"))
async def broadcast(client, message):

    if not is_admin(message.from_user.id):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "Usage:\n/broadcast MESSAGE"
        )

    text = message.text.split(
        " ", 1
    )[1]

    users = db.get_all_users()

    sent = 0

    for user in users:
        try:
            await client.send_message(
                user[0],
                f"📢 Broadcast\n\n{text}"
            )
            sent += 1
        except:
            pass

    await message.reply_text(
        f"✅ Sent To {sent} Users"
    )


# ==========================================
# EXPORT TXT
# ==========================================

@Client.on_message(filters.command("exporttxt"))
async def export_txt(client, message):

    if not is_admin(message.from_user.id):
        return

    data = db.get_all_ff_ids()

    text = ""

    for row in data:

        text += (
            f"UID: {row[2]}\n"
            f"NAME: {row[3]}\n"
            f"CATEGORY: {row[4]}\n\n"
        )

    with open(
        "ff_ids.txt",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(text)

    await message.reply_document(
    "ff_ids.txt"
)

# ==========================================
# EXPORT CSV
# ==========================================

@Client.on_message(filters.command("exportcsv"))
async def export_csv(client, message):

    if not is_admin(message.from_user.id):
        return await message.reply_text(
            "🚫 Not Allowed"
        )

    data = db.get_all_ff_ids()

    with open(
        "ff_ids.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "USER_ID",
            "UID",
            "NICKNAME",
            "CATEGORY",
            "STATUS",
            "VIEWS",
            "FAVORITE",
            "CREATED_AT"
        ])

        for row in data:
            writer.writerow(row)

    await message.reply_document(
        "ff_ids.csv",
        caption="📊 FF IDs CSV Export"
    )
