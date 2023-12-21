# Імпорт необхідних бібліотек та класів
import json
import random
from faker import Faker
from models_contact import Contact
import pika

# Створення об'єкту Faker для генерації випадкових даних
fake = Faker()

# Налаштування з'єднання з RabbitMQ
credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

# Оголошення черги RabbitMQ для відправки повідомлень
channel.queue_declare(queue="email_hello_world")

# Цикл для генерації 5 випадкових контактів та відправки їх в чергу
for _ in range(5):
    # Генерація випадкових даних для контакту
    full_name = fake.name()
    email = fake.email()
    phone = fake.phone_number()
    preferred_contact_method = random.choice(["email", "sms"])

    # Створення об'єкту Contact та збереження його у базі даних
    contact = Contact(
        full_name=full_name,
        email=email,
        phone=phone,
        preferred_contact_method=preferred_contact_method,
    )
    contact.save()

    # Створення повідомлення для відправки в чергу RabbitMQ
    message = {"contact_id": str(contact.id)}
    channel.basic_publish(
        exchange="", routing_key="email_hello_world", body=json.dumps(message)
    )
    print(f"Sent contact {contact.id} to the email queue")

# Закриття з'єднання з RabbitMQ
connection.close()