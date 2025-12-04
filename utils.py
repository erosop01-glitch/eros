from config import ADMIN_ID
from database import db

def is_admin_id(uid):
    return str(uid) == str(ADMIN_ID) or str(uid) in db.get("admins", {})
