from logger import setup_logger
import argparse
from datetime import datetime, timedelta

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
            today = datetime.today()
            # Tuesday to Saturday
            if 0 < today.weekday() < 6:
                dates = [today.strftime("%Y-%m-%d")]
            else:
                # Calculate last Saturday
                last_saturday = today - timedelta(days=(today.weekday() + 2) % 7)
                dates = [last_saturday.strftime("%Y-%m-%d")]
            logger.info("Latest dates processed successfully.")

        elif args.date_range:
            logger.info("Processing date range option...")
            try:
                start_date, end_date = args.date_range
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                # Generate a list of dates between start and end that are tuesday-saturday
                dates = [
                (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range((end_date - start_date).days + 1)
                if (start_date + timedelta(days=i)).weekday() in {1, 2, 3, 4, 5}
                ]
            except (ValueError, TypeError) as e:
                logger.error(f"Invalid start or end date range: {e}")
                return
            logger.info("Date range processed successfully.")

        else:
            logger.info("Processing specific date/s option...")
            try:
                dates = [datetime.strptime(date_str, '%Y-%m-%d').strftime("%Y-%m-%d") for date_str in args.date]
                
                # Filter out Sundays and Mondays
                valid_dates = []
                for date in dates:
                    try:
                        if datetime.strptime(date, '%Y-%m-%d').weekday() in {1, 2, 3, 4, 5}:
                            valid_dates.append(date)
                    except ValueError:
                        pass
                
                if not valid_dates:
                    logger.error("Invalid dates: Dates must be Tuesday through Saturday.")
                    return
                
                dates = valid_dates
            except ValueError as e:
                logger.error(f"Invalid date/s format: {e}")
                return
            logger.info("Specific dates processed successfully.")

        # Setup url and path variables
        url = "https://links.sgx.com/1.0.0/derivatives-historical/{date}/{file}"
        download_path = 'downloads'
        



    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    logger = setup_logger()
    main()


