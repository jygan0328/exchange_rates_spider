# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from exchange_rates_spider.models import ExchangeRate, db_connect, create_table


class SaveExchangeRatePipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)


    def process_item(self, item, spider):
        """
        Save exchange rate in the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        exchange_rate = ExchangeRate()
        exchange_rate.date_now = item["date_now"]
        exchange_rate.currency = item["currency"]
        exchange_rate.valuetoMYR = item["valuetoMYR"]

        try:
            session.add(exchange_rate)
            session.commit()

        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item


class DuplicatesPipeline(object):

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates tables.
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        '''
        Skip duplicated exchange rate based on date and currency
        '''
        session = self.Session()
        exist_exchange_rate = session.query(ExchangeRate).filter_by(
            date_now = item["date_now"],
            currency = item["currency"]
        ).first()
        session.close()
        if exist_exchange_rate is not None:
            #the currency exists
            raise DropItem("Duplicate item found: %s" % item["currency"])
        else:
            return item