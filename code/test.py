#import sys
from os import listdir
from os.path import isfile, join
import re
import numpy as np
import collections

# full articles
article_path = "../res/full-papers_txt/"
article_names = [f for f in listdir(article_path) if isfile(join(article_path, f))]
article_1 = [re.search(r"#[0-9]+", a) for a in article_names]

## a bit more funky because we cannot handle exceptions in list comp.
article_2 = []
for i in article_1: 
    try: 
        article_2.append(i.group())
    except AttributeError: 
        print(i)

# abstracts
abstract_path = "../res/abstracts_txt"
abstract_names = [f for f in listdir(abstract_path) if isfile(join(abstract_path, f))]
abstract_1 = [re.search(r"#[0-9]+", a) for a in abstract_names]
abstract_2 = [id.group() for id in abstract_1]

# any duplicates?
print([item for item, count in collections.Counter(article_2).items() if count > 1])
print([item for item, count in collections.Counter(abstract_2).items() if count > 1])

# check intersection
intersection = list(set(article_2) & set(abstract_2))
len(intersection)

# which full articles are not in abstracts & vice-versa. 
not_in_article = np.setdiff1d(article_2, abstract_2)
not_in_paper = np.setdiff1d(abstract_2, article_2)


