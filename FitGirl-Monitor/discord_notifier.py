import requests

# Discord webhook URL
WEBHOOK_URL = "https://discordapp.com/api/webhooks/1297250640421978222/tLAXWYBdv_QnlElu_Jv5JuAATK3DoKEqxlep4bBToQeJHuOdEZYUh1iltANhK2xnDDba", # Insert your Discord webhook URL here and wrap it in quotes. Ex: "https://discordapp.com/api/webhooks/65498818987357/1568789845621859"

def send_discord_notification(message):
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")