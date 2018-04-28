import scrapy
from scrapy.http import Request
import bs4
import re

from sucie.items import  SucieItem

class chickenSpider(scrapy.Spider):
    name = "sucie"
    allowed_domains = ["www.qinbing.cn"]
    start_urls = [
        "http://www.qinbing.cn/list/jiage/19/1",
    ]
    base_url = "http://www.qinbing.cn/list/jiage/19/"
    base_hidden_url = "http://www.qinbing.cn/html/details_jiage/"



    def start_requests(self):
        for i in range(1,16):
            url = self.base_url + str(i)
            yield Request(url,self.parse)
    def parse(self, response):
        # print(response.xpath('//a[@class="cb6"]//@href'))
        # print(response.xpath('//*[@id="GridView1"]/tbody/tr/td/div[1]/a'))
        # print(response.xpath('//a[@class="cb6"]/@href').extract())
        # print("--------------------------------------------------")
        hidden= response.xpath('//a[@class="cb6"]/@href').extract()
        for each in hidden:
            # print(each)
            # print('\n')
            if each.endswith(".html"):
                new_url = self.base_hidden_url + str(str(each.split("/")[3:][0]))
                yield Request(new_url,callback=self.get_content)

        # hidden_url = ''
        # new_url = self.base_hidden_url + str(hidden_url)
        # yield Request(new_url,callback=self.get_content)


    def get_content(self,response):
        big_title = str(response.xpath("//div[@class='article0']/text()").extract()[0]).strip()
        # date = big_title[:5] # 日期
        date = re.findall('(.*?)日',big_title)[0]+'日'
        province = re.findall('日(.*?)鸡苗',big_title)[0]
        # province = big_title[5:7]#省份

        price = response.xpath("//div[@id='pastingspan1']/text()").extract()
        for p in price:
            if str(p).endswith("参考价】"):

                p_array = p.strip().split()
                if(len(p_array) > 1):

                    district = p_array[0].strip()
                    p_price = p_array[1].strip().split('-')

                    minPrice = re.findall(r"\d+\.?\d*", p_price[0])[0]
                    maxPrice = re.findall(r"\d+\.?\d*", p_price[1])[0]


                    item = SucieItem()
                    item['province'] = province
                    item['date'] = date
                    item['district'] = district
                    item['minPrice'] = minPrice
                    item['maxPrice'] = maxPrice
                    yield item

