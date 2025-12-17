import pandas as pd
from datetime import datetime
import os
import shutil
import psutil
import statistics
import numpy as np 

from classes import Declaration
from templates import templates as temp

start_datetime = datetime.now()
start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

archive = './archive/'
incomming_path = './incomming/'
outgoing_path = './outgoing/'

process = psutil.Process()
snapshots = []

def main():
    start_datetime = datetime.now()
    start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

    incomming_directory = os.fsencode(incomming_path)

    for file in os.listdir(incomming_directory):
        excel_2_xml(file)

    if snapshots: # Check if the list is not empty
        average = statistics.mean(snapshots)
        print(f"Gemiddeld geheugen: {average / 1024**2:.2f} MB", flush=True)
    else:
        print("No data processed, skipping memory usage calculation.", flush=True)

    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}', flush=True)

def excel_2_xml(file):
    filename = os.fsdecode(file)
    filename_full = f"{incomming_path}{filename}"

    df = pd.read_excel(filename_full, engine="openpyxl", header=1)
    df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()

    if df.iloc[2, 9] == 0 and df.iloc[2, 9] == 0:
        first_row_totals_indicator = True

    departure = Declaration('departure')

    know_contianers = []
    previous_doc_items = []
    items = []
    itemcount = 1
    # Per rij doorlopen
    for index, row in df.iterrows():
        mem = process.memory_info().rss   # RAM in bytes
        snapshots.append(mem)

        # row is een Series, je kan per kolom opvragen
        templatecode = row.iloc[0]
        activecompany = row.iloc[1]
        referte_vak_7 = row.iloc[2]
        afzender = row.iloc[3]
        opdrachtgever = row.iloc[4]
        contact = row.iloc[5]
        gewenste_datum_insturen_aangiftedatum = row.iloc[6]
        gewenste_uur_insturen_aangiftetijd = row.iloc[7]
        container = row.iloc[8]
        aantal_verpakkingen = row.iloc[9]
        type_verpakkingen = row.iloc[10]
        goederencode = row.iloc[11]
        goederen_omschrijving = row.iloc[12]
        brutogewicht = row.iloc[13]
        netto_gewicht = row.iloc[14]
        vrachtlijst = row.iloc[15]
        lloydsnummer = row.iloc[16]
        billoflading = row.iloc[17]
        artikel = row.iloc[18]
        item = row.iloc[19]
        carriercode_agentcode = row.iloc[20]
        voorafg_doc_type = row.iloc[21]
        voorafg_document = row.iloc[22]
        datum_voorafg_document = row.iloc[23]
        kaai = row.iloc[24]
        schip = row.iloc[25]
        merken_en_nummers = row.iloc[26]
        schiplandcode = row.iloc[27]
        bestemmeling_naam = row.iloc[28]
        bestemmeling_straat = row.iloc[29]
        bestemmelingpostcode = row.iloc[30]
        bestemmelingplaats = row.iloc[31]
        bestemmelingland = row.iloc[32]
        douanekantoorbestemming = row.iloc[33]
        landvanvertrek = row.iloc[34]
        grenstransportmode = row.iloc[35]
        inlandtransportmode = row.iloc[36]
        inlandtransportidentiteit = row.iloc[37]
        boekingsref = row.iloc[38]
        zegel = row.iloc[39]
        vin = row.iloc[40]
        kvb = row.iloc[41]
        hs_code = row.iloc[42]

        if container not in know_contianers:
            know_contianers.append(container)
            header_data = temp.get_departure_header()

        else:
            sum_packages = df[df.iloc[:,8] == container].iloc[:, 9].sum()
            sum_bruto = df[df.iloc[:,8] == container].iloc[:, 13].sum()
            sum_netto = df[df.iloc[:,8] == container].iloc[:, 14].sum()

            header_data["template"] = templatecode
            header_data["company"] = activecompany
            header_data["commercialreference"] = referte_vak_7
            header_data["principal_id"] = opdrachtgever
            header_data["principal_contactPersonCode"] = contact
            header_data["ControlPackages"] = sum_packages
            header_data["ControlGrossmass"] = sum_bruto
            header_data["ControlNetmass"] = sum_netto
            header_data["countryOfDestinationCode"] = bestemmelingland
            header_data["placeOfLoadingCode"] = "" #sql
            header_data["countryOfDispatchExportCode"] = landvanvertrek
            if np.isnan(grenstransportmode):
                header_data["inlandTransportMode"] = 10
            else:
                header_data["inlandTransportMode"] = grenstransportmode

            header_data["identityOfMeansOfTransportAtDeparture"] = schip
            header_data["total_packages"] = sum_packages
            header_data["total_grossmass"] = sum_bruto
            header_data["total_nettmass"] = sum_netto
            header_data["consignor_id"] = afzender
            header_data["consignee_name"] = bestemmeling_naam
            header_data["consignee_streetAndNumber"] = bestemmeling_straat
            header_data["consignee_postalCode"] = bestemmelingpostcode
            header_data["consignee_City"] = bestemmelingplaats
            header_data["consignee_countryCode"] = bestemmelingland
            header_data["departureReferenceNumber"] = douanekantoorbestemming
            header_data["destinationReferenceNumber"] = douanekantoorbestemming #nakijken met taak

        item_data = temp.get_departure_item()

        item_data["goods_itemNumber"] = itemcount
        item_data["commodityCode"] = goederencode
        item_data["goods_description"] = goederen_omschrijving
        item_data["goods_grossMass"] = brutogewicht
        item_data["goods_netMass"] = netto_gewicht
        item_data["containerNumber"] = container
        item_data["kindOfPackages"] = type_verpakkingen
        item_data["numberOfPackages"] = aantal_verpakkingen

        if activecompany in "PORTWEB|WWL|WCT MEERHO|PORTZEEB|CAT1-PZEEB" and first_row_totals_indicator and index == 0:
            previous_doc_str = f"1{vrachtlijst}{lloydsnummer}"
            complement_info_str = f"{carriercode_agentcode}*{str(1).zfill(item)}*{billoflading}"
            
            item_data["previousDocumentType"] = "126E"
            item_data["previousDocumentReference"] = previous_doc_str
            item_data["complementOfInformation"] = complement_info_str

        if item not in previous_doc_items and itemcount == item:
            previous_doc_items.append(item)
            havencode = 1 #moet van sql query komen

            previous_doc_str = f"{havencode}{vrachtlijst}{lloydsnummer}*{artikel}"
            complement_info_str = f"{carriercode_agentcode}*{str(item).zfill(4)}*{billoflading}"
            
            item_data["previousDocumentType"] = "126E"
            item_data["previousDocumentReference"] = previous_doc_str
            item_data["complementOfInformation"] = complement_info_str

        items.append(item_data)
        
        if index == len(df) - 1 or df['Container'].iloc[index + 1] != container:
            header_data["ControlArticles"] = itemcount
            header_data["total_items"] = itemcount
            
            xml_string = departure.generate_declaration_xml_string(header_data, items)

            output_file_name = f"{outgoing_path}{start_datetime_str}_{filename}_{container}_{index + 1}_outgoing.xml"

            with open(output_file_name, "w") as f:
                f.write(xml_string)

            itemcount = 0 #reset itemcount
            items = [] #reset items
            previous_doc_items = [] #reset previous_doc_items

        itemcount += 1

    filename_full_archive = f'{archive}incomming/{filename}'
    shutil.move(filename_full, filename_full_archive)
