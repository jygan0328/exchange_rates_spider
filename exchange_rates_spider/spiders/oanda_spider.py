import scrapy
from scrapy.loader import ItemLoader

from datetime import datetime, timedelta

from exchange_rates_spider.items import ExchangeRateItem


class Oanda_Spider(scrapy.Spider):
    name = "oanda_spider"

    today = datetime.now()
    start_date = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    base_url = "https://web.oanda.com/cc-api/v1/currencies"
    start_urls = [
        base_url + f"?base=BRL&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=ARS&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=CLP&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=DKK&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=KPW&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=MXN&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=PEN&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=PLN&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=RUB&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=ZAR&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=TRY&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=UYU&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=DEM&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=JOD&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=KZT&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=MOP&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=UAH&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=CZK&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=BDT&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=LKR&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=IRR&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=NGN&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}",
        base_url + f"?base=UZS&quote=MYR&data_type=general_currency_pair&start_date={start_date}&end_date={end_date}"
    ]
    
    def parse(self, response):
        '''
        Example JSON response
        {'response': [{'base_currency': 'UZS', 'quote_currency': 'MYR', 'start_time': '2022-01-15T00:00:00+00:00', 'open_time': '2022-01-15T00:00:00+00:00', 'close_time': '2022-01-15T23:59:59+00:00', 'average_bid': '0.000383598', 'average_ask': '0.000386357', 'average_midpoint': '0.000384978', 'low_ask': '0.000386357', 'high_ask': '0.000386357', 'low_bid': '0.000383598', 'high_bid': '0.000383598'}]}
        '''
        data = response.json()['response'][0]
        loader = ItemLoader(item=ExchangeRateItem())
        loader.add_value('date_now', self.today.strftime("%d %b %Y"))
        loader.add_value('currency', data['base_currency'])
        loader.add_value('valuetoMYR', data['average_bid'])
        yield loader.load_item()