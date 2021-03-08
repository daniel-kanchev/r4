import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from r4.items import Article


class R4Spider(scrapy.Spider):
    name = 'r4'
    allowed_domains = ['r4.com']
    start_urls = [ 'https://www.r4.com/analisis-actualidad/noticias-de-interes',
                  'https://www.r4.com/analisis-actualidad/area-prensa/notas-prensa-r4']

    def parse(self, response):
        links = response.xpath('//a[@class="title"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="articulo__date"]/span/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="articulo__content articulo__content__superior"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
