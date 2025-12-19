from datetime import datetime
import os
import shutil
import time 

from classes import Declaration, Docparser # type: ignore
from templates import templates as temp # type: ignore

start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")
filename = ""
file_path = ""

archive = './archive/'
incomming_dir = './incomming/'
outgoing_dir = './outgoing/'
autosend = 'F'

def main():
    global filename, file_path, start_datetime, start_datetime_str

    incomming_directory = os.fsencode(incomming_dir)

    files = os.listdir(incomming_directory)

    docparser = Docparser()

    if not files:
        print(f"No files detected", flush=True)

    for file in files:
        filename = os.fsdecode(file)
        file_path = f"{incomming_dir}{filename}"

        response = docparser.upload_file(file_path)
        time.sleep(2)
        data = docparser.return_json(response)

        json_2_xml(data)

    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)

def json_2_xml(data):
    global filename, file_path, start_datetime, start_datetime_str

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