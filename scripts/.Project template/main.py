from tasks import main
import os
import pika # type: ignore
import json
import shutil

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')

ROUTING_KEY = os.getenv('ROUTING_KEY') 
QUEUE_NAME = os.getenv('QUEUE_NAME')  

def process_task(ch, method, properties, body):
    # ... (logica om de taak te verwerken is hetzelfde) ...
    # HIER KOMT DE TAAK UIT DIE JE WILT UITVOEREN IN DE CONTAINER
    try:
        task_data = json.loads(body.decode())
        file_path = task_data['file_path']

        if not os.path.exists(file_path):
            print(f" [!] Bestand bestaat niet ({file_path}), taak wordt verwijderd.", flush=True)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f" [*] Worker {ROUTING_KEY} verwerkt bestand: {file_path}", flush=True)

        main(file_path)

        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f" [*] Taak {ROUTING_KEY} voltooid en bericht bevestigd.", flush=True)
        
    except Exception as e:
        print(f" [!!!] Fout bij verwerking van taak {ROUTING_KEY}: {e}", flush=True)
        print(f" [!!!] Taak wordt verwijderd, file wordt verplaatst naar errordir", flush=True)

        shutil.move(file_path, "./error")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consumer():
    credentials = pika.PlainCredentials(username=RABBITMQ_USER, password=RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        )
    )

    channel = connection.channel()

    # 1. Declareer dezelfde Exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)

    # 2. Declareer de unieke wachtrij voor deze worker
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    
    # 3. Bind de wachtrij aan de Exchange met de unieke Routing Key
    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=QUEUE_NAME,
        routing_key=ROUTING_KEY # Alleen berichten met deze sleutel komen hier terecht
    )
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_task)

    print(f' [*] Worker {ROUTING_KEY} luistert naar berichten op queue {QUEUE_NAME}.', flush=True)
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
