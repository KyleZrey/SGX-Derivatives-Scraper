import logging
import os

log_dir = 'logs'

def setup_logger(file_name):

     # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Define the log file path
    log_file = os.path.join(log_dir, file_name)
                
    # Create logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def setup_logger_file(file_name):
    
    # Create log directory if it doesn't exist
    os.makedirs(log_dir, exist_ok=True)
    
    # Define the log file path
    log_file = os.path.join(log_dir, file_name)
    
    # Create logger
    logger = logging.getLogger(file_name)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(log_file)

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)

    return logger
