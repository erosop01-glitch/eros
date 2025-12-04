from config import FORCE_CHANNELS
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def is_joined_all(bot, uid):
    for ch in FORCE_CHANNELS:
        ch = ch.strip()
        if not ch:
            continue
        try:
            status = bot.get_chat_member(ch, uid).status
            if status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True


def send_force_join(bot, uid):
    markup = InlineKeyboardMarkup()
    for ch in FORCE_CHANNELS:
        ch = ch.strip()
        if ch:
            markup.add(
                InlineKeyboardButton("📌 Join Channel", url=f"https://t.me/{ch.replace('-100','')}")
            )

    bot.send_message(
        uid,
        "⚠ *Join our channel to use the bot!*\nThen press /start.",
        reply_markup=markup,
        parse_mode="Markdown"
    )


def bypass_admin(uid):
    from config import ADMIN_ID
    from admin import is_admin

    return uid == ADMIN_ID or is_admin(uid)
