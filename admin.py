from config import *
from utils import *
from database import db, save_db
from telebot import types

# ---------------------
# ADMIN CHECK WRAPPER
# ---------------------
def admin_only(func):
    def wrapper(bot, message):
        uid = message.from_user.id
        if str(uid) != str(ADMIN_ID):
            return bot.reply_to(message, "❌ You are not authorized to use admin commands.")
        return func(bot, message)
    return wrapper


# ---------------------
# HANDLE ADMIN COMMANDS
# ---------------------
@admin_only
def handle_admin_commands(bot, message):
    uid = message.from_user.id
    text = message.text.split()
    cmd = text[0].lower()

    # Extract target user if needed
    target = text[1] if len(text) > 1 else None

    # Ensure DB safety
    if target not in db:
        db[target] = {"credits": 0, "ref_by": None}
        save_db(db)

    # FIX: Ensure proper dictionary
    user = db.get(target, {})
    if not isinstance(user, dict):
        user = {"credits": 0, "ref_by": None}
        db[target] = user
        save_db(db)

    # -------------------------
    # ADMIN COMMANDS START HERE
    # -------------------------

    # Add Credits
    if cmd == "addcredits":
        amount = int(text[2])
        user["credits"] += amount
        save_db(db)
        return bot.reply_to(message, f"✅ Added {amount} credits to {target}")

    # Remove Credits
    elif cmd == "remcredits":
        amount = int(text[2])
        user["credits"] = max(0, user["credits"] - amount)
        save_db(db)
        return bot.reply_to(message, f"✅ Removed {amount} credits from {target}")

    # Check User Info
    elif cmd == "userinfo":
        msg = f"""
👤 **User Info**
ID: `{target}`
Credits: `{user.get('credits', 0)}`
Referred by: `{user.get('ref_by', None)}`
"""
        return bot.reply_to(message, msg, parse_mode="Markdown")

    # Broadcast Message
    elif cmd == "broadcast":
        send_msg = message.text.replace("broadcast ", "")
        for u in db.keys():
            try:
                bot.send_message(u, send_msg)
            except:
                pass
        return bot.reply_to(message, "📢 Broadcast sent to all users!")

    # Update User Referral Reset
    elif cmd == "resetref":
        user["ref_by"] = None
        save_db(db)
        return bot.reply_to(message, f"🔄 Referral reset for {target}")

    # List All Users
    elif cmd == "users":
        return bot.reply_to(message, f"👥 Total Users: {len(db)}")

    # Admin Help
    elif cmd == "adminhelp":
        return bot.reply_to(
            message,
            """
🔐 **ADMIN PANEL**  
Commands:
