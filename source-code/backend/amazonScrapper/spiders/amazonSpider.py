import scrapy
import urllib.parse as urlparse
import json
import os

class AmazonSpider(scrapy.Spider):
    name = "amazonSpider"
    allowed_domains = ["amazon.com"]

    def __init__(self, keywords=None, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        if keywords:
            self.keywords = keywords.split(',')
        else:
            self.keywords = []

    def start_requests(self):
        base_url = 'https://www.amazon.com/s?k='
        for keyword in self.keywords:
            url = f'{base_url}{urlparse.quote(keyword)}'
            print('The url is:', url)
            yield scrapy.Request(url=url, callback=self.parse, meta={'keyword': keyword})

    def parse(self, response):
        keyword = response.meta['keyword']
        products = []

        for product in response.css('div.s-main-slot div.s-result-item'):
            title = product.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 > a > span.a-size-medium.a-color-base.a-text-normal::text').get()
            price = product.css('span.a-price > span.a-offscreen::text').get()
            product_url = product.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 > a::attr(href)').get()
            image_url = product.css('div.a-section.aok-relative.s-image-fixed-height img.s-image::attr(src)').get()
            ratings = product.css('span[aria-label*="ratings"] > a > span.a-size-base.s-underline-text::text').get()


            if title and price and product_url and image_url and ratings:
                products.append({
                    'title': title,
                    'price': price,
                    'product_url': urlparse.urljoin(response.url, product_url),
                    'image_url': image_url,
                    'ratings': ratings
                })

        # Save results to a JSON file named after the keyword
        filename = f'{keyword}.json'
        with open(filename, 'w') as f:
            json.dump({keyword: products}, f)

        # self.log(f'Scraped {len(products)} products for keyword: {keyword} and saved to {filename}')
