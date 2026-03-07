T ?= ~/nltk_data/corpora/reuters/training
Q ?= sanity-queries.txt

index:
	python3 index.py -i $(T) -d dictionary.txt -p postings.txt

search:
	python3 search.py -d dictionary.txt -p postings.txt -q $(Q) -o res

clean:
	rm dictionary.txt postings.txt res