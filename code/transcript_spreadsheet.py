## how to run ##
# be in elo21 folder and type:  
# python code/transcript_spreadsheet.py -i data/transcripts/ -o res/meta_csv/

# packages
import webvtt
import os
import ndjson
import json
from tqdm import tqdm
from pathlib import Path
import re
import argparse 
import pandas as pd

###### .transcript.vtt #######

def get_pandas(filename, base): 

    # prepare df 
    column_names = ['speaker', 'text', 'transcripts-id']
    df = pd.DataFrame(columns = column_names)

    # loop over .transcripts.vtt (gives None in speaker)
    filename = "/work/dk-signal-comparison/elo21/data/transcripts/Friday_28th_May_2021/1100-1215_TRACK1/Platform_possibilities_and_beyond/GMT20210528-105935_Recording.transcript.vtt"
    for caption in webvtt.read(filename): 

        # for the txt (here the formats require different handling).
        split_str = caption.text.split(":", 1)
        try: 
            speaker = split_str[0]
            text = split_str[1]
        except IndexError: 
            speaker = 'None'
            text = split_str[0]
        
        # append to csv
        df = df.append({'speaker': speaker, 'text': text, 'transcripts-id': base}, ignore_index = True)
    
    return df 


def main(inpath, outpath):

    column_names = ['speaker', 'text', 'transcripts-id']
    df = pd.DataFrame(columns = column_names)

    for filename in tqdm(Path(inpath).rglob("*.transcript.vtt")):
        
        # file name 
        base = os.path.splitext(os.path.basename(filename))[0]
        id = re.findall("(\d+-\d+)", base)[0]

        # file content
        df_tmp = get_pandas(filename, id)
        
        # append master df 
        df = df.append(df_tmp, ignore_index = True)
    
    df.to_csv(f"{outpath}/transcripts.csv", index=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inpath", required=True, type=str, help="path to folder with input files")
    ap.add_argument("-o", "--outpath", required=True, type=str, help='path to folder for output csv')
    args = vars(ap.parse_args())

    main(inpath = args['inpath'], outpath = args['outpath'])