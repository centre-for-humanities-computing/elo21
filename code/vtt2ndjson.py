# run from: /work/dk-signal-comparison/elo21
# run this: python code/vtt2ndjson.py -i data/transcripts/ -o1 res/vtt_to_ndjson/ -o2 res/vtt_to_txt

import webvtt
import os
import ndjson
import json
from tqdm import tqdm
from pathlib import Path
import re
import argparse 

# get ndjson (& now also .txt)
def get_ndjson(filename): 
    # loop over files and append to lst. 
    ndjson_lst = []
    txt_str = ''
    for caption in webvtt.read(filename):
        
        # for the ndjson
        dct_tmp = {}
        dct_tmp["start"] = caption.start
        dct_tmp["end"] = caption.end
        split_str = caption.text.split(":", 1)
        try: 
            dct_tmp["speaker"] = split_str[0]
            dct_tmp["utterance"] = split_str[1]
        except IndexError: 
            dct_tmp["speaker"] = 'None'
            dct_tmp["utterance"] = split_str[0]
        
        ndjson_lst.append(dct_tmp)

        # for the txt (here the formats require different handling).
        if '.cc.vtt' in filename: 
            print(f'is cc: {filename}')
            txt_str += dct_tmp["utterance"]
        else: 
            try: 
                txt_str += re.findall('(?<=\:).*', dct_tmp["utterance"])[0]
            except IndexError: 
                pass 

    # convert list to ndjson
    lst_dumped = json.dumps(ndjson_lst)
    lst_loaded = json.loads(lst_dumped)

    return lst_loaded, txt_str


def main(inpath, outpath1, outpath2):
    for filename in tqdm(Path(inpath).rglob("*.vtt")):
        
        # file name 
        base = os.path.splitext(os.path.basename(filename))[0]
        ndjson_title = base + ".ndjson"
        txt_title = base + ".txt"

        # file content
        ndjson_file, txt_file = get_ndjson(os.path.join(f"{filename}"))
        
        # write ndjson file
        with open(os.path.join(outpath1, ndjson_title), "w") as f:
            ndjson.dump(ndjson_file, f)

        # write txt file 
        with open(os.path.join(outpath2, txt_title), "w") as f: 
            f.write(txt_file)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inpath", required=True, type=str, help="path to folder with input files")
    ap.add_argument("-o1", "--outpath1", required=True, type=str, help='path to folder for ndjson')
    ap.add_argument("-o2", "--outpath2", required=True, type=str, help='path to folder for txt')
    args = vars(ap.parse_args())

    main(inpath = args['inpath'], outpath1 = args['outpath1'], outpath2 = args['outpath2'])
