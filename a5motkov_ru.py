import scrapy
from scrapy.http import HtmlResponse
from parser_googs.items import ParserGoogsItem
from scrapy.loader import ItemLoader


class A5motkovRuSpider(scrapy.Spider):
    name = '5motkov_ru'
    allowed_domains = ['5motkov.ru']
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://5motkov.ru/site/search/?q={kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//td[@class='views-field views-field-field-composition']/div[@class='name']/a")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)
        
             
    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=A5motkovRuSpider(), response=response)
        loader.add_xpath('name', "//div[@class='name']/a/text()")
        loader.add_xpath('price', "//div[@class='field-content ']/text()")
        loader.add_xpath('photos', "//td[@class='views-field']/a/img/@src")
        loader.add_value('url', response.url)
        yield loader.load_item()
    
    #print()

        





