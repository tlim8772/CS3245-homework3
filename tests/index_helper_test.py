import unittest
from src.index_helper import *
import shutil

def create_in_dir(in_dir):
    if os.path.exists(in_dir):
        shutil.rmtree(in_dir)
    os.makedirs(in_dir)
    for i in range(4):
        with open(f'{in_dir}/{i}', 'w') as f:
            f.write('a b c')

class Test(unittest.TestCase):
    def test_index_helper(self):
        in_dir = 'test_dir'
        out_dict = 'out_dict'
        out_postings = 'out_postings'
        create_in_dir(in_dir)
        index_helper(in_dir, out_dict, out_postings)

        with open(out_dict, 'rb') as d, open(out_postings, 'rb') as p:
            doc_lens = pickle.load(d)
            doc_freqs = pickle.load(d)
            doc_offsets = pickle.load(d)
            self.assertEqual(doc_lens, {0: math.sqrt(3), 1:math.sqrt(3), 2:math.sqrt(3), 3: math.sqrt(3)})
            self.assertEqual(doc_freqs, {'a': 4, 'b': 4, 'c': 4})

            offset = doc_offsets['b']
            p.seek(offset)
            lst = pickle.load(p)
            self.assertEqual(set(lst), set([(0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0)]))

        shutil.rmtree(in_dir)
        os.remove(out_dict)
        os.remove(out_postings)
