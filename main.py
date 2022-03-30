import xml.etree.ElementTree as ET
from zipfile import ZipFile
import os
from os.path import basename
import tempfile

def close_tmp_file(tf):
    try:
        os.unlink(tf.name)
        tf.close()
    except:
        pass

def parse_xml(contents):

    tree = ET.parse(contents)
    root = tree.getroot()

    try:
        root.attrib['class'] = '80040'
    except:
        pass

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xml')
    tree.write(temp_file.name)

    return temp_file


def do_zip(contents, names):

    with ZipFile('reports.zip', 'w') as zipObj:
       # Iterate over all the files in directory
       for c, n in zip(contents, names):
           temp_file = parse_xml(n)

           zipObj.write(temp_file.name, arcname=f'{n}')
           close_tmp_file(temp_file)


