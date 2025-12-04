from database import db, save_db
import time

def apply_welcome_reward(bot, uid, ref):
    uid = str(uid)

    if db[uid]["bonus_given"] is False:
        db[uid]["credits"] += 5
        db[uid]["bonus_given"] = True
        save_db()
        bot.send_message(uid, "🎉 +5 Welcome Credits Added!")

    # referral check
    if ref and ref != uid and ref in db and db[uid]["ref_bonus_given"] is False:
        db[uid]["credits"] += 5
        db[str(ref)]["credits"] += 5
        db[uid]["ref_bonus_given"] = True
        db[uid]["ref_by"] = ref
        save_db()

        bot.send_message(uid, "🎁 Referral bonus +5 added!")
        bot.send_message(ref, "🎉 Someone joined using your link! +5 credits")
        

def handle_daily_bonus(bot, message):
    uid = str(message.from_user.id)

    now = time.time()
    if "last_bonus" not in db[uid]:
        db[uid]["last_bonus"] = 0

    if now - db[uid]["last_bonus"] >= 86400:
        db[uid]["credits"] += 5
        db[uid]["last_bonus"] = now
        save_db()
        bot.send_message(uid, "🎁 Daily bonus: +5 credits")
    else:
        bot.send_message(uid, "⏳ Bonus already claimed today.")
