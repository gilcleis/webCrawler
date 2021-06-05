# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import unidecode


class WebcrawlerPipeline:
    def process_item(self, item, spider):    
        self.save_file_txt(item['texto'],item['nome_arquivo'])      
        return item
    
    def save_file_txt(self, texto,nome_arquivo):        
        with open(nome_arquivo+'.txt', 'wb') as f:
            f.write(texto.encode())

