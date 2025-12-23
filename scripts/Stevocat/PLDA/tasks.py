from datetime import datetime
import os
import shutil
import time 
import re
import io
import pandas as pd

from classes import Declaration, Docparser, Mail, DatabaseManager # type: ignore
from templates import templates as temp # type: ignore

start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")
filename = ""
file_path = ""

archive = './archive/'
incomming_dir = './incomming/'
outgoing_dir = './outgoing/'
error_dir = "./error/"
autosend = 'F'

db = DatabaseManager()

def check_db(filename):
    datetimekey = filename[:11]
    query = """
            select inserdatetime 
            from stevocatncts
            where insertdatetime = %s
            """
    
    df = db.fetch_as_dataframe(query, (datetimekey, ))

    if df is not None and not df.empty:
        return True

    return False

def main():
    global filename, file_path, start_datetime, start_datetime_str

    incomming_directory = os.fsencode(incomming_dir)
    files = os.listdir(incomming_directory)

    docparser = Docparser()

    if not files:
        print(f"No files detected", flush=True)

    for file in files:
        filename = os.fsdecode(file)
        check = check_db(filename)

        if not check:
            return 0

        file_path = f"{incomming_dir}{filename}"

        response = docparser.upload_file(file_path)
        time.sleep(2)
        data = docparser.return_json(response)

        json_2_xml(data)

    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)

    return 1

def json_2_xml(data):
    # global filename, file_path, start_datetime, start_datetime_str

    im_declaration = Declaration("import")

    header_data = temp.get_PLDA_header()
    item_data = temp.get_PLDA_item()

    header_data["template"] = "STEVOCAT_AUTO_IM"
    header_data["company"] = "ACS"
    header_data["sendDeclaration"] = autosend

    header_data["container"] = data["7_10_container_identification_number"]

    items = [item_data]

    xml_string = im_declaration.generate_declaration_xml_string(header_data, items)

    output_file_name = f"{outgoing_dir}{start_datetime_str}_{filename}_outgoing.xml"
    print(f"Output saved at: {output_file_name}")

    with open(output_file_name, "w") as f:
        f.write(xml_string)

    filename_full_archive = f'{archive}incomming/{filename}'
    shutil.move(file_path, filename_full_archive)

mailincomming_dir = './mailincomming/'
test = "./archive/responses/"

def read_table_mail_pd(html_content):
    try:
        html_io = io.StringIO(html_content)
        all_tables = pd.read_html(html_io)
    except ValueError:
        print("Geen tabellen gevonden in de HTML.")
        return None

    container_pattern = r'[A-Z]{4}\d{7}'
    pattern_t1 = r'(\d{2}BE\w*)'
    pattern_bei = r'(\d{2}BEI\w*)'

    for df in all_tables:
        if df.astype(str).stack().str.contains(container_pattern, regex=True).any():
            
            extracted_data = []

            for _, row in df.iterrows():
                row_string = " ".join(row.astype(str))
                
                cont_match = re.search(container_pattern, row_string)
                be_match = re.search(pattern_t1, row_string)
                bei_match = re.search(pattern_bei, row_string)

                if be_match and bei_match:
                    extracted_data.append({
                        'Container': cont_match.group(0) if cont_match else "Onbekend",
                        'BE_Nummer': be_match.group(1),
                        'BEI_Nummer': bei_match.group(1)
                    })
            
            return pd.DataFrame(extracted_data) if extracted_data else None

def read_mailincomming():
    incomming_directory = os.fsdecode(mailincomming_dir)
    files = os.listdir(incomming_directory)

    if not files:
        print(f"No files detected", flush=True)

    for file in files:
        #Creating a time key to match mail to attachements
        now_datetime = datetime.now()
        now_datetime_str = now_datetime.strftime("%y%m%d%H%M%S")

        filename = os.fsdecode(file)
        file_path = f"{mailincomming_dir}{filename}"

        _, _, _, _, body = Mail.mail_parser(file_path, incomming_dir, now_datetime_str, error_dir)

        #Upload to db
        df = read_table_mail_pd(body)

        query = """
                CREATE TABLE IF NOT EXISTS stevocatncts(
                    insertdatetime varchar(12),
                    container varchar(15),
                    t1 varchar(20) PRIMARY KEY,
                    bei varchar(20)
                )
                """
        
        db.execute_query(query)

        print(f"Load table into database, datetimekey: {now_datetime_str}", flush=True)
        for _, row in df.iterrows():
            query = """
                    INSERT INTO stevocatncts (insertdatetime, container, t1, bei) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (t1) 
                    DO UPDATE SET 
                        bei = EXCLUDED.bei,
                        container = EXCLUDED.container,
                        insertdatetime = EXCLUDED.insertdatetime
                    WHERE EXCLUDED.bei IS NOT NULL AND EXCLUDED.bei != '';
                    """
            val = (now_datetime_str, row["Container"], row["BE_Nummer"], row["BEI_Nummer"])
        
            db.execute_query(query, val)

        filename_full_archive = f'{archive}mailincomming/{now_datetime_str}_{filename}'
        shutil.move(file_path, filename_full_archive)

        print(f"Archived eml to: {filename_full_archive}", flush=True)
