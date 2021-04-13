import scrapy

from scrapy.loader import ItemLoader

from ..items import EalbankItem
from itemloaders.processors import TakeFirst


class EalbankSpider(scrapy.Spider):
	name = 'ealbank'
	start_urls = ['https://www.eal-bank.com/news']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "cards", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "col-md-4", " " ))]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mx-auto", " " ))]//text()[normalize-space() and not(ancestor::h2 | ancestor::small)]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "mx-auto", " " ))]//small/text()').get()

		item = ItemLoader(item=EalbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
