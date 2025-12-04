import time
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import API_URL, API_TOKEN
from database import db, save_db
from logs import log_action

# ------------------------
# COOLDOWN CHECK
# ------------------------
def check_cooldown(uid):
    now = time.time()

    if uid not in db:
        return False, 0

    if now < db[uid]["cooldown"]:
        return False, int(db[uid]["cooldown"] - now)

    db[uid]["cooldown"] = now + 2
    save_db()
    return True, 0


# ------------------------
# API SEARCH
# ------------------------
def api_search(query):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    try:
        r = requests.get(API_URL, params={"query": query}, headers=headers, timeout=10)
        data = r.json()
        if not data:
            return [{"Name": "No Results"}]

        results = []
        for d in data:
            results.append({
                "Name": d.get("Name", "N/A"),
                "Father": d.get("Father Name", "N/A"),
                "Mobile": d.get("Mobile", "N/A"),
                "Alternate": d.get("Alternate", "N/A"),
                "Address": d.get("Address", "N/A"),
                "Circle": d.get("Circle", "N/A"),
                "ID": d.get("Number", "N/A")
            })
        return results

    except Exception as e:
        return [{"Name": "API ERROR", "Address": str(e)}]


# ------------------------
# CARD FORMAT
# ------------------------
def format_card(r, num):
    return f"""
📱 Result #{num}
━━━━━━━━━━━━━━━━━━
👤 Name: {r.get('Name')}
👨‍👦 Father Name: {r.get('Father')}
📞 Mobile: {r.get('Mobile')}
📱 Alternate: {r.get('Alternate')}
🏠 Address: {r.get('Address')}
🌐 Circle: {r.get('Circle')}
🆔 Number : {r.get('ID')}
━━━━━━━━━━━━━━━━━━
"""


# ------------------------
# PAGINATION CACHE
# ------------------------
cache = {}   # qid → pages


def send_page(bot, uid, qid, page):
    pages = cache[qid]

    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("⬅ Prev", callback_data=f"p|prev|{qid}|{page}"),
        InlineKeyboardButton("Next ➡", callback_data=f"p|next|{qid}|{page}")
    )

    bot.send_message(uid, pages[page], reply_markup=markup)


# ------------------------
# CALLBACK HANDLER
# ------------------------
def handle_pagination(bot, call):
    try:
        _, action, qid, page = call.data.split("|")
        page = int(page)
        pages = cache[qid]

        if action == "next":
            page = (page + 1) % len(pages)
        else:
            page = (page - 1) % len(pages)

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("⬅ Prev", callback_data=f"p|prev|{qid}|{page}"),
            InlineKeyboardButton("Next ➡", callback_data=f"p|next|{qid}|{page}")
        )

        bot.edit_message_text(
            pages[page],
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

    except:
        pass



# ------------------------
# MAIN SEARCH EXECUTION
# ------------------------
def do_search(bot, uid, query):
    uid = str(uid)

    # cooldown
    ok, wait = check_cooldown(uid)
    if not ok:
        return bot.send_message(uid, f"⏳ Wait {wait}s")

    # credit check
    if db[uid]["credits"] < 2:
        return bot.send_message(uid, "❌ Not enough credits.\n📞 Contact admin: @incognitovirus")

    # deduct credits
    db[uid]["credits"] -= 2
    save_db()

    results = api_search(query)
    pages = [format_card(r, i+1) for i, r in enumerate(results)]

    qid = str(time.time())
    cache[qid] = pages
    send_page(bot, uid, qid, 0)


# ------------------------
# USER COMMAND HANDLER
# ------------------------
def handle_search_command(bot, message):
    uid = message.from_user.id
    cmd = message.text.split()[0]
    args = message.text.split()

    # REQUIRED PARAM
    if len(args) < 2:
        return bot.send_message(uid, f"❌ Usage: {cmd} VALUE")

    value = args[1]

    # validation rules
    if cmd == "/mobile":
        if not value.isdigit() or len(value) != 10:
            return bot.send_message(uid, "❌ INVALID MOBILE")

    if cmd == "/number":
        if not value.isdigit():
            return bot.send_message(uid, "❌ INVALID NUMBER")

    # PASS TO SEARCH ENGINE
    do_search(bot, uid, value)

    log_action(uid, f"Search {cmd} {value}")
