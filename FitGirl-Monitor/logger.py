import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

# Configure logging
logger = logging.getLogger('RSSChecker')
logger.setLevel(logging.DEBUG)

# Get the directory of the current script
log_directory = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(log_directory, 'rss_checker.log.txt')

# Create a handler that writes log messages to a file, rotating the log file every day and keeping the last 5 days of logs
handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=5)
handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

def log_info(message):
    logger.info(message)

def log_debug(message):
    logger.debug(message)

def log_error(message):
    logger.error(message)