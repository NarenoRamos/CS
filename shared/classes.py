import xml.sax.saxutils as saxutils
from collections import defaultdict
import smtplib
from email.message import EmailMessage
import requests
import os
from email import policy
from email.parser import BytesParser
import shutil
import pandas as pd
from sqlalchemy import create_engine, text


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
        self.smtp_host = os.environ.get('SMTP_HOST')
        self.smtp_port = os.environ.get('SMTP_PORT')

        self.username = os.environ.get('SMTP_USER')
        self.app_password = os.environ.get('SMTP_PASS') 

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

    @staticmethod
    def mail_parser(mail_file, attachements_dir, datetime_str, error_dir):
        if not mail_file.endswith('.eml'):
            shutil.move(mail_file, error_dir)
            print(f"File: {filename} is no eml file, moved to error folder.")
            return
        
        with open(mail_file, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)

        sender = msg["From"]
        receiver = msg["To"]
        subject = msg["Subject"]
        date = msg["Date"]

        html_body = msg.get_body(preferencelist=('html',))
        
        if html_body:
            body_content = html_body.get_content()
        else:
            print("Geen HTML body gevonden in deze mail.")
            body_content = ""

        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                filepath = os.path.join(attachements_dir, f"{datetime_str}_{filename}")
                with open(filepath, "wb") as f:
                    f.write(part.get_payload(decode=True))
                print(f"Attachment saved: {filename}", flush=True)

        return (sender, receiver, subject, date, body_content)
    
class DatabaseManager:
    def __init__(self):
        host = os.getenv('POSTGRES_HOST')
        database = os.getenv('POSTGRES_DB')
        user = os.getenv('POSTGRES_USER')
        password = os.getenv('POSTGRES_PASSWORD')
        port = os.getenv('DB_PORT')

        self.db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

        self.engine = create_engine(self.db_uri, pool_pre_ping=True)
    
    def execute_query(self, query, params=None):
        """
        Voert een query uit (INSERT, UPDATE, DELETE) met automatische commit.
        """
        try:
            # engine.begin() opent een transactie en commit automatisch aan het einde
            with self.engine.begin() as conn:
                # We gebruiken text() voor SQLAlchemy compatibiliteit
                result = conn.execute(text(query), params or {})
                return result.rowcount 
        except Exception as e:
            print(f"Fout bij uitvoeren query: {e}", flush=True)
            return None

    def fetch_as_dataframe(self, query, params=None):
        """
        Voert een SELECT query uit en geeft het resultaat terug als een Pandas DataFrame.
        Dit lost de UserWarning op.
        """
        try:
            # Gebruik de engine direct in pandas
            with self.engine.connect() as conn:
                df = pd.read_sql(text(query), conn, params=params)
                return df
        except Exception as e:
            print(f"Fout bij ophalen DataFrame: {e}", flush=True)
            return None