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

    # Extract user id argument
    target = text[1] if len(text) > 1 else None

    # Ensure DB safety
    if target not in db:
        db[target] = {"credits": 0, "ref_by": None}
        save_db(db)

    # Make sure target user entry is dictionary
    user = db.get(target, {})
    if not isinstance(user, dict):
        user = {"credits": 0, "ref_by": None}
        db[target] = user
        save_db(db)

    # -------------------------
    # ADMIN COMMANDS
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
        msg = (
            f"👤 *User Info*\n"
            f"ID: `{target}`\n"
            f"Credits: `{user.get('credits', 0)}`\n"
            f"Referred by: `{user.get('ref_by', None)}`"
        )
        return bot.reply_to(message, msg, parse_mode="Markdown")

    # Broadcast
    elif cmd == "broadcast":
        send_msg = message.text.replace("broadcast ", "")
        for u in db.keys():
            try:
                bot.send_message(u, send_msg)
            except:
                pass
        return bot.reply_to(message, "📢 Broadcast sent to all users!")

    # Reset Referral
    elif cmd == "resetref":
        user["ref_by"] = None
        save_db(db)
        return bot.reply_to(message, f"🔄 Referral reset for {target}")

    # Total users
    elif cmd == "users":
        return bot.reply_to(message, f"👥 Total Users: {len(db)}")

    # Admin help
    elif cmd == "adminhelp":
        help_text = (
            "🔐 *ADMIN PANEL COMMANDS*\n\n"
            "`addcredits <uid> <amount>`\n"
            "`remcredits <uid> <amount>`\n"
            "`userinfo <uid>`\n"
            "`broadcast <text>`\n"
            "`resetref <uid>`\n"
            "`users`\n"
        )
        return bot.reply_to(message, help_text, parse_mode="Markdown")

    else:
        return bot.reply_to(message, "❌ Unknown admin command.")
