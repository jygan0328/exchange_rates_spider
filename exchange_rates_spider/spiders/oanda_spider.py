import scrapy
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from time import sleep
from datetime import datetime

from exchange_rates_spider.items import ExchangeRateItem


class Oanda_Spider(scrapy.Spider):
    name = "oanda_spider"
    start_urls = ["https://www1.oanda.com/currency/converter/"]

    def parse(self, response):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920x1080")
        # chrome_options.add_argument("--headless")

        chrome_driver_path = get_project_settings().get("CHROME_DRIVER")
        driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
        driver.get("https://www.bnm.gov.my/exchange-rates")

        today = datetime.now()
        selected_month = today.month - 1
        selected_year = today.year
        sleep(10)
        #from
        select_from_month = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_monthStart'))
        select_from_month.select_by_value(str(selected_month))
        select_from_year = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_yearStart'))
        select_from_year.select_by_value(str(selected_year))
        #to
        select_from_month = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_monthEnd'))
        select_from_month.select_by_value(str(selected_month))
        select_from_year = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_yearEnd'))
        select_from_year.select_by_value(str(selected_year))
        #session
        select_session = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_sessionTime'))
        select_session.select_by_value("1200")
        #rate type
        select_type = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_rateType'))
        select_type.select_by_value("MR")
        #quotation
        select_quotation = Select(driver.find_element_by_id('_bnm_exchange_rate_display_portlet_quotation'))
        select_quotation.select_by_value("rm")

        #search
        driver.find_element_by_id("_bnm_exchange_rate_display_portlet_btnSearch").click()
        sleep(5)

        scrapy_selector = Selector(text=driver.page_source)
        
        data = {}
        currencies = []

        for row in scrapy_selector.css("table#dvData2 > tbody > tr"):
            if row.css("th"):
                currencies = row.css("th > b::text").getall()
            else:
                row_data = row.css("td::text").getall()
                if len(row_data) < 10:
                    continue

                for i, c in enumerate(currencies, start=1):
                    if data.get(row_data[0]):
                        data[row_data[0]][c] = row_data[i]
                    else:
                        data[row_data[0]] = {
                            c: row_data[i]
                        }

        for date_now, xrates in data.items():
            for curr, val in xrates.items():
                loader = ItemLoader(item=ExchangeRateItem())
                loader.add_value('date_now', date_now)
                loader.add_value('currency', curr)
                loader.add_value('valuetoMYR', val)
                yield loader.load_item()
        
        driver.quit()