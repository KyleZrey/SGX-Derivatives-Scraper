import argparse
import os
from logger import setup_logger, setup_logger_file
from datetime import datetime, timedelta
import requests

def download(dates):
    # Setup url and path variables
    url = "https://links.sgx.com/1.0.0/derivatives-historical/{index}/{file}"
    download_path = 'downloads'
    
    # If multiple dates loop around all of it
    for date in dates:
        try:
            index = date_to_index(date)
        except Exception as e:
            logger.error(f"Skipping date {date} due to error: {e}")
            downloads_logger.error(f"Skipping date {date} due to error: {e}")
            continue

        date_dir = os.path.join(download_path, date)
        if not os.path.exists(date_dir):
            os.makedirs(date_dir)
        files = [
        ("WEBPXTICK_DT.zip", f"WEBPXTICK_DT_{date.replace('-', '')}.zip"),
        ("TickData_structure.dat", "TickData_structure.dat"),
        ("TC.txt", f"TC_{date.replace('-', '')}.txt"),
        ("TC_structure.dat", "TC_structure.dat")
        ]
        for original_file, new_file_name in files:
            file_url = url.format(index=index, file=original_file)
            file_path = os.path.join(date_dir, new_file_name)
            try:
                download_file(file_url, file_path)
                logger.info(f"Downloaded {new_file_name} for date {date} to {file_path}")
                downloads_logger.info(f"Downloaded {new_file_name} for date {date} to {file_path}")
            except Exception as e:
                logger.error(f"Failed to download {new_file_name} for date {date}: {e}")
                downloads_logger.error(f"Failed to download {new_file_name} for date {date}: {e}")

def download_file(file_url, file_path):
    response = requests.get(file_url, stream=True)
    if response.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        raise Exception(f"Failed to download file: HTTP {response.status_code}")

def date_to_index(date):
    try: # Indexing is only consistent from 2021-01-01
        start_date = datetime.strptime('2021-01-01', '%Y-%m-%d')
        end_date = datetime.strptime(date, '%Y-%m-%d')
        days_difference = (end_date - start_date).days
        weekdays = sum(1 for i in range(days_difference) if (start_date + timedelta(days=i)).weekday() < 5)
        return weekdays + 4803
    except (ValueError, TypeError) as e:
        logger.error(f"Failed to calculate date index: {e}")
        raise

def main():
    #Command line arguments parser
    try:
        logger.info("Parsing command line arguments...")

        parser = argparse.ArgumentParser(description="Specify Date Range")
        # Latest files only
        parser.add_argument('--latest', action='store_true', 
                            help='''Include the latest files available. Yesterday\'s 
                            files if yesterday is a weekday, Last Friday\'s files if not.''')# Date range
        # Date range
        parser.add_argument('--date-range', required=False, nargs=2,
                            help='''Dates in the format YYYY-MM-DD. space separated, 
                            inclusive, and start-date < end-date''')
        # Specific date or a list of dates
        parser.add_argument('--date', required=False, nargs='+',
                            help='Date/s in the format YYYY-MM-DD, space separated')
        args = parser.parse_args()

        logger.info("Command line arguments parsed successfully.")

        if args.latest:
            logger.info("Processing latest dates option...")
            yesterday = datetime.today() - timedelta(days=1)
            # Monday to Friday
            if 0 < yesterday.weekday() < 5:
                dates = [yesterday.strftime("%Y-%m-%d")]
            else:
                # Calculate last Friday
                last_friday = yesterday - timedelta(days=(yesterday.weekday() + 3) % 7)
                dates = [last_friday.strftime("%Y-%m-%d")]
            logger.info("Latest dates processed successfully.")

        elif args.date_range:
            logger.info("Processing date range option...")
            try:
                start_date, end_date = args.date_range
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                # Generate a list of dates between start and end that are monday-friday
                dates = [
                (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range((end_date - start_date).days + 1)
                if (start_date + timedelta(days=i)).weekday() in {0, 1, 2, 3, 4}
                ]
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid start or end date range: {e}")
                return
            logger.info("Date range processed successfully.")

        else:
            logger.info("Processing specific date/s option...")
            try:
                dates = [datetime.strptime(date_str, '%Y-%m-%d').strftime("%Y-%m-%d") for date_str in args.date]
                
                # Filter out Saturdays and Sundays
                valid_dates = []
                for date in dates:
                    try:
                        if datetime.strptime(date, '%Y-%m-%d').weekday() in {0, 1, 2, 3, 4}:
                            valid_dates.append(date)
                    except ValueError:
                        pass
                
                if not valid_dates:
                    logger.error("Invalid dates: Dates must be Monday through Friday.")
                    return
                
                dates = valid_dates
            except ValueError as e:
                logger.error(f"Invalid date/s format: {e}")
                return
            logger.info("Specific dates processed successfully.")
        
        if any(datetime.strptime(date, '%Y-%m-%d').year < 2021 for date in dates):
            logger.info('Dates before 2021 have inconsistent indexing in the SGX Website, use with caution.')
        
        # After arguments parsing, pass dates to download function
        download(dates)




    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    logger = setup_logger("scraper.log")
    downloads_logger = setup_logger_file("downloads.log")
    main()


