import pickle
from typing import IO
import nltk
import math
from collections import Counter
import heapq

def get_doclens_docfreqs_offsetdict(out_dict: str) -> tuple[dict[int, int], dict[str, int], dict[str, int]]:
    with open(out_dict, 'rb') as f:
        doc_lens = pickle.load(f)
        doc_freqs = pickle.load(f)
        offset_dict = pickle.load(f)
    return doc_lens, doc_freqs, offset_dict

def get_posting_list(token, offset_dict: dict[str, int], posting_file: IO[bytes]) -> list[tuple[int, float]]:
    if token not in offset_dict:
        return []
    offset = offset_dict[token]
    posting_file.seek(offset)
    return pickle.load(posting_file)

def eval(query: str, doc_len: dict[int, int], doc_freqs: dict[str, int], offset_dict: dict[str, int], posting_file: IO[bytes]) -> list[int]:
    docN = len(doc_len)
    stemmer = nltk.stem.PorterStemmer()
    doc_res: dict[int, float] = {}
    tokens = list(map(lambda word: stemmer.stem(word, to_lowercase=True), nltk.word_tokenize(query)))
    counter = Counter(tokens)
    query_vector_len = 0.0
    
    for token in tokens:
        # skip tokens that are not in any documents
        if token not in doc_freqs:
            continue
        
        w_query = (1 + math.log10(counter[token])) * math.log10(docN / doc_freqs[token])
        query_vector_len += math.pow(w_query, 2)

        posting_list = get_posting_list(token, offset_dict, posting_file)
        for doc, w in posting_list:
            if doc not in doc_res:
                doc_res[doc] = 0.0
            doc_res[doc] += w_query * w
    
    query_vector_len = math.sqrt(query_vector_len)
    
    for doc in doc_res.keys():
        doc_res[doc] /= (query_vector_len * doc_len[doc])

    result = heapq.nlargest(10, doc_res.items(), key=lambda pair: (pair[1], -pair[0]))
    result = list(map(lambda pair: pair[0], result))
    
    return result



