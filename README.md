# Car Auction Data

**Note:** This project was developed and tested on Ubuntu. Compatibility with Windows has not been verified.

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/car-auction-scraper.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd car-auction-scraper
    ```

3. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

5. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the scraper, follow these steps:

1. **Navigate to the project directory:**
    ```bash
    cd auction/auction
    ```

2. **Run the command:**
    ```bash
    scrapy crawl car_auction
    ```

This will initiate the spider, allowing it to visit the specified URLs and extract car auction data. The gathered information will be stored in a CSV file named `BringATrailer_CarAuctionData_{current_date}.csv` in the `data` directory. Additionally, images will be downloaded and saved in the `data/Pictures` directory, with filenames based on the lot numbers.

## Important Note

Make sure to have Scrapy installed and activate the virtual environment before running the script.

```bash
pip install scrapy
