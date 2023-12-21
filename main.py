# Імпорт необхідних бібліотек
import json  # Імпорт бібліотеки для роботи з JSON
import scrapy  # Імпорт Scrapy для веб-скрапінгу
from itemadapter import ItemAdapter  # Імпорт засобу для адаптації об'єктів
from scrapy.crawler import CrawlerProcess  # Імпорт процесу Scrapy
from scrapy.item import Item, Field  # Імпорт необхідних класів для створення полів

# Оголошення класу для об'єкта цитати
class QuoteItem(Item):
    quote = Field()  # Поле для цитати
    author = Field()  # Поле для автора
    tags = Field()  # Поле для тегів

# Оголошення класу для об'єкта автора
class AuthorItem(Item):
    fullname = Field()  # Поле для повного імені автора
    born_date = Field()  # Поле для дати народження
    born_location = Field()  # Поле для місця народження
    description = Field()  # Поле для опису

# Оголошення класу для обробки даних
class DataPipline:
    quotes = []  # Список для зберігання цитат
    authors = []  # Список для зберігання даних про авторів

    # Метод для обробки елементу
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if "fullname" in adapter.keys():
            self.authors.append(dict(adapter))
        if "quote" in adapter.keys():
            self.quotes.append(dict(adapter))

    # Метод для завершення роботи павука
    def close_spider(self, spider):
        with open("quotes.json", "w", encoding="utf-8") as fd:
            json.dump(self.quotes, fd, ensure_ascii=False, indent=2)
        with open("authors.json", "w", encoding="utf-8") as fd:
            json.dump(self.authors, fd, ensure_ascii=False, indent=2)

# Оголошення павука Scrapy
class QuotesSpider(scrapy.Spider):
    name = "get_quotes"  # Назва павука
    allowed_domains = ["quotes.toscrape.com"]  # Домен, який може бути відвіданий
    start_urls = ["https://quotes.toscrape.com/"]  # Початкова URL-адреса для початку скрапінгу
    custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}  # Налаштування пайплайну

    # Метод для обробки головної сторінки
    def parse(self, response, **kwargs):
        for q in response.xpath("/html//div[@class='quote']"):
            quote = q.xpath("span[@class='text']/text()").get().strip()
            author = q.xpath("span/small[@class='author']/text()").get().strip()
            tags = q.xpath("div[@class='tags']/a/text()").extract()
            yield QuoteItem(quote=quote, author=author, tags=tags)
            yield response.follow(
                url=self.start_urls[0] + q.xpath("span/a/@href").get(),
                callback=self.parse_author,
            )

        next_link = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    # Метод для обробки сторінки автора
    @classmethod
    def parse_author(cls, response, **kwargs):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = (
            content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        )
        born_location = (
            content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        )
        description = (
            content.xpath("div[@class='author-description']/text()").get().strip()
        )
        yield AuthorItem(
            fullname=fullname,
            born_date=born_date,
            born_location=born_location,
            description=description,
        )

# Запуск павука, якщо код викликається безпосередньо
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()