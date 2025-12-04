from database import db, save_db
from logs import log_action
from config import ADMIN_ID
from utils import is_admin_id


def is_admin(uid):
    uid = str(uid)
    return uid == str(ADMIN_ID) or ("admins" in db and uid in db["admins"])


def handle_admin_commands(bot, message):
    uid = message.from_user.id
    text = message.text.split()

    if not is_admin(uid):
        return bot.send_message(uid, "❌ Admin only.")

    cmd = text[0]

    # -------------------
    # ADD ADMIN
    # -------------------
    if cmd == "/admin":
        if len(text) < 2:
            return bot.send_message(uid, "Use: /admin USERID")

        target = text[1]
        if "admins" not in db:
            db["admins"] = []

        if target not in db["admins"]:
            db["admins"].append(target)
            save_db()
            log_action(uid, f"Added admin {target}")
            return bot.send_message(uid, f"✅ Admin added: {target}")

    # -------------------
    # REMOVE ADMIN
    # -------------------
    if cmd == "/unadmin":
        if len(text) < 2:
            return bot.send_message(uid, "Use: /unadmin USERID")

        target = text[1]
        if target in db["admins"]:
            db["admins"].remove(target)
            save_db()
            log_action(uid, f"Removed admin {target}")
            return bot.send_message(uid, f"❎ Admin removed: {target}")

    # -------------------
    # ADMIN LIST
    # -------------------
    if cmd == "/admins":
        if "admins" not in db or not db["admins"]:
            return bot.send_message(uid, "No admins yet.")

        text = "👑 *Admins:*\n" + "\n".join(db["admins"])
        return bot.send_message(uid, text, parse_mode="Markdown")

    # -------------------
    # ADD CREDITS
    # -------------------
    if cmd == "/addcredits":
        if len(text) < 3:
            return bot.send_message(uid, "Use: /addcredits USERID AMOUNT")

        target = text[1]
        amount = int(text[2])

        if target not in db:
            return bot.send_message(uid, "User not found.")

        db[target]["credits"] += amount
        save_db()

        log_action(uid, f"Added {amount} credits to {target}")
        return bot.send_message(uid, f"✅ Added {amount} credits to {target}")

    # -------------------
    # REMOVE CREDITS
    # -------------------
    if cmd == "/remcredits":
        if len(text) < 3:
            return bot.send_message(uid, "Use: /remcredits USERID AMOUNT")

        target = text[1]
        amount = int(text[2])

        if target not in db:
            return bot.send_message(uid, "User not found.")

        db[target]["credits"] = max(0, db[target]["credits"] - amount)
        save_db()

        log_action(uid, f"Removed {amount} credits from {target}")
        return bot.send_message(uid, f"❎ Removed {amount} credits from {target}")

    # -------------------
    # BROADCAST
    # -------------------
    if cmd == "/broadcast":
        msg = message.text.replace("/broadcast ", "")
        for u in db:
            try:
                bot.send_message(u, msg)
            except:
                pass
        log_action(uid, "Broadcast sent")
        return bot.send_message(uid, "📢 Broadcast sent.")

    # -------------------
    # REFILL ALL USERS
    # -------------------
    if cmd == "/refillall":
        if len(text) < 2:
            return bot.send_message(uid, "Use: /refillall AMOUNT")

        amount = int(text[1])
        count = 0

        for u in db:
            if u.isdigit():
                db[u]["credits"] += amount
                count += 1

        save_db()
        log_action(uid, f"Refilled {amount} to all users")

        return bot.send_message(uid, f"🔥 Refilled {amount} credits to {count} users.")

    # -------------------
    # REFERRAL RANKING
    # -------------------
    if cmd == "/reftop":
        counts = {}

        for u in db:
            if db[u].get("ref_by"):
                r = db[u]["ref_by"]
                counts[r] = counts.get(r, 0) + 1

        if not counts:
            return bot.send_message(uid, "No referrals yet.")

        sorted_list = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        text = "🏆 *Top Referrers:*\n\n"
        for i, (user, cnt) in enumerate(sorted_list[:10], start=1):
            text += f"{i}) `{user}` — {cnt}\n"

        return bot.send_message(uid, text, parse_mode="Markdown")

    # -------------------
    # VIEW LOGS
    # -------------------
    if cmd == "/logs":
        from logs import get_last_logs
        logs = get_last_logs(20)
        return bot.send_message(uid, logs, parse_mode="Markdown")

    bot.send_message(uid, "Unknown admin command.")
