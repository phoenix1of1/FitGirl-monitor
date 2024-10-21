import requests

# Discord webhook URL
WEBHOOK_URL = "https://discordapp.com/api/webhooks/65498818987357/1568789845621859"  # Insert your Discord webhook URL here and wrap it in quotes.

def send_discord_notification(message):
    data = {
        "content": message
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        if response.status_code == 204:
            print("Notification sent successfully.")
        else:
            print(f"Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification. Error: {e}")

# Example usage
send_discord_notification("Test message")