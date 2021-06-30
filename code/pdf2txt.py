#import sys
import os
import argparse 
from pathlib import Path
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
import io

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


def main(inpath, outpath):
    for filename in Path(inpath).glob("*.pdf"):

        base=os.path.splitext(os.path.basename(filename))[0]

        text = pdfparser(os.path.join(f"{filename}"))

        with open(os.path.join(outpath, f"{base}.txt"), "w") as text_file:
            text_file.write(text)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--inpath", required=True, type=str, help="path to folder with input files (pdfs)")
    ap.add_argument("-o", "--outpath", required=True, type=str, help='path to folder for saving output files')
    args = vars(ap.parse_args())

    main(inpath = args['inpath'], outpath = args['outpath'])