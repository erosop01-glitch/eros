from database import db, save_db

if "logs" not in db:
    db["logs"] = []
    save_db()


def log_action(admin_id, action):
    db["logs"].append({
        "admin": admin_id,
        "action": action
    })
    save_db()


def get_last_logs(n=20):
    logs = db["logs"][-n:]
    text = "📜 *Admin Logs:*\n\n"
    for l in logs:
        text += f"- {l['action']} (by {l['admin']})\n"
    return text
