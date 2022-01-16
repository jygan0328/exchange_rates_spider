# Exchange Rate Spider

## Disclaimer
**Please perform web scraping responsibly without causing harms to the website.**

## Project Description
This is a bot/spider that collect the exchange rate of foreign currencies to Malaysia Ringgit (MYR) using **Python Scrapy framework**. This project is a revamp of the same exchange rate spider program that I have done in my job back in 2020 using **Selenium**. By using Scrapy, it becomes more lightweight and efficient to collect data. 

The data source is from the below websites/API:
* [Bank Negara Malaysia website](https://www.bnm.gov.my/exchange-rates)
* [OANDA](https://web.oanda.com/cc-api/v1/currencies) 


## Requirement
`$ pip install Scrapy`

## How to Install and Run the Project
1. Git clone this project.
`git clone https://github.com/jygan0328/exchange_rates_spider.git`
2. Create a virtual environment (conda/venv) and install package in `requirements.txt`.
3. Run the command in the project directory.
`python crawl.py`
4. The data collected are stored in `sqlite3` database in project directory. You may change to use any other DBMS by changing `CONNECTION_STRING` in settings file.