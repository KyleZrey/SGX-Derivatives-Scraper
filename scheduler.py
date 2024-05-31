import schedule
import time
import subprocess
from datetime import datetime
import argparse

def run_scraper():
    subprocess.run(["python", "scraper.py", "--latest"])

def job():
    # Check if today is Tuesday to Saturday
    if datetime.today().weekday() in {1, 2, 3, 4, 5}:
        run_scraper()

def main(scheduled_time):
    # Schedule the job to run at the specified time
    schedule.every().day.at(scheduled_time).do(job)

    # Run the scheduler
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Scheduler stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Schedule scraper.py to run at a specific time.')
    parser.add_argument('--time', type=str, required=True, 
                        help='Time to run scraper.py in HH:MM format')
    args = parser.parse_args()

    main(args.time)
