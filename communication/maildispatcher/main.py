import imaplib
import os
import json
import time

IMAP_SERVER = os.environ.get('SMTP_HOST')
EMAIL_USER = os.environ.get('SMTP_USER')
PASSWORD = os.environ.get('SMTP_PASS') 

def get_config():
    try:
        with open('/config/config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Config fout: {e}")
        return {}

def delete_mail(imap, message_num):
    imap.store(message_num, '+FLAGS', '\\Deleted')

def save_mail(imap, message_num, dir):

    _, data = imap.fetch(message_num, "(RFC822)")

    for response_part in data:
        if isinstance(response_part, tuple):
            # De e-mail inhoud zit in de tweede index van de tuple
            msg_content = response_part[1]
            
            # Bepaal de bestandsnaam (bijv. email_1.eml)
            file_path = os.path.join(dir, f"email_{message_num.decode()}.eml")
            
            # Schrijf de data weg als binaire data ('wb')
            with open(file_path, 'wb') as f:
                f.write(msg_content)
            
            print(f"Saved at: {file_path}", flush=True)
            delete_mail(imap, message_num)

def main():
    print("Logging on ...", flush=True)
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_USER, PASSWORD)
    print("Connected succesfully!", flush=True)
        
    while True: 
        try:
            print("Reading mails for configured subjects...", flush=True)
            config = get_config()
            imap.select("Inbox")
            
            for subject in config:
                _, data = imap.search(None, f"(SUBJECT {subject})")
                message_nums = data[0].split()

                for num in message_nums:
                    save_mail(imap, num, config[subject])

            imap.expunge()

            time.sleep(5)

        except Exception as e:
            print(f"Could not connect: {e}", flush=True)
            print("Reconecting over 30 seconden...", flush=True)
            time.sleep(30)

if __name__ == "__main__":
    main()
