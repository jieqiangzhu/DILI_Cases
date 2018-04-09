# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 16:19:15 2018

@author: Jieqiang.Zhu
"""
import pandas as pd
import numpy as np
import requests
import time
from lxml import etree

pmids = pd.read_csv('PMIDs.csv')

def get_pubmed_record(url):
    content = requests.get(url).content
    tree = etree.fromstring(content)
    id = tree.xpath("//MedlineCitation/PMID[@Version='1']")
    title = tree.xpath("//Article/ArticleTitle")
    year = tree.xpath("//PubMedPubDate[@PubStatus='pubmed']/Year")
    abstract = tree.xpath("//Abstract/AbstractText")
    language = tree.xpath("//Language")
    affiliation = tree.xpath("//Affiliation")
    
    record = pd.DataFrame(np.empty((1,6)),columns = ['PMID','Title','Year','Abstract','Language','Affiliation'])
    record['PMID'] = id[0].text
    record['Title'] = title[0].text
    record['Year'] = year[0].text
    record['Abstract'] = 'NA' if len(abstract)==0 else abstract[0].text
    record['Language'] = 'NA' if len(language)==0 else language[0].text
    record['Affiliation'] = 'NA' if len(affiliation)==0 else affiliation[0].text

    return record

whole_records = pd.DataFrame(np.zeros((1,6)),columns = ['PMID','Title','Year','Abstract','Language','Affiliation'])

#for each in drug_pages['URL']:
for each in pmids['PMID']:
    pubmed_url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&retmode=xml&id="+str(each)
    
    new_record = get_pubmed_record(pubmed_url)
    whole_records = pd.concat([whole_records,new_record])
    print('The current number is {}, and {}% have been finished'.format(each,each/len(pmids)*100))
    time.sleep(10)
    
whole_records.to_csv('pubmed_records.csv')
