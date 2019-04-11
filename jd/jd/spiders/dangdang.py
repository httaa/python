# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy

class DangdangSpider(RedisSpider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    # start_urls = ['http://dangdang.com/']
    redis_key = 'dangdang'


    def parse(self, response):
        #大分类
        div_list = response.xpath("//div[@class='con flq_body']/div")
        for div in div_list:
            item = {}
            item['b_cate'] = div.xpath("./dl/dt//text()").extract()
            item['b_cate'] = [i.strip() for i in item['b_cate'] if len(i.strip())>0]
            # print(item['b_cate'])
            dl_list = div.xpath("./div//dl[@class='inner_dl']")
            for dl in dl_list:
                item['m_cate'] = dl.xpath("./dt//text()").extract()
                item["m_cate"] = [i.strip() for i in item['m_cate'] if len(i.strip())>0]
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    item["s_href"] = a.xpath("./@href").extract_first()
                    item["s_cate"] = a.xpath("./text()").extract_first()
                    if item["s_href"] is not None:
                        yield scrapy.Request(
                            item["s_href"],
                            callback = self.parse_book_list,
                            meta = {"item":deepcopy((item))}
                        )

    def parse_book_list(self,response):
        item = response.meta['item']
        li_list = response.xpath("//ul[@class='bigimg']/li")
        for li in li_list:
            item["book_img"] = li.xpath("./a[@class='pic']/img/@src").extract_first()
            if item["book_img"] =="images/model/guan/url_none.png":
                item["book_img"] = li.xpath("./a[@class='pic']/img/@data-original").extract_first()
            item["book_name"] = li.xpath("./p[@class='name']/a/@title").extract_first()
            print(item["book_name"])
        next_url = response.xpath("//li[@class='next']/a/@href").extract_first()
        if next_url is not None:
            next_url = "https://category.dangdang.com" + next_url
            yield scrapy.Request(
                next_url,
                callback = self.parse_book_list,
                meta = {"item":deepcopy(item)}
            )


