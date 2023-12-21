# Імпорт необхідних бібліотек та класів
import json
import pika
from models_contact import Contact

# Створення об'єкту PlainCredentials для автентифікації з RabbitMQ
credentials = pika.PlainCredentials("guest", "guest")

# Створення об'єкту BlockingConnection для взаємодії з RabbitMQ
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)

# Створення каналу для обміну даними з RabbitMQ
channel = connection.channel()

# Оголошення функції callback для обробки отриманих повідомлень
def callback(ch, method, properties, body):
    # Виведення отриманого повідомлення
    print(f" [x] Received {body}")

    # Розпакування та обробка JSON-повідомлення
    message = json.loads(body)
    contact_id = message["contact_id"]
    contact = Contact.objects.get(id=contact_id)

    # Виведення інформації про відправку повідомлення
    print(f"Sending email to {contact.email} for contact {contact.id}")

    # Зміна статусу відправлення та збереження об'єкта Contact в базі даних
    contact.message_sent = True
    contact.save()

    # Виведення інформації про відправлене повідомлення
    print(f"Email sent to {contact.email} for contact {contact.id}")

# Підписка на отримання повідомлень з черги "email_hello_world"
channel.basic_consume(
    queue="email_hello_world", on_message_callback=callback, auto_ack=True
)

# Виведення повідомлення про очікування нових повідомлень
print(" [*] Waiting for messages. To exit press CTRL+C")

# Запуск обробки отриманих повідомлень
channel.start_consuming()