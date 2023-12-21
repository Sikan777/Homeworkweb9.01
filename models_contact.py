# Імпорт необхідних класів та функцій з бібліотек
from mongoengine import connect, Document, StringField, BooleanField

# Підключення до бази даних MongoDB Atlas за допомогою функції connect
connect(
    db="HWW8",
    host="mongodb+srv://sikanbog:87654321@cluster0.vemep8z.mongodb.net/?retryWrites=true&w=majority",
)

# Оголошення класу Contact, який наслідується від Document (модель MongoDB)
class Contact(Document):
    # Оголошення полів для зберігання даних про контакт
    full_name = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    message_sent = BooleanField(default=False)
    phone = StringField()
    preferred_contact_method = StringField(choices=["email", "sms"], default="email")
