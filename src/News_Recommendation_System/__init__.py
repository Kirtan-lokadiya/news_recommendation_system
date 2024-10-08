import os
import sys
import logging

# Define log format
logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Define log directory and file
log_dir = "logs"
log_filepath = os.path.join(log_dir, "running_logs.log")

# Create log directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath),    # Save logs to file
        logging.StreamHandler(sys.stdout)     # Print logs to terminal
    ]
)

# Correct logger name
logger = logging.getLogger('News_Recommendation_Logger')
