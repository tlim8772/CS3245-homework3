import unittest
import os
import shutil
from src.index_helper import index_helper
from src.query import *

def create_in_dir(in_dir):
    if os.path.exists(in_dir):
        shutil.rmtree(in_dir)
    os.makedirs(in_dir)
    for i in range(4):
        with open(f'{in_dir}/{i}', 'w') as f:
            f.write('a b c')

class Test(unittest.TestCase):
    def test_get_from_dictionary_file_and_posting_file(self):
        in_dir = 'test_dir'
        out_dict = 'out_dict'
        out_postings = 'out_postings'
        create_in_dir(in_dir)
        index_helper(in_dir, out_dict, out_postings)

        doc_lens, doc_freqs, offset_dict = get_doclens_docfreqs_offsetdict(out_dict)
        self.assertEqual(doc_lens, {0: math.sqrt(3), 1: math.sqrt(3), 2: math.sqrt(3), 3: math.sqrt(3)})
        self.assertEqual(doc_freqs, {'a': 4, 'b': 4, 'c': 4})

        with open(out_postings, 'rb') as pf:
            lst = get_posting_list('c', offset_dict, pf)
            self.assertEqual(set(lst), set([(0, 1), (1, 1), (2, 1), (3, 1)]))

        os.remove(out_dict)
        os.remove(out_postings)
        shutil.rmtree(in_dir)

