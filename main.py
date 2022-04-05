import xml.etree.ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED
import os

import tempfile
import base64


def close_tmp_file(tf):

    try:
        os.unlink(tf.name)
        tf.close()
    except:
        pass


def parse_xml(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    tree = ET.ElementTree(ET.fromstring(decoded))
    #tree = ET.parse(contents)
    root = tree.getroot()

    try:
        root.attrib['class'] = '80040'
    except:
        pass

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xml')
    tree.write(temp_file.name)

    return temp_file


def do_zip(names):

    zip_tf = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    zf = ZipFile(zip_tf, mode='w', compression=ZIP_DEFLATED)

    for (n, c) in names:
        temp_file = parse_xml(c)
        name = n.replace('80020', '80040')
        zf.write(temp_file.name, f"{name}")

        temp_file.flush()
        close_tmp_file(temp_file)

    zf.close()
    return zip_tf


