import scrapy
from . import const
from . import mysql


class Myspider(scrapy.Spider):

    name = 'bbs2'
    
    def parse(self,response):
        if 'fid' in response.url:
            return self.parse_board(response)
        elif 'tid' in response.url:
            return self.parse_article(response)
        else:
            print('跳过该网页')

    def parse_board(self,response):
        print('该网页是个版面%s' % response.url)
        
        sel = scrapy.selector.Selector(response)
        sites = sel.xpath('//tbody')
        
        for site in sites:
            try:
                url = site.xpath('tr/th/span[@id]/a[last()]/@href').extract()[0]
                title = site.xpath('tr/th/span[@id]/a[last()]/text()').extract()[0].encode('gbk','ignore').decode('gbk','ignore')
                author = site.xpath('tr/td[@class="author"]/cite/a/text()').extract()[0].encode('gbk','ignore').decode('gbk','ignore')
                time = site.xpath('tr/td[@class="author"]/em/text()').extract()[0]
                reply = site.xpath('tr/td[@class="nums"]/strong/text()').extract()[0]
                next_url = const.URL + url
                print(title,url,author,time,reply)
                self.store_data({'title':title, 'url':url, 'author':author, 'time':time, 'reply':reply, 'table':'list'})
                yield scrapy.Request(next_url, headers=const.HEADERS,meta={'cookiejar':response.meta['cookiejar']}, callback=self.parse)
            except:
                pass
        try:
            next_url = sel.xpath('//div[@class="pages"]/a[@class="next"]/@href').extract()[0]
            next_url = const.URL + next_url
            yield scrapy.Request(next_url, headers=const.HEADERS,meta={'cookiejar':response.meta['cookiejar']}, callback=self.parse)
        except:
            pass
        
    def parse_article(self,response):
        url = response.url
        print('该网页%s是个文章' % url)
        response = response.replace(body=response.text.encode('gbk','ignore').decode('gbk','ignore'))
        with open ('text.txt','w') as f:
            f.write(response.text)
        sel = scrapy.selector.Selector(response)
        sites = sel.xpath('//div[@class="mainbox viewthread"]/table/tr[1]')
        texts = []
        for site in sites:
            try:
                text = site.xpath('td[@class="postcontent"]/div[@class="postmessage defaultpost"]/div[@id]/text()').extract()[0]
                author = site.xpath('td[@class="postauthor"]/cite/a/text()').extract()[0]
                time = site.xpath('td[@class="postcontent"]/div[@class="postinfo"]/text()').extract()[4].strip()
                text = author+time+text
                if text == '':
                    text = '无权访问当前界面'
                texts.append(text)
            except:
                pass
        print(texts)
        self.store_data({'url':url, 'text':texts, 'table':'article'})
        try:
            next_url = sel.xpath('//div[@class="pages"]/a[@class="next"]/@href').extract()[0]
            next_url = const.URL + next_url
            yield scrapy.Request(next_url, headers=const.HEADERS, meta={'cookiejar':response.meta['cookiejar']},callback=self.parse)
        except:
            pass 
        
    def store_data(self,data):
        if data['table']=='article':
            sql = 'insert into article(url,text) values("%s","%s")' % (data['url'],data['text'])
        else:
            sql = 'insert into list(title,url,author,time,reply) values("%s","%s","%s","%s","%s")' % (data['title'],data['url'],data['author'],data['time'],data['reply'])
        self.db.update(sql)
    
    def start_requests(self):
        self.db = mysql.MySQL(const.DB_CONFIG['host'],const.DB_CONFIG['user'],const.DB_CONFIG['password'],const.DB_CONFIG['db'],const.DB_CONFIG['port'],const.DB_CONFIG['charset'],const.DB_CONFIG['timeout'])
        return [scrapy.FormRequest("http://www.oiegg.com/logging.php?action=login&",\
                formdata = const.FORM_DATA, meta={'cookiejar':True}, headers=const.HEADERS,\
                callback = self.logged_in)]
    def logged_in(self,response):
        self.start_urls = self.load_start_urls()
        for url in self.start_urls:
            yield scrapy.Request(url, meta={'cookiejar':response.meta['cookiejar']}, headers=const.HEADERS, callback=self.parse)
    def load_start_urls(self):
        sql = 'select url from boards'
        urls = self.db.query(sql)
        self.start_urls = []
        for url in urls:
            yield url[0]
