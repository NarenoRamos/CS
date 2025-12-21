import xml.sax.saxutils as saxutils
from collections import defaultdict
import smtplib
import imaplib
import email
from email.message import EmailMessage
import requests
import os
import re
    
class Declaration():
    def __init__ (self, type: str):
        base_path = os.path.dirname(os.path.abspath(__file__))
        template_folder = os.path.join(base_path, "templates")

        #Use NCTS template
        if type == 'departure':
            try:
                with open(os.path.join(template_folder, "NCTS_Template.xml"), "r", encoding="iso-8859-1") as f:
                    self.declaration_header_template = f.read()
                
                with open(os.path.join(template_folder, "NCTS_Item_Template.xml"), "r", encoding="iso-8859-1") as f:
                    self.declaration_item_template = f.read()
            except FileNotFoundError:
                print(f"FOUT: Kan de template bestanden niet vinden in {template_folder}")
                raise

        #Use PLDA import template
        if type == 'import':
            try:
                with open(os.path.join(template_folder, "PLDA_ImportTemplate.xml"), "r", encoding="iso-8859-1") as f:
                    self.declaration_header_template = f.read()
                
                with open(os.path.join(template_folder, "PLDA_ItemTemplate.xml"), "r", encoding="iso-8859-1") as f:
                    self.declaration_item_template = f.read()
            except FileNotFoundError:
                print("FOUT: Kan de template bestanden niet vinden in de map ./templates/")
                raise
        
        #Use PLDA Export template
        if type == 'export':
            try:
                with open(os.path.join(template_folder, "PLDA_ExportTemplate.xml"), "r", encoding="iso-8859-1") as f:
                    self.declaration_header_template = f.read()
                
                with open(os.path.join(template_folder, "PLDA_ItemTemplate.xml"), "r", encoding="iso-8859-1") as f:
                    self.declaration_item_template = f.read()
            except FileNotFoundError:
                print("FOUT: Kan de template bestanden niet vinden in de map ./templates/")
                raise


    def _sanitize_data(self, data_dict):
            """
            Zorgt ervoor dat speciale XML karakters (zoals <, >, &) in de data
            worden escaped om corrupte XML te voorkomen.
            """
            clean_dict = {}
            for key, value in data_dict.items():
                if isinstance(value, str):
                    clean_dict[key] = saxutils.escape(value)
                else:
                    clean_dict[key] = value
            return clean_dict
    
    def generate_declaration_xml_string(self, header_data: dict, items_data: list[dict]) -> str:
        """
        Genereert de volledige XML string.
        
        :param header_data: Dictionary met waarden voor de hoofding.
        :param items_data: Lijst van Dictionaries, één per item.
        """
        
        # 1. Genereer de string voor alle items
        items_xml_parts = []
        for item in items_data:
            # Data schoonmaken (escaping)
            clean_item = self._sanitize_data(item)
            try:
                # Invullen van de item template
                item_str = self.declaration_item_template.format(**clean_item)
                items_xml_parts.append(item_str)
            except KeyError as e:
                raise ValueError(f"Ontbrekende data in item: {e}")

        # Voeg alle items samen, gescheiden door een nieuwe regel
        full_items_string = "\n".join(items_xml_parts)

        # 2. Bereid de header data voor
        # Voeg de gegenereerde items string toe aan de header data dictionary
        # zodat deze op de plek van {goods_items_xml} komt.
        full_header_data = self._sanitize_data(header_data)
        full_header_data['goods_items_xml'] = full_items_string

        defaultdict(str, full_header_data)

        # 3. Genereer de finale XML
        try:
            final_xml = self.declaration_header_template.format(**full_header_data)
            return final_xml
        except KeyError as e:
            raise ValueError(f"Ontbrekende data in de header: {e}")
        
class Docparser():
    def __init__(self):
        self.docparser_api_key = os.environ.get('DOCPARSER_API_KEY')
        self.parser_id = os.environ.get('PARSER_ID')

    def upload_file(self, file_path):
        filename = os.fsdecode(file_path)

        post_url = f"https://api.docparser.com/v1/document/upload/{self.parser_id}"
        
        print(f"Sending file {filename} to parser:{self.parser_id}", flush=True)
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(post_url, files=files, auth=(self.docparser_api_key, ""))
            data = response.json()

            if isinstance(data, list):
                data = data[0]

            return data
        
    def return_json(self, upload_response):
        if not 'id' in upload_response:
            print(f"ERROR: No id found in response", flush=True)
            raise 
        else:
            document_id = upload_response.get("id")

        print(f"Fetching JSON", flush=True)
        fetch_url = f"https://api.docparser.com/v1/results/{self.parser_id}/{document_id}"
        response = requests.get(fetch_url, auth=(self.docparser_api_key, ""))

        data = response.json()
        if isinstance(data, list):
            data = data[0]
            
        return data
    
class Mail():
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 587

        self.username = "giani.narenoramos@gmail.com"
        self.app_password = "raug ixso uatc fwif"   # maak via je Google-account (2FA vereist)

    def sendmail(self, message, to):
        msg = EmailMessage()
        msg["From"] = self.username
        msg["To"] = "giani.ramos@outlook.com"
        msg["Subject"] = "Berichten"
        msg.set_content(message)

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(self.username, self.app_password)
            smtp.send_message(msg)

    def _sanitize_filename(self, name):
        # Verwijder tekens die niet in bestandsnamen mogen
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()
    
    def save_mail(self, substring, dir):
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(self.username, self.app_password )
        mail.select("inbox")

        status, data = mail.search(None, f'(SUBJECT "{substring}")')
        mail_ids = data[0].split()

        if not mail_ids:
            print(f"No mails found with '{substring}' in subject.")
            return
        
        print(f"{len(mail_ids)} mails found. Saving mail...")

        #hieronder nakijken

        for m_id in mail_ids:
            # 3. Haal de ruwe data op (RFC822 is het .eml formaat)
            status, msg_data = mail.fetch(m_id, "(RFC822)")
            raw_email = msg_data[0][1] # Dit zijn de ruwe bytes

            # 4. Onderwerp ophalen voor de bestandsnaam
            # We gebruiken een simpele fetch voor de header om de naam te bepalen
            status, header_data = mail.fetch(m_id, "(BODY[HEADER.FIELDS (SUBJECT)])")
            subject = header_data[0][1].decode().replace("Subject: ", "").strip()
            
            filename = self._sanitize_filename(f"{subject}_{m_id.decode()}.eml")
            filepath = os.path.join(dir, filename)

            # 5. Opslaan als binary file
            with open(filepath, "wb") as f:
                f.write(raw_email)
            
            print(f"Opgeslagen: {filename}")

        mail.logout()

