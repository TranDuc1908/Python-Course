import scrapy
import json

class QuotesSpider(scrapy.Spider):
    # name = "quotes"

    # # def start_requests(self):
    #     # urls = [
    #     #     'https://vnexpress.net/thoi-su',
    #     #     'https://vnexpress.net/thoi-su-p2',
    #     # ]
    #     # for url in urls:
    #     #     yield scrapy.Request(url=url, callback=self.parse)
    # start_urls = [
    #     'http://quotes.toscrape.com/page/1/',
    #     'http://quotes.toscrape.com/page/2/',
    # ]

    # # def parse(self, response):
    # #     page = response.url.split("/")[-2]
    # #     filename = 'quotes-%s.html' % page
    # #     with open(filename, 'wb') as f:
    # #         f.write(response.body)
    # #     self.log('Saved file %s' % filename)

    # # def parse(self, response):
    # #     page = response.url.split("/")[-2]
    # #     filename = 'quotes-%s.html' % page
    # #     with open(filename, 'wb') as f:
    # #         f.write(response.body)
        
    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').extract_first(),
    #             'author': quote.css('small.author::text').extract_first(),
    #             'tags': quote.css('div.tags a.tag::text').extract(),
    #         }

    #     next_page = response.css('li.next a::attr(href)').extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, callback=self.parse)

    # =======================================================================

    # name = 'author'

    # start_urls = ['http://quotes.toscrape.com/']

    # def parse(self, response):
    #     # follow links to author pages
    #     for href in response.css('.author + a::attr(href)'):
    #         yield response.follow(href, self.parse_author)

    #     # follow pagination links
    #     for href in response.css('li.next a::attr(href)'):
    #         yield response.follow(href, self.parse)

    # def parse_author(self, response):
    #     def extract_with_css(query):
    #         return response.css(query).extract_first().strip()

    #     yield {
    #         'name': extract_with_css('h3.author-title::text'),
    #         'birthdate': extract_with_css('.author-born-date::text'),
    #         'bio': extract_with_css('.author-description::text'),
    #     }

    # =======================================================================

    # name = "quotes"

    # def start_requests(self):
    #     url = 'http://quotes.toscrape.com/'
    #     tag = getattr(self, 'tag', None)
    #     if tag is not None:
    #         url = url + 'tag/' + tag
    #     yield scrapy.Request(url, self.parse)

    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').extract_first(),
    #             'author': quote.css('small.author::text').extract_first(),
    #         }

    #     next_page = response.css('li.next a::attr(href)').extract_first()
    #     if next_page is not None:
    #         yield response.follow(next_page, self.parse)


    # =======================================================================

    name = 'crawlVNE'

    start_urls = ['https://vnexpress.net/thoi-su']

    def parse(self, response):
        tmp = response.xpath('//h3//a/text()').extract()
        href = response.xpath('//h3//a/@href').extract()
        res = dict()
        count_1 = len(tmp)
        count_2 = len(href)
        if count_1 < count_2:
            final = count_1
        else:
            final = count_2
        i=0
        while i < final:
            res[i] = {"title" : tmp[i].encode("utf-8"), "href" : href[i]}
            i += 1 
        filename = "vne.json"
        with open(filename, 'w') as f:
            f.write(json.dumps(res))