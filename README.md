## Zillow Property Scraper

This Python script asynchronously scrapes property data from Zillow's search results and saves it to a CSV file.

### Features

* Fetches data from multiple Zillow search pages concurrently using asynchronous programming.
* Extracts relevant property details like address, city, state, etc. (customizable).
* Handles potential errors during web requests and data processing.

### Requirements

* Python 3.7 or later
* aiohttp library (`pip install aiohttp`)
* pandas library (for data manipulation, `pip install pandas`)

### Usage

1. Clone this repository.
2. Install required libraries (`pip install -r requirements.txt`).
3. (Optional) Modify the `fetch_data` function to extract additional desired property details from the Zillow response.
4. Run the script: `python main.py`

**Note:** This script aims for educational purposes and demonstrates asynchronous scraping techniques. Always check Zillow's terms of service before scraping data from their website.

### Output

The script saves the extracted property data to a CSV file named `zillow_extract_data.csv` in the `zillow` directory (modify filename/path as needed).

### License

MIT License
