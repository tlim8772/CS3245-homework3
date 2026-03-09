T ?= ~/nltk_data/corpora/reuters/training
Q ?= sanity-queries.txt

index:
	python3 index.py -i $(T) -d dictionary.txt -p postings.txt

search:
	python3 search.py -d dictionary.txt -p postings.txt -q $(Q) -o res

clean:
	rm dictionary.txt postings.txt res

submission:
	@if [ ! -f dictionary.txt ] || [ ! -f postings.txt ]; then \
		echo "Error: dictionary.txt and postings.txt must exist before creating submission zip."; \
		exit 1; \
	fi
	@rm -f A0266620H-A0272009L.zip
	@zip A0266620H-A0272009L.zip $(shell git ls-files) dictionary.txt postings.txt