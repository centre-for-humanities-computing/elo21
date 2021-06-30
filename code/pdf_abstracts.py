#import sys
import os
import argparse 
from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io
import re
import pandas as pd

# from pdf2txt.py
def pdfparser(data):

    fp = open(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams) #codec=codec
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()

    return data

# write abstract .txt files. 
def write_txt(id, content): 
    f = open(f"../res/abstracts_txt/{id}_abstract.txt", "w+")
    f.write(content)
    f.close()

# pdf parse
all_abstracts = pdfparser('../data/ELO_2021_-_Abstracts (1).pdf')

# split on ID.
all_articles = re.split(r'#[0-9]+', all_abstracts)
all_idx = re.findall(r'(#[0-9]+)', all_abstracts)
    
# take out only the actual papers. 
actual_articles = [paper for paper in all_articles if len(paper) > 500]
actual_length = len(actual_articles)
actual_ids = all_idx[-actual_length:]

# prepare dataframe 
column_names = ['ID', 'authors', 'title']
df = pd.DataFrame(columns = column_names)

# loop over them 
for i in range(len(actual_ids)): 
    
    # get author, title and abstract
    capture = re.match(r'(.+)(?:Title)(.+)(?:Abstract)(.+)', actual_articles[i], re.DOTALL)
    authors = capture.groups()[0].strip()
    title = capture.groups()[1]
    abstract = capture.groups()[2]

    # get ID 
    id = actual_ids[i]

    # add to dataframe
    df = df.append({'ID': id, 'authors': authors, 'title': title}, ignore_index = True)

    # write txt
    write_txt(id, abstract)

# write data frame 
df.to_csv("../res/meta_csv/titles.csv", index = False)
