import scrapy
import csv
from scrapy.crawler import CrawlerProcess

urlss = ['https://www.eyeofriyadh.com/ar/directory/?s=&search_post_type=place&location=&category=&count=&sort-by=&sort=']


class hopa(scrapy.Spider):
    name = "hopa"

    def start_requests(self):
        urls = urlss
        for url in urls:
            yield scrapy.Request(url=url, callback=self.front_page)

    def front_page(self, response):
        dok_link = response.css('div.col-md-4>a::attr(href)').extract()
        for link in dok_link:
            yield response.follow(url=link, callback=self.next_page)

    def next_page(self,response):
        sec_links = response.css('div.col-md-3>div:nth-of-type(1)>div:nth-of-type(1)>a::attr(href)').extract()
        for link in sec_links:
            yield response.follow(url=link, callback=self.last_page)

    def last_page(self,response):
        box = response.css('div.content_left>div[style*="float:right"] ::text')
        e_mail = list(filter(lambda x: '@' in x, box.extract()))
        web = list(filter(lambda x: 'www' in x, box.extract()))
        name = response.css('div.content_left>div[style*="float:right"]>h1 ::text').extract_first()
        categ = response.css('div.content_left>div[style*="float:right"]>a ::text').extract()
        phone = response.css('div.content_left>div[style*="float:right"] li>span[dir*="ltr"] ::text').extract()


        with open(r'C:\Users\ENG.Mohamed\Desktop\New folder\dapssstsoa.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name,categ[0],categ[1],e_mail,web,phone])


process = CrawlerProcess()
process.crawl(hopa)
process.start()