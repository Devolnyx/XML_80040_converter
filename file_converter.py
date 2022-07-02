import xml.etree.ElementTree as ET
import os
import datetime
from dateutil.relativedelta import relativedelta
import logging

logging.basicConfig(filename='logs.log',
                    filemode='a',
                    level=logging.INFO,
                    format='[%(asctime)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(' ')

#get month of previous period
folder = (datetime.datetime.now() - relativedelta(months=1))
period = folder.strftime('%Y''%m')
folder = folder.strftime('%Y''_%m')

#check if folder for current month is exists
if os.path.exists(folder):
    logger.info(f'Папка "{folder}" уже существует')
    pass
else:
    os.mkdir(folder)
    logger.info(f'Папка "{folder}" создана')


def parse_xml(folder, file):
    tree = ET.parse(file)
    root = tree.getroot()
    try:
        root.attrib['class'] = '80040'

        name = file.replace('80020', '80040')
        tree.write(os.path.join(folder, name), encoding="UTF-8", xml_declaration=True)
    except:
        pass


files = [x for x in os.listdir() if x.endswith('.xml')]

if len(files) >0:
    logger.info(f'Найдено {len(files)} отчетов XML80020 в корневой директории')
    n = 0
    w = 0
    skip = []
    for file in files:
        #check if period in filename, etc. 202203 in 80040_3525337803_20220322_0_1000
        if period in file:
            parse_xml(folder, file)
            os.remove(file)
            n+=1
        else:
            w+=1
            skip.append(file)

    logger.info(f'Всего обработано {n} отчетов')
    if w!=0:
        logger.info(f'Пропущено {w} отчетов, не относящихся к рассматриваемому периоду {folder}')

else:
    logger.info('Файлы отчетов XML в корневой директории не найдены')
