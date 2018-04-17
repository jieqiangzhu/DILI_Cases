# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 09:02:08 2018

@author: Jieqiang.Zhu
"""
import requests
import string
import time
import csv
from lxml import etree

def get_drug_list(url):
    content = requests.get(url).content
    html = etree.HTML(content)
    result_name = html.xpath('//h3/ol/li/a/text()')
    result_url = html.xpath('//h3/ol/li/a/@href')
    result = dict(zip(result_name,result_url))
    return result

urls = []
for alphabet in string.ascii_uppercase:
	urls.append('https://livertox.nih.gov/php/searchchem.php?chemrang='+alphabet)

drug_pages = {}

for each in urls:
    drug_pages.update(get_drug_list(each))
    time.sleep(20)

with open('drug_pages.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in drug_pages.items():
       writer.writerow([key, value])
