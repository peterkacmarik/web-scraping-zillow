import traceback    # Importing the traceback module
import pandas as pd  # Importing the pandas library and aliasing it as pd
import logging  # Importing the logging module for logging purposes
import aiohttp  # Importing the aiohttp library for asynchronous HTTP requests
import asyncio  # Importing the asyncio library for asynchronous programming
import time  # Importing the time library for timing the operation
from fetch_page import fetch_page
from fetch_data import fetch_data


# Configure logging to provide detailed information about the scraping process
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

async def main():
    """
    This function is the main coroutine of the program.
    It uses asyncio to fetch pages and their associated data
    using the functions from fetch_page and fetch_data modules.

    It creates a queue to store the fetched pages and their details
    and starts fetching pages and their details concurrently
    until it reaches the last page.

    It then creates a pandas DataFrame out of the fetched details
    and saves it to a CSV file.
    """

    async with aiohttp.ClientSession() as session:
        queue = asyncio.Queue()  # Initialize the queue
        url = "https://www.zillow.com/async-create-search-page-state"
        current_page = 1  # Start from page 1
        request_id = 3  # Start from request ID 3
        detail_data = []  # Initialize an empty list to store the fetched details

        start_time = time.time()  # Start the timer

        # Start fetching pages and their details concurrently
        while True:
            try:
                fetched_page = await fetch_page(session, url, current_page, request_id, queue)  # Fetch the page
            except Exception as e:
                logging.error(f"Error fetching page {current_page}: {e}")
                break
            
            # Add the fetched page and its details to the queue
            if fetched_page:
                task = asyncio.create_task(fetch_data(current_page, queue))  # Create a task to fetch the details
                detail_data.extend(await task)  # Add the fetched details to the list
                current_page += 1  # Increment the page number
                request_id += 1  # Increment the request ID
                await queue.join()  # Wait for all tasks to complete
                await task  # Wait for the task to complete
            else:
                logging.warning('End scraping !')
                break

        end_time = time.time()  # Stop the timer
        logging.info(f"This operation took: {end_time - start_time} seconds")
        print(f"Number of details fetched: {len(detail_data)}")

        try:
            # Create a pandas DataFrame and save it to a CSV file
            df = pd.DataFrame(detail_data)
            # df.to_csv('zillow/zillow_extract_data.csv', index=False, encoding='utf-8-sig')
            print(df)  # Uncomment to print the DataFrame
        except Exception as e:
            # Handle any errors that occur during the DataFrame creation
            logging.error(f"Error creating DataFrame: {e}")
            logging.error(traceback.format_exc())

# Run the main coroutine        
if __name__ == "__main__":
    asyncio.run(main())