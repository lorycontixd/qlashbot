from xml.etree import ElementTree as ET
from io import StringIO

def extract_fields(message):
    string = StringIO()
    string.write("<banned>")
    string.write("<player " + message + " />")
    string.write("</banned>")
    tree = ET.fromstring(string.getvalue())

    fields_dict = tree.find('.//player')
    string.close()
    return fields_dict.attrib

fields = extract_fields(""" name="QLS | Lore" tag="#20VYYG2L" ban="40d" reason="Insults" discord="Lore#5934" """)
#{'name': 'QLS | Lore', 'tag': '#20VYYG2L', 'ban': '40d', 'reason': 'Insults', 'discord': 'Lore#5934'}
print(fields)
