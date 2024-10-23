import requests

# Discord webhook URL
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"  # Placeholder text

def send_discord_notification(message):
    if WEBHOOK_URL == "YOUR_DISCORD_WEBHOOK_URL":
        print("Discord webhook URL is not set. Skipping notification.")
        return
    
    data = {
        "content": message
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code == 204:
        print("Notification sent successfully.")
    else:
        print(f"Failed to send notification. Status code: {response.status_code}")