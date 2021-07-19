# run from: /work/dk-signal-comparison/elo21
# run this: python code/clean_vtt.py -i res/vtt_to_txt/ -o res/vtt_txt_clean/

# NB: has issues with "I'm" & stuff like this. 

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import spacy
nlp = spacy.load("en_core_web_sm")
from tqdm import tqdm
import os
import argparse 
from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io

# modified something that Jan found in the archives. 
class TextFeatures:
    """ Class for extracting lexical features from text  
    Input:
        text: str variable
    """
    def __init__(self, text):
        assert isinstance(text, str), "'text' must have type str."
        self.text = text
        self.cleaned_text = TextFeatures.normalizing_text(self.text)
        self.tokens = [token for token in self.cleaned_text.split() if token not in stopwords.words('english')] #without stopwords
        self.tokenized = nlp(' '.join(self.tokens))
        self.lemmas = [token.lemma_ for token in self.tokenized]
        self.lemmatized = ' '.join(self.lemmas)
        self.n_tokens = len(self.tokens)    
    
    @staticmethod
    def normalizing_text(text):
        #normalising (make lower, remove punctuation, fix abbreviations, etc.)
        text = text.lower() #lower case
        #text = re.sub(r"_", " ", text) #replace underscore with space
        #text = re.sub(r'[^\w\s]', "", text) #remove punctuation and emojis
        #text = re.sub(r'abstracts', "", text) #remove "abstracts"
        text = re.sub(r'\d+', ' ', text)
        text = re.sub(r'\W+', ' ', text)
        text = re.sub(r'\s+', ' ', text) # excess whitespace with single :) 
        return text    

# function to load file 
def load_file(filename):
    with open(filename) as f:
        lines = f.read().replace('\n', ' ') 
        return lines

# def main
def main(inpath, outpath):
    for filename in tqdm(Path(inpath).glob("*.txt")):

        # read the file 
        paper_tmp = load_file(filename)
        paper_instance = TextFeatures(paper_tmp)
        clean_tmp = paper_instance.cleaned_text

        # make sure that files are non-empty
        if len(clean_tmp) > 20:
        
            # change the filename
            base=os.path.splitext(os.path.basename(filename))[0] + ".txt"

            # save 
            with open(os.path.join(outpath, base), "w") as text_file:
                text_file.write(clean_tmp)
        
        else: 
            pass

# run main
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inpath", required=True, type=str, help="path to folder with input files (pdfs)")
    ap.add_argument("-o", "--outpath", required=True, type=str, help='path to folder for saving output files')
    args = vars(ap.parse_args())

    main(inpath = args['inpath'], outpath = args['outpath'])