{
    # ------------------------------------------------------------------
    # Sectie 1: Basis Header Info (Root en CustomsStreamliner)
    # ------------------------------------------------------------------
    "dateCreation": "",           # Datum aanmaak (YYYY-MM-DD)
    "timeCreation": "",           # Tijd aanmaak (HH:MM:SS)
    "template": "",               # Sjabloon naam
    "company": "",                # Bedrijfsnaam
    "messageStatus": "New",       # Status van het bericht (bv. New, Update)
    "status": "Draft",            # Dossier status (bv. Draft, Sent)
    "LRN": "",                    # Local Reference Number (Uniek per aangifte)
    "user": "",                   # Gebruikerscode/Naam die de aangifte aanmaakt
    "printLocation": "",          # Print locatie
    "createDeclaration": "Y",     # Declaratie aanmaken (Y/N)
    "sendDeclaration": "Y",       # Declaratie verzenden (Y/N)
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
    "dialogLanguageIndicatorAtDeparture": "NL", # Taalcode voor dialoog
    "nctsAccompanyingDocumentLanguageCode": "NL", # Taalcode voor het NCTS document

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
    "notValidForEC": "0",         # Niet geldig voor EC (1=Ja, 0=Nee)

    "transportPlannedDate": "",   # Geplande transportdatum (YYYY-MM-DD)
    "transportPlannedTime": ""    # Geplande transporttijd (HH:MM)
}