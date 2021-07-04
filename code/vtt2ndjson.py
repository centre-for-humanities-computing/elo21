import webvtt
import os
import ndjson
import json
from tqdm import tqdm
from pathlib import Path
import re
import argparse 

### testing on vtt transcripts

# load  file and create dictionary 
# potential issue: same speaker cut up. 
# nb: we need the filename as well. 

def get_transcripts(filename): 
    # loop over files and append to lst. 
    lst = []
    for caption in webvtt.read(filename):
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
        lst.append(dct_tmp)

    # convert list to ndjson
    lst_dumped = json.dumps(lst)
    lst_loaded = json.loads(lst_dumped)
    #lst_ndjson = ndjson.dumps(lst_loaded)

    return lst_loaded
    

def main(inpath, outpath):
    for filename in tqdm(Path(inpath).rglob("*.vtt")):
        
        # file name 
        base = os.path.splitext(os.path.basename(filename))[0]
        full_title = base + ".vtt" + ".ndjson"

        # file content
        file = get_transcripts(os.path.join(f"{filename}"))
        
        # write file 
        with open(os.path.join(outpath, full_title), "w") as f:
            ndjson.dump(file, f)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inpath", required=True, type=str, help="path to folder with input files")
    ap.add_argument("-o", "--outpath", required=True, type=str, help='path to folder for saving output files')
    args = vars(ap.parse_args())

    main(inpath = args['inpath'], outpath = args['outpath'])
