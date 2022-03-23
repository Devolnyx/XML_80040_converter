import xml.etree.ElementTree as ET
import os

files = [x for x in os.listdir() if '.xml' in x]

tree = ET.parse('country_data.xml')
root = tree.getroot()

#type
xml_type = root.attrib['class']