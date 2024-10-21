FitGirl Monitor Tool

What is it?
Simply put, it's a notification tool to alert a person when a repack has been made available.

Why did you make it?
RSS Readers are everywhere but I don't need a feature rich reader to collect all posts from a feed. I just need a tool that will alert me when the latest repack is available 
so that if I am busy with something else, my tool will grab my attention. I added the Discord function just because I don't want to always have to TAB between screens and 
since Discord is available on mobile and I have my mobile always around me, it made sense to use my phone as another prompt tool.

How does it monitor the site?
I make use of the RSS feed provided by FitGirl on the website and just monitor the feed every 60 seconds for new posts.
It displays results in the terminal until such time the user exits the script.
If you so desire, you can also have the script send a notification via a Discord webhook to your personal Discord server which then gives you an audible alert notification.
There is a nifty little cycle counter to let you know how many checks you have made during the active session.

How do I edit the interval for checking the feed?
Open RSS_Checker.py in your favourite editor and find the line: check_interval = 60
Change the number to anything you desire, just remember that it's in seconds so 5 minutes would be 300.

How do I use the Discord notification feature?
Open discord_notifier.py in your favourite editor and look for: WEBHOOK_URL = "",
Insert your webhook url between the quotes and you are good to go.

How do I run the tool?
When you download the tool, just open a terminal, navigate to where you stored the scripts and run RSS_Checker.py

How do I close the tool?
On Windows, use CTRL & C to interupt a running script, once interupted, you can close the terminal.

What has this tool been tested on?
Windows 11
