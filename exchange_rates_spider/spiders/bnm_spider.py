import scrapy
from scrapy.loader import ItemLoader
from datetime import datetime

from exchange_rates_spider.items import ExchangeRateItem


class BNM_Exchange_Rates_Spider(scrapy.Spider):
    name = "bnm_spider"

    #selected month and year for the url parameter
    today = datetime.now()
    selected_month = today.month - 1
    selected_year = today.year

    start_urls = [
        f"https://www.bnm.gov.my/exchange-rates?p_p_id=bnm_exchange_rate_display_portlet&p_p_lifecycle=0&p_p_state=normal&p_p_mode=view&_bnm_exchange_rate_display_portlet_monthStart={selected_month}&_bnm_exchange_rate_display_portlet_yearStart={selected_year}&_bnm_exchange_rate_display_portlet_monthEnd={selected_month}&_bnm_exchange_rate_display_portlet_yearEnd={selected_year}&_bnm_exchange_rate_display_portlet_sessionTime=1200&_bnm_exchange_rate_display_portlet_rateType=MR&_bnm_exchange_rate_display_portlet_quotation=rm"
    ]

    def parse(self, response):
        data = {}
        currencies = []

        #process the html data into a dictionary
        for row in response.css("table#dvData2 > tr"):
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
        
        #convert the dictionary data into items
        for date_now, xrates in data.items():
            for curr, val in xrates.items():
                loader = ItemLoader(item=ExchangeRateItem())
                loader.add_value('date_now', date_now)
                loader.add_value('currency', curr)
                loader.add_value('valuetoMYR', val)
                yield loader.load_item()