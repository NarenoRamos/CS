import xml.sax.saxutils as saxutils
from collections import defaultdict
import os
    
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
        
