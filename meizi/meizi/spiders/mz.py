# -*- coding: utf-8 -*-
import os
import urllib.request

import scrapy

from meizi.items import MeiziItem


class MzSpider(scrapy.Spider):
    name = 'mz'
    # allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/xinggan/']

    def parse(self, response):
        li_list = response.xpath('//ul[@id="pins"]//li')
        for li in li_list:
            item = MeiziItem()
            item['img_name'] = li.xpath('.//a/img/@alt').extract_first()
            img_info_url = li.xpath('.//a/@href').extract_first()
            yield scrapy.Request(url=img_info_url, callback=self.img_info, meta={'item': item})

    def img_info(self, response):
        item = response.meta['item']
        item['img_url'] = response.xpath('//div[@class="main-image"]/p/a/img/@src').extract_first()
        yield item
        yield scrapy.Request(url=item['img_url'], callback=self.download,meta={'item':item})

    def download(self,response):
        item = response.meta['item']
        # dir_path = './meizi'
        suffix = os.path.splitext(item['img_url'])[-1]
        file_name = item['img_name'] + suffix
        # file_path = os.path.join(dir_path, file_name)
        # urllib.request.urlretrieve(item['img_url'], file_path)
        with open('meizi/' + file_name,'wb') as fw:
            fw.write(response.body)
