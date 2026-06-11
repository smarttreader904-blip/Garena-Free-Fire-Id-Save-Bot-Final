# ==========================================
# utils.py
# FF ID Management Bot Utilities
# ==========================================

from datetime import datetime
import csv
import config


# ==========================================
# 📅 CURRENT DATE TIME
# ==========================================

def current_datetime():
    return datetime.now().strftime(
        f"{config.DATE_FORMAT} {config.TIME_FORMAT}"
    )


# ==========================================
# 📅 CURRENT DATE
# ==========================================

def current_date():
    return datetime.now().strftime(
        config.DATE_FORMAT
    )


# ==========================================
# 🕒 CURRENT TIME
# ==========================================

def current_time():
    return datetime.now().strftime(
        config.TIME_FORMAT
    )


# ==========================================
# 🔍 VALID UID CHECK
# ==========================================

def valid_uid(uid):

    if not uid.isdigit():
        return False

    if len(uid) < 6:
        return False

    return True


# ==========================================
# 👤 VALID NAME CHECK
# ==========================================

def valid_name(name):

    if len(name.strip()) < 2:
        return False

    return True


# ==========================================
# 🗂 VALID CATEGORY
# ==========================================

def valid_category(category):

    return category in config.CATEGORIES


# ==========================================
# ⭐ STATUS FORMAT
# ==========================================

def status_text(status):

    if status == "approved":
        return "✅ Approved"

    elif status == "rejected":
        return "❌ Rejected"

    elif status == "pending":
        return "📥 Pending"

    return "Unknown"


# ==========================================
# 📊 NUMBER FORMAT
# ==========================================

def format_number(number):
    return "{:,}".format(number)


# ==========================================
# 📝 LOG FORMAT
# ==========================================

def make_log(action, admin_id, uid):

    return (
        f"[{current_datetime()}] "
        f"{action} | "
        f"Admin: {admin_id} | "
        f"UID: {uid}"
    )


# ==========================================
# 📤 EXPORT TXT
# ==========================================

def export_txt(data, filename="ff_ids.txt"):

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        for row in data:
            file.write(str(row) + "\n")

    return filename


# ==========================================
# 📤 EXPORT CSV
# ==========================================

def export_csv(data, filename="ff_ids.csv"):

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        for row in data:
            writer.writerow(row)

    return filename


# ==========================================
# 🎮 FF ID FORMAT
# ==========================================

def ff_details(uid, nickname, category):

    return (
        f"🎮 FF ID Details\n\n"
        f"🆔 UID: {uid}\n"
        f"👤 Nickname: {nickname}\n"
        f"🏆 Category: {category}"
    )


# ==========================================
# 📈 VIEW FORMAT
# ==========================================

def view_text(views):

    return f"👀 Views: {views}"


# ==========================================
# ⭐ FAVORITE FORMAT
# ==========================================

def favorite_text():

    return "⭐ Added To Favorites"


# ==========================================
# 🚫 NOT ALLOWED
# ==========================================

def not_allowed():

    return "❌ Not Allowed"


# ==========================================
# ✅ SUCCESS
# ==========================================

def success(text="Success"):

    return f"✅ {text}"


# ==========================================
# ❌ ERROR
# ==========================================

def error(text="Error"):

    return f"❌ {text}"
