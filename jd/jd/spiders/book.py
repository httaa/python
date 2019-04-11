# -*- coding: utf-8 -*-
import scrapy
# from jd.items import JdItem
from copy import deepcopy

class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['jd.com']
    start_urls = ['http://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='mc']/dl/dt")
        for dt in dt_list:
            item = {}
            item['b_cate'] = dt.xpath("./a/text()").extract_first()
            em_list = dt.xpath("./following-sibling::dd[1]/em")
            for em in em_list:
                item['s_cate'] = em.xpath("./a/text()").extract_first()
                item['s_href'] = em.xpath("./a/@href").extract_first()
                if item['s_href'] is not None:
                    item['s_href'] = "https:" + item['s_href']
                    yield scrapy.Request(
                        item["s_href"],
                        callback = self.parse_detail,
                        meta = {'item':deepcopy(item)}
                    )


    def parse_detail(self,response):
        item = response.meta['item']
        li_list = response.xpath("//div[@id='plist']/ul/li")
        for li in li_list:
            item['book_img'] = li.xpath(".//div[@class='p-img']//img/@src").extract_first()
            if item['book_img'] is not None:
                item['book_img'] = "https:" + item['book_img']
            item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extrat_first()
            item['book_author'] = li.xpath(".//span[class='auth_type_1']/a/text()").extrat_first()

        next_url = response.xpath("//a[@class='pn-next']/@href").extrat_first()
        if next_url is not None:
            next_url = 'http://list.jd.com' + next_url
            yield scrapy.Request(
                next_url,
                callback = self.parse_detail,
                meta = {'item':deepcopy(item)}
            )



