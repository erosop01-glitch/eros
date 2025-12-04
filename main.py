from config import *
from database import *
from force_join import *
from reward import *
from search import *
from admin import *
from logs import *
from utils import *

# ---------------- Render keep-alive tiny web server ----------------
import os
from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running"

port = int(os.environ.get("PORT", 5000))

import threading
threading.Thread(target=lambda: app.run(host="0.0.0.0", port=port)).start()
# -------------------------------------------------------------------

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    text = message.text

    init_user(uid)

    # Referral detect
    ref = None
    if " " in text:
        ref = text.split()[1].replace("REF", "")

    # FORCE JOIN CHECK
    if not bypass_admin(uid):
        if not is_joined_all(bot, uid):
            return send_force_join(bot, uid)

    # APPLY REWARDS
    apply_welcome_reward(bot, uid, ref)

    bot.send_message(
        uid,
        f"👋 Welcome!\nUse /help for commands.\n📞 Admin: {ADMIN_USERNAME}"
    )


@bot.message_handler(commands=['help'])
def help_menu(message):
    uid = message.from_user.id

    if is_admin(uid):
        bot.send_message(uid, ADMIN_HELP, parse_mode="Markdown")
    else:
        bot.send_message(uid, USER_HELP, parse_mode="Markdown")


# -----------------------------
# SEARCH MODULE HANDLING
# -----------------------------
@bot.message_handler(commands=['mobile', 'number', 'email', 'domain', 'ip', 'vehicle', 'tgid', 'instaid'])
def search_handler(message):
    handle_search_command(bot, message)


# -----------------------------
# BONUS
# -----------------------------
@bot.message_handler(commands=['bonus'])
def bonus(message):
    handle_daily_bonus(bot, message)


# -----------------------------
# ADMIN COMMANDS
# -----------------------------
@bot.message_handler(commands=[
    'admin', 'unadmin', 'admins',
    'addcredits', 'remcredits',
    'block', 'unblock',
    'broadcast',
    'makecode',
    'updatelog',
    'stats',
    'resetuser',
    'refillall',
    'reftop',
    'logs'
])
def admin_handler(message):
    handle_admin_commands(bot, message)


# -----------------------------
# GLOBAL PROTECTION
# -----------------------------
@bot.message_handler(func=lambda m: True)
def fallback(message):
    uid = message.from_user.id
    if not bypass_admin(uid):
        if not is_joined_all(bot, uid):
            return send_force_join(bot, uid)

    if not message.text.startswith("/"):
        bot.send_message(uid, "❗ Please use /help")


bot.polling()
