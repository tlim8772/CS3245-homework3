This is the README file for A0266620H-A0272009L's submission<br>
Email: e1091280@u.nus.edu, e1121412@u.nus.edu

== Python Version ==

We're using Python Version 3.12.3 or replace version number> for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.


We iterate through each document and then iterate through all the tokens to build the dictionary and the posting list. The dictionary consists of 3 objects, the document len which contains the length of the vector of the document, the document frequency which contains the document frequency of each token and the offset dictionary which contains the offset to the posting list for each token. The posting list is a list of (docID, 1 + log(frequency of token in that doc)).

When processing a query, we get frequency of each token in the query. Then we get the document frequency of that token. Then we retrieve the posting list of that token, and for each document in that posting list we multiply with 1 + log(freq of token in that document) to build the score of each document. After processing all the tokens, we divide the documents score by the length of document vector (length of query vector ignored as it is the same for all document scores).

After we have the score for each document (documents which do not share a common token with the query ignored), we use heapq to get the 10 largest.

== Files included with this submission ==

`src/index_helper.py`: builds `dictionary.txt` and `postings.txt`.<br>
`src/query.py`: evaluates the query<br>

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[X] We, A0266620H and A0272009L, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Gilligan's Island Rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
