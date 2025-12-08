import pandas as pd
from classes import Declaration
from datetime import datetime
import os
import shutil
import psutil
import time
import statistics

def NCTS_excel_upload():
    process = psutil.Process()
    snapshots = []

    start_datetime = datetime.now()
    start_datetime_str = start_datetime.strftime("%y%m%d%H%M%S")

    archive = './archive/'
    incomming_path = './incomming/'

    incomming_directory = os.fsencode(incomming_path)

    for file in os.listdir(incomming_directory):
        filename = os.fsdecode(file)
        filename_full = f"{incomming_path}{filename}"

        df = pd.read_excel(filename_full, engine="openpyxl", header=1)
        df.columns = df.columns.str.replace(r'\n', ' ', regex=True).str.strip()

        departure = Declaration('departure')

        know_contianers = []
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
            elif container in know_contianers:
                header_data = {
                    # ------------------------------------------------------------------
                    # Sectie 1: Basis Header Info (Root en CustomsStreamliner)
                    # ------------------------------------------------------------------
                    "dateCreation": "",           # Datum aanmaak (YYYY-MM-DD)
                    "timeCreation": "",           # Tijd aanmaak (HH:MM:SS)
                    "template": "",               # Sjabloon naam
                    "company": activecompany,                # Bedrijfsnaam
                    "messageStatus": "New",       # Status van het bericht (bv. New, Update)
                    "status": "Draft",            # Dossier status (bv. Draft, Sent)
                    "LRN": "",                    # Local Reference Number (Uniek per aangifte)
                    "user": "",                   # Gebruikerscode/Naam die de aangifte aanmaakt
                    "printLocation": "",          # Print locatie
                    "createDeclaration": "Y",     # Declaratie aanmaken (Y/N)
                    "sendDeclaration": "N",       # Declaratie verzenden (Y/N)
                    "sendPlannedDateTime": "",    # Geplande verzenddatum en -tijd (YYYY-MM-DDTHH:MM:SS)
                    "commercialreference": referte_vak_7,    # Dossiernummer ERP / Commerciële referentie
                    "terminalDeclarationType": "",# Type terminal aangifte
                    "terminal": "",               # Terminal code
                    "transhipment": "N",          # Overslag (Y/N)

                    # ------------------------------------------------------------------
                    # Sectie 2: Principal (Hoofdelijk Aansprakelijke)
                    # ------------------------------------------------------------------
                    "principal_id": "",           # EORI/ID van de Principal
                    "principal_contactPersonCode": "", # Contactpersoon code van de Principal

                    # ------------------------------------------------------------------
                    # Sectie 3: Controlewaarden
                    # ------------------------------------------------------------------
                    "ControlArticles": "0",       # Totaal aantal artikelen (items)
                    "ControlPackages": aantal_verpakkingen,       # Totaal aantal colli/pakketten
                    "ControlGrossmass": brutogewicht,   # Totale Bruto Massa
                    "ControlNetmass": netto_gewicht,     # Totale Netto Massa

                    # ------------------------------------------------------------------
                    # Sectie 4: Header Veldinformatie
                    # ------------------------------------------------------------------
                    "countryOfDestinationCode": "",  # Land van bestemming (bv. GB)
                    "placeOfLoadingCode": "",        # Plaats van belading code
                    "countryOfDispatchExportCode": "", # Land van verzending/export (bv. BE)
                    "inlandTransportMode": "",       # Vervoerswijze in het binnenland (Code)
                    "transportModeAtBorder": "",     # Vervoerswijze aan de grens (Code)
                    
                    "identityOfMeansOfTransportAtDeparture": "", # Identiteit vervoermiddel bij vertrek
                    "nationalityOfMeansOfTransportAtDeparture": "", # Nationaliteit vervoermiddel bij vertrek

                    "identityOfMeansOfTransportCrossingBorder": "", # Identiteit vervoermiddel dat grens overschrijdt
                    "nationalityOfMeansOfTransportCrossingBorder": "", # Nationaliteit vervoermiddel dat grens overschrijdt

                    "issuingDate": "",            # Datum van afgifte (YYYY-MM-DD)
                    "dialogLanguageIndicatorAtDeparture": "NL", # Taalcode voor dialoog
                    "nctsAccompanyingDocumentLanguageCode": "NL", # Taalcode voor het NCTS document

                    "total_items": "0",           # Totaal aantal goederenartikelen
                    "total_packages": aantal_verpakkingen,        # Totaal aantal colli
                    "total_grossmass": brutogewicht,    # Totaal bruto gewicht
                    "total_nettmass": netto_gewicht,     # Totaal netto gewicht

                    "simplifiedProcedureFlag": "0", # Vereenvoudigde procedure vlag (0=Nee)
                    "declarationPlace": "",       # Plaats van aangifte
                    # ------------------------------------------------------------------
                    # Sectie 5: Declarant (Aangever)
                    # ------------------------------------------------------------------
                    "declarant_id": "",           # EORI/ID van de Aangever
                    "declarant_name": "",
                    "declarant_streetAndNumber": "",
                    "declarant_postalCode": "",
                    "declarant_City": "",
                    "declarant_countryCode": "",
                    "declarant_tin": "",          # Fiscaal nummer (TIN)

                    # ------------------------------------------------------------------
                    # Sectie 6: Representative (Vertegenwoordiger)
                    # ------------------------------------------------------------------
                    "representative_user": "",
                    "representative_name": "",
                    "representative_authorisation": "", # Machtiging

                    # ------------------------------------------------------------------
                    # Sectie 7: Consignor (Aflader/Verzender)
                    # ------------------------------------------------------------------
                    "consignor_id": "",           # EORI/ID van de Verzender
                    "consignor_name": "",
                    "consignor_streetAndNumber": "",
                    "consignor_postalCode": "",
                    "consignor_City": "",
                    "consignor_countryCode": "",

                    # ------------------------------------------------------------------
                    # Sectie 8: Consignee (Ontvanger)
                    # ------------------------------------------------------------------
                    "consignee_id": "",           # EORI/ID van de Ontvanger
                    "consignee_name": "",
                    "consignee_streetAndNumber": "",
                    "consignee_postalCode": "",
                    "consignee_City": "",
                    "consignee_countryCode": "",

                    # ------------------------------------------------------------------
                    # Sectie 9: Douanekantoren, Controle & Garantie
                    # ------------------------------------------------------------------
                    "departureReferenceNumber": "", # Kantoor van vertrek code
                    "destinationReferenceNumber": "", # Kantoor van bestemming code

                    "controlResultCode": "",      # Controle resultaat code
                    "dateLimit": "",              # Datum limiet (YYYY-MM-DD)

                    "guaranteeType": "",          # Garantie type (bv. 1)
                    "guaranteeReference": "",     # Garantie referentienummer (GRN)
                    "accessCode": "",             # Toegangscode
                    "notValidForEC": "0",         # Niet geldig voor EC (1=Ja, 0=Nee)

                    "transportPlannedDate": "",   # Geplande transportdatum (YYYY-MM-DD)
                    "transportPlannedTime": ""    # Geplande transporttijd (HH:MM)

                }

            item = {
                # ------------------------------------------------------------------
                # Sectie 1: Basis Item Informatie
                # ------------------------------------------------------------------
                "goods_itemNumber": itemcount,         # Artikelnummer (1, 2, 3, etc.)
                "goods_description": goederen_omschrijving,        # Gedetailleerde goederenomschrijving
                "goods_grossMass": brutogewicht,      # Bruto massa (per item)
                "goods_netMass": netto_gewicht,        # Netto massa (per item)

                # ------------------------------------------------------------------
                # Sectie 2: Previous Administrative References (Voorgaande Documenten)
                # ------------------------------------------------------------------
                "previousDocumentType": "",       # Type van het voorgaande document (Code)
                "previousDocumentReference": "",  # Referentie van het voorgaande document
                "complementOfInformation": "",    # Aanvullende informatie
                "DocumentLineItemNr": "",         # Lijnnummer in het voorgaande document (indien van toepassing)

                # ------------------------------------------------------------------
                # Sectie 3: Containers
                # ------------------------------------------------------------------
                "containerNumber": container,            # Containernummer (indien van toepassing)

                # ------------------------------------------------------------------
                # Sectie 4: Packages (Colli)
                # ------------------------------------------------------------------
                "marksAndNumbersOfPackages": "",   # Merken en nummers op de verpakkingen
                "kindOfPackages": "",             # Type verpakking (Code, bv. CT voor Karton)
                "numberOfPackages": aantal_verpakkingen,          # Aantal colli
                "numberOfPieces": "0"             # Aantal stuks (indien van toepassing, bv. bij losse goederen)
            }

            items.append(item)
            
            if index == len(df) - 1 or df['Container'].iloc[index + 1] != container :
                
                xml_string = departure.generate_departure_xml_string(header_data, items)

                output_file_name = f"./outgoing/{start_datetime_str}_{filename}_{container}_{index + 1}_outgoing.xml"

                with open(output_file_name, "w") as f:
                    f.write(xml_string)

                itemcount = 1 #reset itemcount
                items = [] #reset items

        filename_full_archive = f'{archive}incomming/{filename}'
        shutil.move(filename_full, filename_full_archive)

    average = statistics.mean(snapshots)
    print(f"Gemiddeld geheugen: {average / 1024**2:.2f} MB")

    end_datetime = datetime.now()
    excecution_time = end_datetime - start_datetime
    print(f'Excecutiontime: {excecution_time}')
                    