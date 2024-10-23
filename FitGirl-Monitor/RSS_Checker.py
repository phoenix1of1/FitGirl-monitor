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
RESET = '\033[0m'

# Path to the sound file
SOUND_FILE_PATH = r"path\to\file\level-up-191997.mp3"

# Function to play sound alert
def play_sound_alert():
    if os.path.exists(SOUND_FILE_PATH):
        winsound.PlaySound(SOUND_FILE_PATH, winsound.SND_FILENAME)
    else:
        logger.log_warning(f"Sound file not found: {SOUND_FILE_PATH}")

# Function to fetch and parse the RSS feed
def fetch_feed():
    return feedparser.parse(RSS_FEED_URL)

# Function to check for new posts
def check_for_new_posts(latest_post_id):
    feed = fetch_feed()
    if (feed.entries):
        latest_entry = feed.entries[0]
        second_latest_entry = feed.entries[1] if len(feed.entries) > 1 else None
        
        # Discard posts without a title or with specific titles
        if (not latest_entry.title or 
            latest_entry.title == "Upcoming Repacks" or 
            latest_entry.title == "A Call for Donations" or 
            latest_entry.title.startswith("Updates Digest for")):
            return latest_post_id, False, None
        
        # Extract the article ID from the entry link
        latest_entry_id = latest_entry.link.split('/')[-2]
        
        if latest_entry_id != latest_post_id:
            print(f"New post detected: {latest_entry.title}")
            print(f"Second latest post: {second_latest_entry.title if second_latest_entry else 'None'}")
            logger.log_info(f"New post detected: {latest_entry.title}")
            logger.log_info(f"Second latest post: {second_latest_entry.title if second_latest_entry else 'None'}")
            
            # Send notification to Discord
            send_discord_notification(f"New post detected: {latest_entry.title}")
            send_discord_notification(f"Second latest post: {second_latest_entry.title if second_latest_entry else 'None'}")
            
            # Play sound alert
            play_sound_alert()
            
            return latest_entry_id, True, latest_entry.title
        else:
            return latest_post_id, False, latest_entry.title
    return latest_post_id, False, None

def main():
    # Initialize the latest post title with the title of the latest valid post from the RSS feed
    feed = fetch_feed()
    latest_post_title = "No posts yet"
    latest_post_id = None
    
    for entry in feed.entries:
        if (entry.title and 
            entry.title != "Upcoming Repacks" and 
            entry.title != "A Call for Donations" and 
            not entry.title.startswith("Updates Digest for")):
            latest_post_title = entry.title
            latest_post_id = entry.link.split('/')[-2]
            break

    check_interval = 60  # Interval in seconds
    cycle_counter = 0

    while True:
        cycle_counter += 1
        latest_post_id, new_posts_found, new_latest_post_title = check_for_new_posts(latest_post_id)
        
        # Update the latest post title if a new post is found
        if new_latest_post_title:
            latest_post_title = new_latest_post_title
        
        # Clear the terminal
        print("\033[H\033[J", end="")
        
        # Print the latest post title in light blue and the title itself in yellow
        print(f"{LIGHT_BLUE}Latest post title: {YELLOW}{latest_post_title}{RESET}")
        
        # Countdown timer in purple with padding to clear previous output
        for remaining in range(check_interval, 0, -1):
            print(f"\rCycle: {cycle_counter} | {PURPLE}Next check in: {remaining} seconds{RESET}    ", end="", flush=True)
            time.sleep(1)
        print()  # Move to the next line after countdown
        
        if new_posts_found:
            print("New posts were found.")
            # Play sound alert when new posts are found
            play_sound_alert()
        else:
            print("No new posts found.")
        
        if not new_posts_found:
            print(f"The cached latest post is still the latest post available: {latest_post_title}")
        
        print("Starting check for new posts...")  # Message indicating a new check
        
        # 15-second countdown timer
        for remaining in range(15, 0, -1):
            print(f"\r{PURPLE}Next check starts in: {remaining} seconds{RESET}    ", end="", flush=True)
            time.sleep(1)
        print()  # Move to the next line after countdown

if __name__ == "__main__":
    main()