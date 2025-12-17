def get_departure_header():
    dir = {
        # ------------------------------------------------------------------
        # Sectie 1: Basis Header Info (Root en CustomsStreamliner)
        # ------------------------------------------------------------------
        "dateCreation": "",           # Datum aanmaak (YYYY-MM-DD)
        "timeCreation": "",           # Tijd aanmaak (HH:MM:SS)
        "template": "",               # Sjabloon naam
        "company": "",                # Bedrijfsnaam
        "messageStatus": "",       # Status van het bericht (bv. New, Update)
        "status": "",            # Dossier status (bv. Draft, Sent)
        "LRN": "",                    # Local Reference Number (Uniek per aangifte)
        "user": "",                   # Gebruikerscode/Naam die de aangifte aanmaakt
        "printLocation": "",          # Print locatie
        "createDeclaration": "T",     # Declaratie aanmaken (T/F)
        "sendDeclaration": "F",       # Declaratie verzenden (T/F)
        "sendPlannedDateTime": "",    # Geplande verzenddatum en -tijd (YYYY-MM-DDTHH:MM:SS)
        "commercialreference": "",    # Dossiernummer ERP / Commerciële referentie
        "terminalDeclarationType": "",# Type terminal aangifte
        "terminal": "",               # Terminal code
        "transhipment": "N",          # Overslag (Y/N)
        
        # Custom placeholder voor de items, moet altijd aanwezig zijn
        "goods_items_xml": "",        # Wordt automatisch gevuld door de generate_xml methode!

        # ------------------------------------------------------------------
        # Sectie 2: Principal (Hoofdelijk Aansprakelijke)
        # ------------------------------------------------------------------
        "principal_id": "",           # EORI/ID van de Principal
        "principal_contactPersonCode": "", # Contactpersoon code van de Principal

        # ------------------------------------------------------------------
        # Sectie 3: Controlewaarden
        # ------------------------------------------------------------------
        "ControlArticles": "0",       # Totaal aantal artikelen (items)
        "ControlPackages": "0",       # Totaal aantal colli/pakketten
        "ControlGrossmass": "0.00",   # Totale Bruto Massa
        "ControlNetmass": "0.00",     # Totale Netto Massa

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
        "dialogLanguageIndicatorAtDeparture": "", # Taalcode voor dialoog
        "nctsAccompanyingDocumentLanguageCode": "", # Taalcode voor het NCTS document

        "total_items": "0",           # Totaal aantal goederenartikelen
        "total_packages": "0",        # Totaal aantal colli
        "total_grossmass": "0.00",    # Totaal bruto gewicht
        "total_nettmass": "0.00",     # Totaal netto gewicht

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
        "notValidForEC": "",         # Niet geldig voor EC (1=Ja, 0=Nee)

        "transportPlannedDate": "",   # Geplande transportdatum (YYYY-MM-DD)
        "transportPlannedTime": "",   # Geplande transporttijd (HH:MM)
        "agreedLocationOfGoods": ""   # Afgesproken locatie
    }
    return dir

def get_departure_item():
    dir = {
        # ------------------------------------------------------------------
        # Sectie 1: Basis Item Informatie
        # ------------------------------------------------------------------
        "goods_itemNumber": "",         # Artikelnummer (1, 2, 3, etc.)
        "commodityCode": "",           # Goederencode
        "goods_description": "",        # Gedetailleerde goederenomschrijving
        "goods_grossMass": "",      # Bruto massa (per item)
        "goods_netMass": "",        # Netto massa (per item)

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
        "containerNumber": "",            # Containernummer (indien van toepassing)

        # ------------------------------------------------------------------
        # Sectie 4: Packages (Colli)
        # ------------------------------------------------------------------
        "marksAndNumbersOfPackages": "",   # Merken en nummers op de verpakkingen
        "kindOfPackages": "",             # Type verpakking (Code, bv. CT voor Karton)
        "numberOfPackages": "0",          # Aantal colli
        "numberOfPieces": "0"             # Aantal stuks (indien van toepassing, bv. bij losse goederen)


    }
    return dir

def get_PLDA_header():
    dir = {
        # ------------------------------------------------------------------
        # Sectie 1: Basis Header Info (Root en CustomsStreamliner)
        # ------------------------------------------------------------------
        "dateCreation": "",           # Datum aanmaak (YYYY-MM-DD)
        "timeCreation": "",           # Tijd aanmaak (HH:MM:SS)
        "linkIdERP": "",              # Interne ERP-link ID
        
        "template": "",               # Sjabloon naam
        "company": "",                # Active company
        "status": "",                 # Dossier status (bv. Draft, Sent)
        "user": "",                   # Gebruikerscode/Naam die de aangifte aanmaakt
        "printLocation": "",          # Print locatie
        "sendDeclaration": "",        # Autosend
        "declarationId": "",          # Declaratie ID
        "procedureType": "",          # Type procedure (bv. S, D)

        # Custom placeholder voor de items, moet altijd aanwezig zijn
        "goods_items_xml": "",        # Wordt automatisch gevuld door de generate_xml methode!

        # ------------------------------------------------------------------
        # Sectie 2: Principal (Hoofdelijk Aansprakelijke/Exporteur)
        # ------------------------------------------------------------------
        "principal_operatorName": "",
        "principal_postalCode": "",
        "principal_streetAndNumber1": "",
        "principal_streetAndNumber2": "",
        "principal_city": "",
        "principal_countrySubEntity": "",
        "principal_country": "",
        "principal_id": "",           # EORI/ID van de Principal
        "principal_erpId": "",
        "principal_erpId2": "",
        "principal_contactPersonCode": "",
        "principal_contactPersonName": "",
        "principal_contactPersonEmail": "",

        # ------------------------------------------------------------------
        # Sectie 3: Supplier (Leverancier, indien van toepassing)
        # ------------------------------------------------------------------
        "supplier_country": "",
        "supplier_identifier": "",
        "supplier_operatorIdentity": "",
        "supplier_operatorName": "",
        "supplier_postalCode": "",
        "supplier_streetAndNumber1": "",
        "supplier_streetAndNumber2": "",
        "supplier_city": "",
        "supplier_countrySubEntity": "",
        "supplier_country_address": "", # Let op: gebruikt in OperatorAddress
        "supplier_id": "",
        "supplier_erpId": "",
        "supplier_erpId2": "",

        # ------------------------------------------------------------------
        # Sectie 4: Geïntegreerde Logistieke Systemen (ILS)
        # ------------------------------------------------------------------
        "createDossier": "F",
        "IlsDossier_company": "",
        "IlsDossier_departement": "",
        "IlsDossier_dossierType": "",
        "IlsDossier_subDossierType": "",
        "IlsDossier_dossierId": "",

        # ------------------------------------------------------------------
        # Sectie 5: Parties (Enkel ERP IDs)
        # ------------------------------------------------------------------
        "consignee_id": "",           # EORI/ID van de Ontvanger
        "consignee_erpId": "",
        "consignee_erpId2": "",
        "consignor_id": "",           # EORI/ID van de Verzender
        "consignor_erpId": "",
        "consignor_erpId2": "",
        "RelationImportDuties_id": "",
        "RelationImportDuties_erpId": "",
        "RelationImportDuties_erpId2": "",

        # ------------------------------------------------------------------
        # Sectie 6: Controle & Totalen (CustomsStreamliner)
        # ------------------------------------------------------------------
        "totalPrice": "0.00", 
        "totalGrossmass": "0.00",
        "totalNetmass": "0.00",
        "totalPackages": "0", 
        
        # Extra CS Velden
        "terminal": "",
        "terminalExtraDocuments": "",
        "bookingReference": "",
        "FreeText": "",
        "Amount": "0.00",
        "statisticsGroup": "",
        "DV1_type": "",
        "relationStockFiche": "",
        "relationStockFicheErpId": "",
        "relationStockFicheErpId2": "",
        
        # ------------------------------------------------------------------
        # Sectie 7: MessageBody / SADExport / GoodsDeclaration Header
        # ------------------------------------------------------------------
        "acceptanceDate": "", 
        "localReferenceNumber": "",   # LRN
        "commercialReference": "", 
        
        # Totalen (SAD Export)
        "items": "0", 
        "totalGrossmass_sad": "0.00",
        "totalNetmass_sad": "0.00",
        "packages": "0", 
        
        # Transactie Aard
        "transactionNature1": "", 
        "transactionNature2": "", 
        
        # Declarant (Aangever)
        "declarantstatus": "",
        "authorisedIdentity": "",
        "declarant_country": "",
        "declarant_identifier": "",
        "declarant_operatorIdentity": "",
        "declarant_operatorName": "",
        "declarant_postalCode": "",
        "declarant_streetAndNumber1": "",
        "declarant_city": "",
        "declarant_country_address": "",
        "declarant_contactPersonName": "", 
        "declarant_contactPersonCommunicationNumber": "", 
        "declarant_contactPersonEmail": "", 
        "declarant_contactPersonFaxNumber": "", 
        
        "issuePlace": "", 
        "typePartOne": "", 
        "typePartTwo": "", 
        
        # Consignor (Aflader/Verzender) - Gegevens
        "consignor_country": "",
        "consignor_identifier": "", 
        "consignor_operatorIdentity": "", 
        "consignor_operatorName": "", 
        "consignor_postalCode": "",
        "consignor_streetAndNumber1": "",
        "consignor_city": "",
        "consignor_country_address": "",
        
        # Consignee (Ontvanger) - Gegevens
        "consignee_operatorName": "", 
        "consignee_postalCode": "",
        "consignee_streetAndNumber1": "",
        "consignee_city": "",
        "consignee_country_address": "",
        
        # Transport
        "deliveryTerms": "", 
        "deliveryTermsPlace": "", 
        "borderMode": "", 
        "borderNationality": "", 
        "borderIdentity": "", 
        "departureIdentity": "", 
        "inlandMode": "", 
        "dispatchCountry": "", 
        
        # Douane Kantoor & Locatie
        "exitOffice": "", 
        "precise": "", 
        "validationOffice": "", 
        "loadingPlaceIdentity": "", 
        
        # Factuur
        "exchangeRate": "1.00",
        "currency": "EUR",
        "invoiceAmount": "0.00",
        
        "container": "",
        "specificCircumStance": "",
    }
    return dir

def get_PLDA_item():
    dir = {
        # Basis Item Info
        "sequence": "",              # Artikelnummer (1, 2, 3...)
        "commodityCode": "",         # HS Code / Goederencode
        "netMass": "0.00",           # Netto massa per item
        "grossMass": "0.00",         # Bruto massa per item
        "goodsDescription": "",      # Gedetailleerde goederenomschrijving

        # Verpakking
        "marksNumber": "",           # Merken en nummers
        "packages": "0",             # Aantal colli
        "packageType": "",           # Type verpakking (Code)

        # Land/Regio
        "destinationCountry": "",    # Land van bestemming
        "destinationRegion": "",
        "originCountry": "",         # Land van oorsprong
        "originRegion": "",

        # Supplementaire Eenheden
        "supplementaryUnits": "0",
        "supplementaryUnitsCode": "", # Code voor supplementaire eenheden (bv. C62)

        # Douanebehandeling
        "procedurePart1": "",        # Procedure (deel 1: 40)
        "procedurePart2": "",        # Procedure (deel 2: 00)
        "procedureType": "",         # Type procedure (bv. Y)
        
        # Entrepot (Warehouse)
        "warehouseType": "",
        "warehouseIdentity": "",
        "warehouseCountry": "",
        
        # Invoerrechten (Charges Import - vaak niet van toepassing bij export)
        "vatCharges_charges": "0.00",
        "vatCharges_currency": "EUR",
        "customsCharges_transportInsuranceCharges": "0.00",
        "customsCharges_currency": "EUR",

        # Prijs / Statistiekwaarde
        "price": "0.00",
        "price_exchangeRate": "1.00",
        "price_currency": "EUR",
        
        # Voorgaande Documenten
        "documentReference": "",     # Referentie van voorgaand document (bijv. factuur)
        "documentType": "",          # Type van voorgaand document (Code)
        "previousDocumentCategory": "",
        "previousDocumentLoc": "",
        "previousDocumentArt": "",
        "previousDocumentDate": ""
    }
    return dir