import os
import glob
import itertools

import ndjson
from multiprocessing import Manager, Pool
import gensim


def extract_meta(gen):
    """
    returns a generator which yield only the text
    """
    for i in gen:
        yield i['fname'], i['index']


def extract_text(gen):
    """
    returns a generator which yield only the text
    """
    for i in gen:
        yield i['text']


def chunk(iterable, size=10):
    """
    chunks a generator function into chunks of specific size and return the as a list
    """
    iterator = iter(iterable)
    for first in iterator:
        yield list(itertools.chain([first], itertools.islice(iterator, size - 1)))


def load_spacy():
    nlp = spacy.load('da_core_news_lg', disable=['textcat'])
    return nlp


def lemmatize_file(path, nlp, outdir):
    '''
    Parallelize this
    '''
    with open(path) as f:
        reader = ndjson.reader(f)
        reader = extract_text(reader)
        meta = extract_meta(reader)

        docs = nlp.pipe(reader)

        spacy_tokens = []
        for doc in docs:
            doc_features = {}
            doc_features.update({
                'text': [token.text for token in doc],
                'lemma': [token.lemma_ for token in doc],
                'pos': [token.pos_ for token in doc],
                'dep': [token.dep_ for token in doc],
                'ner': [token.ent_type_ for token in doc]
                })
            spacy_tokens.append(doc_features)

        del docs
    
    outfname = os.path.basename(path)
    with open(os.path.join(outdir, outfname), 'w') as fout:
        ndjson.dump(spacy_tokens, fout)
    
    return None


def main(paths, nlp, outdir):
    for file in paths:
        print('processing {}'.format(file))
        lemmatize_file(file, nlp, outdir)


if __name__ == "__main__":
    import glob
    sub_paths = parsed_subs = glob.glob('../data/Subtitles_parsed/*.ndjson')
    nlp = load_spacy()
    outdir = '../data/Subtitles_lemma_test/'
    main(sub_paths, nlp, outdir)