import json

DB_FILE = "users.json"

def load_db():
    try:
        return json.load(open(DB_FILE, "r"))
    except:
        return {}

def save_db():
    json.dump(db, open(DB_FILE, "w"), indent=4)

db = load_db()

# INIT USER
def init_user(uid):
    uid = str(uid)
    if uid not in db:
        db[uid] = {
            "credits": 10,
            "bonus_given": False,
            "ref_bonus_given": False,
            "ref_by": None,
            "cooldown": 0,
            "blocked": False,
            "redeemed_codes": []
        }
        save_db()
