from datetime import datetime
import os
import shutil
import time 
import re
import io
import json
import pandas as pd

from classes import Declaration, Docparser, Mail, DatabaseManager # type: ignore
from templates import templates as temp # type: ignore

TEST = False

start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

archive = './PLDA/archive/'
incomming_dir = './PLDA/incomming/'
outgoing_dir = './PLDA/outgoing/'
error_dir = "./PLDA/error/"
mailincomming_dir = './PLDA/mailincomming/'
test = "./PLDA/archive/responses/"

autosend = 'F'

db = DatabaseManager()

# ----------------------------------------
# 1.0 Read Mail and safe attachements
# ----------------------------------------
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

                if be_match:
                    extracted_data.append({
                        'Container': cont_match.group(0) if cont_match else "Onbekend",
                        'BE_Nummer': be_match.group(1),
                        'BEI_Nummer': bei_match.group(1) if bei_match else None
                    })
            
            return pd.DataFrame(extracted_data) if extracted_data else None

def read_mailincomming(file_path):
    #Creating a time key to match mail to attachements
    now_datetime = datetime.now()
    now_datetime_str = now_datetime.strftime("%y%m%d%H%M%S")

    filename = os.path.basename(file_path)

    _, _, _, _, body = Mail.mail_parser(file_path, incomming_dir, now_datetime_str, error_dir)

    #Upload to db
    df = read_table_mail_pd(body)

    query = """
            CREATE TABLE IF NOT EXISTS stevocatncts(
                insertdatetime varchar(12),
                container varchar(15),
                t1 varchar(20),
                bei varchar(20)
            )
            """
    db.execute_query(query)

    print(f"Load table into database, datetimekey: {now_datetime_str}", flush=True)
    if df is None or df.empty:
        query = """
                insert into stevocatncts
                values (:insertdatetime)
                """
        val = {"insertdatetime": now_datetime_str,}
        db.execute_query(query, val)

    else:
        for _, row in df.iterrows():
            query = """
                    INSERT INTO stevocatncts (insertdatetime, container, t1, bei) 
                    VALUES (:insertdatetime, :container, :t1, :bei)
                    """
            val = {"insertdatetime": now_datetime_str,
                "container": row["Container"],
                "t1": row["BE_Nummer"],
                "bei": row["BEI_Nummer"]
                }
        
            db.execute_query(query, val)

    filename_full_archive = f'{archive}mailincomming/{now_datetime_str}_{filename}'
    shutil.move(file_path, filename_full_archive)

    print(f"Archived eml to: {filename_full_archive}", flush=True)

# ----------------------------------------
# 2. Send att 2 Docparser an create XML
# ----------------------------------------

def main(file_path):
    global start_datetime, start_datetime_str
    start_datetime = datetime.now()
    start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

    docparser = Docparser()

    if not TEST:
        response = docparser.upload_file(file_path)
        time.sleep(2)
        data = docparser.return_json(response)
    else:
        with open("./archive/responses/response2.json", "r") as f:
            data = json.load(f)

    json_2_xml(data, file_path)

    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)

def json_2_xml(data, file_path):
    filename = os.path.basename(file_path)
    datetimekey = filename[:12]

    im_declaration = Declaration("import")

    header_data = temp.get_PLDA_header()
    item_data = temp.get_PLDA_item()

    mrn = data["2___mrn"]

    print(datetimekey, mrn, flush=True)
    query = """
            select bei 
            from stevocatncts
            where insertdatetime = :dt and t1 = :t1
            """
    
    df = db.fetch_as_dataframe(query, {"dt": datetimekey, "t1": mrn})
    if not df.empty:
        previous_document = df.iloc[0, 0]
    else:
        previous_document = None


    header_data["template"] = "STEVOCAT_AUTO_IM"
    header_data["company"] = "ACS"
    header_data["sendDeclaration"] = autosend

    header_data["container"] = data["7_10_container_identification_number"]

    if previous_document:
        item_data["documentReference"] = previous_document
        item_data["documentType"] = "NMRN"
    else:
        item_data["documentReference"] = mrn
        item_data["documentType"] = "N821"

    items = [item_data]

    xml_string = im_declaration.generate_declaration_xml_string(header_data, items)

    output_file_name = f"{outgoing_dir}{start_datetime_str}_{filename}_outgoing.xml"
    print(f"Output saved at: {output_file_name}")

    with open(output_file_name, "w") as f:
        f.write(xml_string)

    filename_full_archive = f'{archive}incomming/{filename}'
    shutil.move(file_path, filename_full_archive)


