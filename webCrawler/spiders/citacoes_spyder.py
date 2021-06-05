import scrapy

class SpiderCitacoes(scrapy.Spider):
    name = 'citacoes'

    start_urls = [
            'http://quotes.toscrape.com/page/1/'
        ]

    def parse(self, response):          
        for citacao in response.css('div.quote'):
            yield {
                "texto" : citacao.css('span.text::text').extract_first(),
                "autor" : citacao.css('small.author::text').extract_first(),
                "tags": citacao.css('div.tags a.tag::text').extract(),
                "pagina": response.url.split("/")[-2],
                "regra": 'Regra2' if citacao.css('span.text::text').re(r'truth')  else 'Regra1',                
            }
           