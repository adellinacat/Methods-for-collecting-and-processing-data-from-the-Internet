from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from parser_goods.spiders.a5motkov_ru import A5motkovRuSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    # search = input('Enter theme')
    runner.crawl(A5motkovRuSpider, search='infinity')

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()

