import scrapy


class BNM_Exchange_Rates_Spider(scrapy.Spider):
    name = "bnm_exchange_rates_spider"
    start_urls = ["https://www.bnm.gov.my/exchange-rates"]

    def parse(self, response):
        data = {}
        currencies = []
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
        yield data