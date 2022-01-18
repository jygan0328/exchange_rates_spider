# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from datetime import datetime
from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst

def convert_date(text):
    # convert string 18 Jan 2022 to Python date
    return datetime.strptime(text, "%d %b %Y").date()

class ExchangeRateItem(Item):
    date_now = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    currency = Field(
        output_processor=TakeFirst()
    )
    valuetoMYR = Field(
        output_processor=TakeFirst()
    )
