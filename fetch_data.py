import logging  # Importing the logging module for logging purposes
import asyncio  # Importing the asyncio library for asynchronous programming


# Configure logging to provide detailed information about the scraping process
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

async def fetch_data(current_page, queue):
    """
    Asynchronously fetches data from a queue and returns a list of dictionaries containing the extracted data.
    
    Args:
        current_page (int): The current page number being scraped.
        queue (asyncio.Queue): The queue containing the data to be fetched.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents the extracted data from a single item in the queue.
              Each dictionary contains the following keys:
                  - 'id' (str): The ID of the item.
                  - 'address' (str): The address of the item.
                  - 'addressCity' (str): The city of the item's address.
                  - 'addressState' (str): The state of the item's address.
                  - 'addressStreet' (str): The street of the item's address.
                  - 'addressZipcode' (str): The zipcode of the item's address.
                  - Additional keys can be added as needed.
    
    Raises:
        asyncio.QueueEmpty: If the queue is empty when trying to get items.
        Exception: If an unexpected error occurs while fetching data.
    """
    list_fetched_data = []  # Initialize an empty list to store the fetched data
    try:
        # Loop until the queue is empty
        if not queue.empty():
            for item in await queue.get():
                try:
                    list_detail_data = {
                        'id': item.get('id'),
                        'address': item.get('address'),
                        'addressCity': item.get('addressCity'),
                        'addressState': item.get('addressState'),
                        'addressStreet': item.get('addressStreet'),
                        'addressZipcode': item.get('addressZipcode'),
                        # add more properties as needed...
                    }
                    list_fetched_data.append(list_detail_data)  # Add the fetched data to the list
                except TypeError as e:
                    logging.error(f"Error processing item data: {e}")
                    # Handle the error or continue to the next item
                    continue    # Continue to the next item
            queue.task_done()    # Mark the task as done
            logging.info(f"Page {current_page} successfully extracted data")
        else:
            logging.warning('End scraping !')
    except asyncio.QueueEmpty:
        logging.warning('Queue was empty when trying to get items.')
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching data: {e}")
    return list_fetched_data    # Return the list of fetched data
