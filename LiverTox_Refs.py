import requests
import pandas as pd
import numpy as np
import random
from lxml import etree

def get_ref_record(url):
    content = requests.get(url).content
    html = etree.HTML(content)

    refs = html.xpath('//ol[1]/li/h3')
    ref_num = len(refs)
    result_ref = ['NA']*ref_num
    result_pubmed = ['NA']*ref_num
    result_comment = ['NA']*ref_num

    for i in range(ref_num):
        ref_loc = '//ol[1]/li['+str(i+1)+']/h3[1]/text()'
        pubmed_loc = '//ol[1]/li['+str(i+1)+']/h3[1]/a[1]/@href'
        comment_loc = '//ol[1]/li['+str(i+1)+']/h3[1]/em[1]/text()'
        if len(html.xpath(ref_loc))>=1:
            result_ref[i] = html.xpath(ref_loc)[0]
        if len(html.xpath(pubmed_loc))>=1:    
            result_pubmed[i] = html.xpath(pubmed_loc)[0]
        if len(html.xpath(comment_loc))>=1:
            result_comment[i] = html.xpath(comment_loc)[0]
    
    record = pd.DataFrame(np.zeros((ref_num,4)),columns = ['Drug','Ref','Pubmed','Comment'])
    record['Drug'] = url
    record['Ref'] = result_ref
    record['Pubmed'] = result_pubmed   
    record['Comment'] = result_comment

    return record
