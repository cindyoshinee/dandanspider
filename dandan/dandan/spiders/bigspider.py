import scrapy
from . import const
from . import mysql
import re

class Bigspider(scrapy.Spider):
    name = 'bbs'
    start_urls = ['http://www.oiegg.com/index.php']
    allowed_domains = ['oiegg.com']
    headers = const.HEADERS
    pat = r'sub_\d{2,3}_menu'
    db = mysql.MySQL(const.DB_CONFIG['host'],const.DB_CONFIG['user'],const.DB_CONFIG['password'],const.DB_CONFIG['db'],const.DB_CONFIG['port'],const.DB_CONFIG['charset'],const.DB_CONFIG['timeout'])

    def parse(self,response):
        sel = scrapy.selector.Selector(response)
        sitess = sel.xpath('//div[@class="inner_wrapper"]/ul')
        for sites in sitess:
            uid = sites.xpath('@id').extract()[0]
            try:
                if uid == re.search(self.pat,uid).group():
                    site = sites.xpath('li')
                    for eachsite in site:
                        url = eachsite.xpath('a/@href').extract()[0]
                        name = eachsite.xpath('a/text()').extract()[0]
                        url = const.URL + url
                        print(url,name)
                        self.store_data({'url':url, 'name':name})
            except AttributeError:
                pass

    def store_data(self,data):
        sql = 'insert into boards(url,name) values ("%s","%s")' % (data['url'],data['name'])
        self.db.update(sql)
