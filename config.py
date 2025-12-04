import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
FORCE_CHANNELS = os.getenv("FORCE_CHANNELS", "").split(",")

ADMIN_USERNAME = "@incognitovirus"

# Help Menus
USER_HELP = """
🤖 USER COMMANDS
━━━━━━━━━━━━━━
🔍 SEARCH:
/mobile 9876543210
/number 123456789012
/email abc@gmail.com
/domain google.com
/ip 1.1.1.1
/vehicle MP09AB1234
/tgid 123456789
/instaid username

🎁 REWARDS:
/bonus
/redeem CODE

💳 CREDITS:
/profile
/send USERID AMOUNT

📞 Admin Contact:
@incognitovirus
"""

ADMIN_HELP = USER_HELP + """
👑 ADMIN PANEL
━━━━━━━━━━━━━━
/admin USERID
/unadmin USERID
/admins

/addcredits USERID AMOUNT
/remcredits USERID AMOUNT

/block USERID
/unblock USERID

/broadcast TEXT
/makecode CODE AMOUNT MAXUSE

/refillall AMOUNT
/reftop
/logs
"""
