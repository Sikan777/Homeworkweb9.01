# Імпорт необхідних класів та функцій з бібліотек
from bson import json_util
from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE

# Підключення до бази даних MongoDB Atlas за допомогою функції connect
connect(
    db="HWW8",
    host="mongodb+srv://sikanbog:87654321@cluster0.vemep8z.mongodb.net/?retryWrites=true&w=majority",
)

# Оголошення класу Author, який наслідується від Document (модель MongoDB)
class Author(Document):
    # Оголошення полів для зберігання даних про автора
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()

    # Оголошення метаданих для моделі (назва колекції)
    meta = {"collection": "authors"}

# Оголошення класу Quote, який наслідується від Document (модель MongoDB)
class Quote(Document):
    # Оголошення полів для зберігання даних про цитату
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()

    # Оголошення метаданих для моделі (назва колекції)
    meta = {"collection": "quotes"}

    # Визначення методу to_json для конвертації об'єкту в JSON-рядок
    def to_json(self, *args, **kwargs):
        data = self.to_mongo(*args, **kwargs)
        data["author"] = self.author.fullname
        return json_util.dumps(data, ensure_ascii=False)

