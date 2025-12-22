import os
from watchdog.observers import Observer # type: ignore
from watchdog.events import FileSystemEventHandler  # type: ignore
import pika # type: ignore
import time
import json

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
EXCHANGE_NAME = os.getenv('EXCHANGE_NAME')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')

def publish_task(file_path_in_container, routing_key):
    credentials = pika.PlainCredentials(username=RABBITMQ_USER, password=RABBITMQ_PASS)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        )
    )
    
    channel = connection.channel()
    
    # Declareer de DIRECT exchange (deze is de 'router')
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='direct', durable=True)

    # We sturen een JSON-bericht met het pad dat de Worker kan gebruiken
    message = {
        'timestamp': time.time(),
        'file_path': file_path_in_container,
        'task_type': routing_key
    }
    
    channel.basic_publish(
        exchange=EXCHANGE_NAME, # Publiceer naar de Exchange
        routing_key=routing_key, # Gebruik de mapnaam als routing key
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    print(f" [x] Gepubliceerd bericht met sleutel '{routing_key}' voor bestand {file_path_in_container}")
    connection.close()

class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            
            # Voorbeeld pad: '/app/Scripts/Ncts Excel Upload/incomming/container.xls'
            path_parts = event.src_path.strip('/').split('/')

            # routing_key = 'Ncts Excel Upload/incomming'
            routing_key = '/'.join(path_parts[2:-1])

            # file_path = ./incomming/contcontainer.xls
            file_path = f"./{'/'.join(path_parts[3:])}"
            
            publish_task(file_path, routing_key)
            print(f"Detected: {routing_key}", flush=True)

def return_watchdog_dirs():
    with open("/config/config.txt") as f:
        return [line.strip() for line in f if line.strip()]

watched_paths = set()

def update_watched_dirs(observer, event_handler):
    new_paths = set(return_watchdog_dirs())
    for path in new_paths - watched_paths:
        if not os.path.isdir(path):
            print(f"⚠️ Pad bestaat niet of is geen directory: {path}", flush=True)
            continue

        try:
            observer.schedule(event_handler, path, recursive=False)
            watched_paths.add(path)
            print(f"✅ Nieuwe dir toegevoegd aan watchdog: {path}", flush=True)
        except Exception as e:
            print(f"❌ Fout bij toevoegen van {path}: {e}", flush=True)


if __name__ == "__main__":
    print("Start monitoring dirs...", flush=True)

    event_handler = FileHandler()
    observer = Observer()
    observer.start()

    try:
        while True:
            update_watched_dirs(observer, event_handler)
            time.sleep(5)  # elke 5 sec checken
    except KeyboardInterrupt:
        observer.stop()

    observer.join()