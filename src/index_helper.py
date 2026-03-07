import os
import nltk
from pathlib import Path
from collections import Counter
import itertools
import math
import pickle

# doc_lens: maps file name to the vector length
# doc_freqs: maps word to document frequency
# get total number of documents from doc_freqs
def index_helper(in_dir: str, out_dict: str, out_postings: str):
    doc_lens: dict[int, float] = {}
    doc_freqs: Counter[str] = Counter()
    postings: dict[str, list[tuple[int,float]]] = {}
    stemmer = nltk.stem.PorterStemmer()

    for path in Path(in_dir).iterdir():
        if not path.is_file() or not path.name.isdigit():
            continue
        
        with path.open('r') as f:
            doc_id = int(path.name)
            counter: Counter[str] = Counter()
            text = f.read()
            sentences = nltk.sent_tokenize(text)
            words = itertools.chain.from_iterable(map(lambda sentence: nltk.word_tokenize(sentence), sentences))
            tokens = map(lambda word: stemmer.stem(word, to_lowercase=True), words)
            for token in tokens:
                counter[token] += 1
            
            sum = 0.0
            for word, freq in counter.items():
                doc_freqs[word] += 1
                w = 1 + math.log10(freq)
                sum += w**2
                if word not in postings:
                    postings[word] = []
                postings[word].append((doc_id, w))
            doc_lens[doc_id] = math.sqrt(sum)

    with open(out_dict, 'wb') as dict_f, open(out_postings, 'wb') as postings_f:
        pickle.dump(doc_lens, dict_f)
        pickle.dump(doc_freqs, dict_f)
        
        offset_dict: dict[str, int] = {}
        offset = 0
        for word, posting_list in postings.items():
            byte_obj = pickle.dumps(posting_list)
            postings_f.write(byte_obj)
            offset_dict[word] = offset
            offset += len(byte_obj)
        pickle.dump(offset_dict, dict_f) 


        

