import scrapy
import re
import unidecode
import pandas as pd

class SpiderCitacoes(scrapy.Spider):
    name = 'citacoes'
    items = []
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
            callback=self.parse_access,
        )

    def parse_access(self, response):
        has_logout_link = response.css('a[href="/logout"]').extract_first()
        if not has_logout_link:
            raise CloseSpider('**** falha de autenticação ****')
        self.log('**** acabei de fazer login ****')     

        for citacao in response.css('div.quote'):
            texto=''
            if ((citacao.css('a.tag::text').re(r'life') and citacao.css('small.author::text').re(r'Mark Twain'))
            or citacao.css('span.text::text').re(r'truth')):                
                item = {
                    "texto" : (citacao.css('span.text::text').extract_first()),
                    "autor" : citacao.css('small.author::text').extract_first(),
                    "tags": citacao.css('div.tags a.tag::text').extract(),
                    "numero_pagina": response.url.split("/")[-2],
                    "numero_regra": 1 if (citacao.css('a.tag::text').re(r'life') and citacao.css('small.author::text').re(r'Mark Twain'))  else 2,
                    "nome_arquivo": self.slugify(citacao.css('span.text::text').extract_first()[1:60])+'.txt',
                }     
                self.items.append(item) 
                yield item           
                
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                url=response.urljoin(next_page),
                callback=self.parse_access,
            )
        df = pd.DataFrame(self.items, columns=[ 'autor','tags', 'numero_pagina', 'numero_regra','nome_arquivo'])
        yield df.to_csv('citacoes.csv', sep = ';', mode = 'w', decimal='.',header = True, encoding="utf-8-sig")
       

    def slugify(self,text):
        text = unidecode.unidecode(text).lower()
        return re.sub(r'[\W_]+', '-', text)


           