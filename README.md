## Steam Games Scraper

This project is designed to scrape game information from the Steam store using web scraping techniques. The scraper works in two stages, utilizing two Scrapy spiders to efficiently collect data:

- `Steam ID Spider`: This spider extracts the Steam IDs of games from the Steam store's search page. These IDs serve as unique identifiers for each game.
    
- `Steam Spider`: Using the collected Steam IDs, this spider retrieves detailed information about each game, such as its title, description, and other metadata.

The scraped data can be saved in various formats (e.g., JSON) for further analysis or integration into other projects.
Tools and Technologies

The project leverages the following tools and libraries:

- `Python`: The programming language used to write the scraper.
- `Scrapy`: A powerful web crawling and scraping framework, used to build and run the spiders.
    
### How It Works
#### Workflow

  - `Steam ID Spider`:
        Starts by navigating to the Steam search page.
        Collects game IDs (steam_appid) and their corresponding titles.
        Supports infinite scroll to load additional games dynamically, if required.

  - `Steam Spider`:
      Takes the game IDs from the first spider as input.
      Fetches detailed game information by visiting each game's detail page.

#### Output

The results are stored in a CSV file (steam.csv), with each line containing the game's ID and relevant details.

### Usage

#### Prerequisites

 - Install Python 3.9+ and set up a virtual environment.
 - Install the required libraries:
    `pip install scrapy pandas`

#### Running the Spiders

1 - Run the Steam ID Spider to collect game IDs:
    `scrapy crawl steamID_spider -O steam_id.csv`

This will generate a JSON file containing the game IDs and titles.

2 - Run the Steam Spider to fetch detailed information:
    `scrapy crawl steam_spider -O steam.csv`

This spider will read the steam_id.csv file and retrieve detailed information for each game.