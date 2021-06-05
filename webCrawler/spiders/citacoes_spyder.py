import scrapy

class SpiderCitacoes(scrapy.Spider):
    name = 'citacoes'

    start_urls = [
            'http://quotes.toscrape.com/login'
        ]

    def parse(self, response):
        self.log('visitei a página de login: {}'.format(response.url))
        token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        yield scrapy.FormRequest(
            url='http://quotes.toscrape.com/login',
            formdata={
                'username': 'gilclei',
                'password': '123456',
                'csrf_token': token,
            },
            callback=self.parse_acess,
        )

    def parse_acess(self, response):
        has_logout_link = response.css('a[href="/logout"]').extract_first()
        if not has_logout_link:
            raise CloseSpider('**** falha de autenticação ****')
        self.log('**** acabei de fazer login ****')      
        for citacao in response.css('div.quote'):
            teste =  {
                "texto" : citacao.css('span.text::text').extract_first(),
                "autor" : citacao.css('small.author::text').extract_first(),
                "tags": citacao.css('div.tags a.tag::text').extract(),
                "pagina": response.url.split("/")[-2],
                "regra": 'Regra2' if citacao.css('span.text::text').re(r'truth')  else 'Regra1',                
            }
           