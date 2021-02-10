# spiders/__init__.py
import scrapy


from ..items import NewsItem

class GuarduanSpider(scrapy.Spider):
    name = 'news'
    start_urls=[
        'https://www.theguardian.com/world/all',
    #   'https://www.theguardian.com/commentisfree/all',
    #   'https://www.theguardian.com/film/all',
    #   'https://www.theguardian.com/games/all',
    #   'https://www.theguardian.com/music/all',
    #   'https://www.theguardian.com/lifeandstyle/all',
    #   'https://www.theguardian.com/stage/all',
    #   'https://www.theguardian.com/fashion/all',
    #   'https://www.theguardian.com/business/all',
    #   'https://www.theguardian.com/money/all',
    ]



    def parse(self, response):
        article_url_selector = '//*[contains(@class,"fc-item__link")]//@href'
        for article_url in response.xpath(article_url_selector).extract():
            yield scrapy.Request(
                url=article_url,
                callback=self.parse_article
            )

        next_page_selector = '//*[contains(@class,"pagination__action--static") and contains(@rel,"next")]//@href'
        next_page = response.xpath(next_page_selector).extract_first()
        if (next_page):
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )


    def parse_article(self, response):
        # Test if the article is already crawled
        if ('cached' in response.flags):
            return


        content_selector = ' //*[contains(@class,"content__article-body")]//p//text() | //*[contains(@class,"article-body-commercial-selector ")]//p//text() '
        author_selector = '//a[contains(@rel,"author")]//*/text() | //a[contains(@rel,"author")]//text() | //*[contains(@data-link-name,"byline")]/div[contains(@class,"css-1rv9jci")]//text()  | //p[contains(@class,"byline")]//text()'
        category_selector = '//a[contains(@data-link-name,"article section")]//*//text()'
        publishing_date_selector = '//*[contains(@class,"content__dateline-wpd")]//text() | //label[contains(@class,"css-hn0k3p")]//text() '

        item = NewsItem()

        item['author'] =  response.xpath(author_selector).extract()
        item['headline'] = response.css('h1::text').extract()
        item['content'] = ''.join(response.xpath(content_selector).extract())
        item['category'] = response.xpath(category_selector).extract()
        item['url'] = response.request.url
        item['published_at'] = response.xpath(publishing_date_selector).extract_first()

        yield item

