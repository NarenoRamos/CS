import pandas as pd # type: ignore
from datetime import datetime
import os
import shutil
import numpy as np # type: ignore
import requests
import time 

from classes import Declaration # type: ignore
from templates import templates as temp # type: ignore

start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")
filename = ""
file_path = ""

docparser_api_key = os.environ.get('DOCPARSER_API_KEY')
parser_id = os.environ.get('PARSER_ID')

archive = './archive/'
incomming_dir = './incomming/'
outgoing_dir = './outgoing/'
autosend = 'F'

def main():
    global filename, file_path, start_datetime, start_datetime_str

    incomming_directory = os.fsencode(incomming_dir)

    files = os.listdir(incomming_directory)

    if not files:
        print(f"No files detected", flush=True)

    for file in files:
        data = send_2_docparser(file)

        json_2_xml(data)

    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)

def send_2_docparser(file):
    global filename, file_path, start_datetime, start_datetime_str

    filename = os.fsdecode(file)
    file_path = f"{incomming_dir}{filename}"

    post_url = f"https://api.docparser.com/v1/document/upload/{parser_id}"
    
    print(f"Sending file to parser:{parser_id}", flush=True)
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(post_url, files=files, auth=(docparser_api_key, ""))
        data = response.json()

        document_id = data.get('id')
        
    time.sleep(20)

    print(f"Fetching JSON", flush=True)
    fetch_url = f"https://api.docparser.com/v1/results/{parser_id}/{document_id}"
    response = requests.get(fetch_url, auth=(docparser_api_key, ""))

    data = response.json()
    data = data[0]

    print(type(data), flush=True)
    return data

def json_2_xml(data):
    global filename, file_path, start_datetime, start_datetime_str

    print(type(data), flush=True)
    im_declaration = Declaration("import")

    header_data = temp.get_PLDA_header()
    item_data = temp.get_PLDA_item()

    print(header_data["template"], flush=True)
    print(item_data["netMass"], flush=True)

    header_data["template"] = "STEVOCAT_AUTO_IM"
    header_data["company"] = "ACS"
    header_data["sendDeclaration"] = autosend

    item_data["commodityCode"] = data["6_14_commodity_code"]

    items = [item_data]

    print("voor xmlstring", flush=True)
    xml_string = im_declaration.generate_declaration_xml_string(header_data, items)

    output_file_name = f"{outgoing_dir}{start_datetime_str}_{filename}_outgoing.xml"

    with open(output_file_name, "w") as f:
        f.write(xml_string)

    filename_full_archive = f'{archive}incomming/{filename}'
    shutil.move(file_path, filename_full_archive)