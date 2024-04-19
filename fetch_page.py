import logging  # Importing the logging module for logging purposes
import aiohttp  # Importing the aiohttp library for asynchronous HTTP requests
import asyncio  # Importing the asyncio library for asynchronous programming
import json  # Importing the json library for JSON encoding and decoding
from aiohttp import ClientError, ClientResponseError


# Configure logging to provide detailed information about the scraping process
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

# Časové intervaly pre backoff stratégiu
BACKOFF_INTERVALS = [1, 2, 4, 8, 16]  # Sekundy

async def fetch_page(session, url, current_page, request_id, queue):
    """Fetch a page of search results from Zillow

    The function sends a GET request to the specified URL with the specified
    payload and headers, then parses the JSON response and adds the search results
    to the queue.

    Args:
    session (aiohttp.ClientSession): The aiohttp session to use for the request
    url (str): The URL to send the request to
    current_page (int): The number of the page being fetched (for logging purposes)
    request_id (str): The request ID to include in the payload
    queue (asyncio.Queue): The queue to add the search results to

    Returns:
    bool: Whether the page was fetched and added to the queue successfully
    """
    
    # Define the payload and headers for the request
    payload = json.dumps({
    "searchQueryState": {
        "isMapVisible": False,
        "mapBounds": {
        "west": -74.51938436914065,
        "east": -73.4399776308594,
        "south": 40.405685665239744,
        "north": 40.988741695224775
        },
        "regionSelection": [
        {
            "regionId": 6181,
            "regionType": 6
        }
        ],
        "filterState": {
        "sortSelection": {
            "value": "globalrelevanceex"
        },
        "isAllHomes": {
            "value": True
        }
        },
        "isListVisible": True,
        "pagination": {
        "currentPage": current_page
        }
    },
    "wants": {
        "cat1": [
        "listResults"
        ],
        "cat2": [
        "total"
        ]
    },
    "requestId": request_id,
    "isDebugRequest": False
    })
    # Define the headers for the request
    headers = {
    'accept': '*/*',
    'accept-language': 'sk-SK,sk;q=0.9,cs;q=0.8,en-US;q=0.7,en;q=0.6',
    'content-type': 'application/json',
    'cookie': 'zguid=24|%24b6e54c0c-29ea-476a-b23f-5565aa2d7a39; zgsession=1|758d1123-b2d8-4d3b-b486-7fdc21918702; JSESSIONID=1BCB0406EF04C8820958DDAC3C12AA5B; pxcts=7bd746f0-fdb8-11ee-b815-b06feef0b1a5; _pxvid=7bd72c1b-fdb8-11ee-b815-1d15ec4a4283; AWSALB=Ajzme9BBaRQkR2wLe98DmuWms0Yq1McIvukWp0kChSYwu+Qm6g9AOrB8F5oMVDUH4Q+MG+BxN53FwyoR13RepVYEqKMoTzYCGH3xDs3RZl2AE8AX3t6VF6lzyXiv; AWSALBCORS=Ajzme9BBaRQkR2wLe98DmuWms0Yq1McIvukWp0kChSYwu+Qm6g9AOrB8F5oMVDUH4Q+MG+BxN53FwyoR13RepVYEqKMoTzYCGH3xDs3RZl2AE8AX3t6VF6lzyXiv; _px3=92605c59f852c8af5bfd25868bccf8c95fff83904a8d6c1f2d4284511c88c572:357Zb68320zt6VUaccF0gKIqcRDlkIJ5FZzd4OF/5yosPsJsMT0IyK9n6GPeGAsdr7o7xxpMuHhzy2u+Sy3D0g==:1000:2KDz5nrDjTcqTyat+/gLQL/3MejclfgdvnwIRXBSIqA4SUGkrX1pKGBHs1GmUEEKI65laRpHSxN7gtd7XbiTfEgZxz1KoDYz7G8SvmfR2SDGfeDJmAKV0SLlrtI53dDG041vo2ycbNllSid+jTaumGwmn7FOQy+637an/rBAQ78QY+QJQYIOx5ZQ4kvcKwqKD+Zfz+XoauAin7ug1I0gQxiOgig8uSwC2a96WYjcOZo=; search=6|1716060099954%7Crect%3D40.917577%2C-73.700272%2C40.477399%2C-74.25909%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26student-housing%3D0%26income-restricted-housing%3D0%26military-housing%3D0%26disabled-housing%3D0%26senior-housing%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%096181%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; search=6|1716060357185%7Crect%3D40.917577%2C-73.700272%2C40.477399%2C-74.25909%26rid%3D6181%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26student-housing%3D0%26income-restricted-housing%3D0%26military-housing%3D0%26disabled-housing%3D0%26senior-housing%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%096181%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09',
    'origin': 'https://www.zillow.com',
    'priority': 'u=1, i',
    'referer': 'https://www.zillow.com/new-york-ny/2_p/?searchQueryState=%7B%22pagination%22%3A%7B%22currentPage%22%3A2%7D%2C%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22west%22%3A-74.25909%2C%22east%22%3A-73.700272%2C%22south%22%3A40.477399%2C%22north%22%3A40.917577%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A6181%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        # Send a GET request to the specified URL and return the response
        async with session.put(url, headers=headers, data=payload) as response:
            if response.status == 200:  # Check if the response status is 200
                try:
                    json_data = await response.json()  # Decode the response as JSON
                except aiohttp.ContentTypeError:
                    logging.error(f"Invalid content type received from page {current_page}")
                    return False
                except ValueError:
                    logging.error(f"JSON decoding failed for page {current_page}")
                    return False
                # Extract the search results from the JSON data
                start_point = json_data.get('cat1', {}).get('searchResults', {}).get('listResults')
                # Add the search results to the queue
                if start_point:
                    await queue.put(start_point)
                    logging.info(f"Page {current_page} successfully add to queue")
                    return True
                else:
                    logging.error(f"No data found in page {current_page}")
                    return False
            else:
                logging.error(f"Error fetching page {current_page}: {response.status}")
                return False
    except ClientResponseError as e:
        logging.error(f"Client response error for page {current_page}: {e}")
        return False
    except ClientError as e:
        logging.error(f"Client error for page {current_page}: {e}")
        return False
    except asyncio.TimeoutError:
        logging.error(f"Timeout error fetching page {current_page}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return False
