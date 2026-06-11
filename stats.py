# ==========================================
# utils.py
# FF ID Management Bot Utilities
# ==========================================

from datetime import datetime
import config


# ==========================================
# CHECK ADMIN
# ==========================================

def is_admin(user_id):
    return user_id in config.ADMIN_IDS


# ==========================================
# CURRENT TIME
# ==========================================

def get_time():
    return datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


# ==========================================
# FORMAT FF DETAILS
# ==========================================

def format_ff(data):

    if not data:
        return "❌ No Data Found"

    return f"""
🎮 FF ID Details

🆔 UID: {data[2]}
👤 Nickname: {data[3]}
🏆 Category: {data[4]}
📊 Status: {data[5]}
👁 Views: {data[6]}
⭐ Favorite: {data[7]}
📅 Saved: {data[8]}
"""


# ==========================================
# SUCCESS MESSAGE
# ==========================================

def success(text):
    return f"✅ {text}"


# ==========================================
# ERROR MESSAGE
# ==========================================

def error(text):
    return f"❌ {text}"


# ==========================================
# NOT ALLOWED
# ==========================================

def not_allowed():
    return "🚫 Not Allowed"


# ==========================================
# DUPLICATE UID
# ==========================================

def duplicate_uid():
    return "⚠️ UID Already Exists"


# ==========================================
# PENDING MESSAGE
# ==========================================

def pending_message(uid):
    return (
        f"📥 Request Submitted\n\n"
        f"UID: {uid}\n"
        f"Status: Pending Approval"
    )


# ==========================================
# APPROVED MESSAGE
# ==========================================

def approved_message(uid):
    return (
        f"✅ FF ID Approved\n\n"
        f"UID: {uid}"
    )


# ==========================================
# REJECTED MESSAGE
# ==========================================

def rejected_message(uid):
    return (
        f"❌ FF ID Rejected\n\n"
        f"UID: {uid}"
    )


# ==========================================
# BROADCAST FORMAT
# ==========================================

def broadcast_message(text):
    return (
        "📢 Broadcast Message\n\n"
        f"{text}"
    )


# ==========================================
# CATEGORY LIST
# ==========================================

CATEGORIES = [
    "Bronze",
    "Silver",
    "Gold",
    "Platinum",
    "Diamond",
    "Heroic",
    "Grandmaster"
    ]
