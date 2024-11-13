import feedparser
import time
from datetime import datetime, timedelta
import logger  # Import the logging module
from discord_notifier import send_discord_notification  # Import the notification function
import winsound  # Import the winsound function
import os  # Import the os module to check file existence

# URL of the RSS feed
RSS_FEED_URL = "http://fitgirl-repacks.site/feed/"

# ANSI escape codes for colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
PURPLE = '\033[95m'
LIGHT_BLUE = '\033[94m'
RED = '\033[91m'
RESET = '\033[0m'

# Path to the sound file
SOUND_FILE_PATH = r"path\to\file\level-up-191997.mp3"

# Function to play sound alert
def play_sound_alert():
    if os.path.exists(SOUND_FILE_PATH):
        winsound.PlaySound(SOUND_FILE_PATH, winsound.SND_FILENAME)
    else:
        logger.log_error(f"Sound file not found: {SOUND_FILE_PATH}")

# Function to fetch and parse the RSS feed
def fetch_feed():
    return feedparser.parse(RSS_FEED_URL)

# Function to check for new posts
def check_for_new_posts(latest_post_id):
    feed = fetch_feed()
    if feed.entries:
        latest_entry = feed.entries[0]
        second_latest_entry = feed.entries[1] if len(feed.entries) > 1 else None
        
        # Discard posts without a title or with specific titles
        if (not latest_entry.title or 
            latest_entry.title == "Upcoming Repacks" or 
            latest_entry.title == "A Call for Donations" or 
            latest_entry.title.startswith("Updates Digest for")):
            return latest_post_id, None, None
        
        # Extract the article ID from the entry link
        latest_entry_id = latest_entry.link.split('/')[-2]
        
        if latest_entry_id != latest_post_id:
            # Extract the HTTP link and title from the entry
            http_link = latest_entry.link
            title = latest_entry.title
            
            # Send a notification
            send_discord_notification(f"New post found: {title} - {http_link}")
            
            # Play sound alert
            play_sound_alert()
            
            # Update the latest post ID
            return latest_entry_id, title, http_link
    else:
        logger.log_error("No entries found in the RSS feed.")
    
    return latest_post_id, None, None

def main():
    # Initialize the latest post title with the title of the latest valid post from the RSS feed
    feed = fetch_feed()
    latest_post_title = "No posts yet"
    latest_post_id = None
    latest_post_url = None
    
    for entry in feed.entries:
        if (entry.title and 
            entry.title != "Upcoming Repacks" and 
            entry.title != "A Call for Donations" and 
            not entry.title.startswith("Updates Digest for")):
            latest_post_title = entry.title
            latest_post_id = entry.link.split('/')[-2]
            latest_post_url = entry.link
            break

    check_interval = 60  # Interval in seconds
    cycle_counter = 0

    while True:
        cycle_counter += 1
        latest_post_id, new_post_title, new_post_url = check_for_new_posts(latest_post_id)
        
        if new_post_title and new_post_url:
            latest_post_title = new_post_title
            latest_post_url = new_post_url

        # Clear the terminal
        print("\033[H\033[J", end="")
        
        if latest_post_title and latest_post_url:
            print(f"{LIGHT_BLUE}Latest post title:{RESET} {YELLOW}{latest_post_title}{RESET}")
            print(f"{GREEN}{latest_post_url}{RESET}")

        # Print the cycle and initial check interval
        print(f"Cycle: {cycle_counter} | {PURPLE}Next check in: {check_interval} seconds{RESET}", end="")

        # Countdown timer
        for remaining in range(check_interval, 0, -1):
            print(f"\rCycle: {cycle_counter} | {PURPLE}Next check in: {remaining} seconds{RESET}   ", end="")
            time.sleep(1)
        print()  # Move to the next line after countdown

        if not new_post_title and not new_post_url:
            print(f"{RED}No new post, proceeding to next check{RESET}")
            time.sleep(5)  # Wait for 5 seconds before starting the next check

if __name__ == "__main__":
    main()