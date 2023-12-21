# Імпорт бібліотек та класів
import json
from mongoengine.errors import NotUniqueError

# Імпорт моделей Author та Quote
from models import Author, Quote

# Початок виконання основної програми
if __name__ == "__main__":
    # Завантаження даних з файлу authors.json та збереження їх у базу даних
    with open("authors.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            try:
                # Створення об'єкта Author та збереження його у базі даних
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )
                author.save()
            except NotUniqueError:
                # Обробка виключення, яке виникає, якщо автор вже існує
                print(f"The author already exists {el.get('fullname')}")

    # Завантаження даних з файлу qoutes.json та збереження їх у базу даних
    with open("qoutes.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            # Знаходження автора за іменем в цитаті
            author, *_ = Author.objects(fullname=el.get("author"))

            # Створення об'єкта Quote та збереження його у базі даних
            quote = Quote(quote=el.get("quote"), tags=el.get("tags"), author=author)
            quote.save()