# News Websites Scraper

This repository contains a Python script that uses the Scrapy framework to scrape news headlines,Description, timestamps, and related images from different News websites.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/hardikk65/News_Scraper.git

2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Navigate to the project directory:

```bash
cd newsscraper
```

2. Run the Scrapy spider:

```bash
scrapy crawl newsspider -O scraped_data.json
```

This will start the scraping process and save the data to an `scraped_data.json` file.

## Output

The scraper will generate a JSON file (`scraped_data.json`) with the following structure:

```json
[
  {
    "Title": "Sample Headline",
    "Description": "Sample Description",
    "timestamp": "Day Month Date, Year",
    "Source_link": "https://example.com/category/",
    "image_link": "https://example.com/image.jpg",
  }
]
```
You can also generate a CSV file (`scraped_data.csv`) with a similar structure.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. Make sure to follow the [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
