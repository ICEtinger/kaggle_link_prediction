import pandas as pd

from numpy import loadtxt
#from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import csv
from math import log, sqrt

training_set = pd.read_csv('training_set.txt', sep=' ', header=None)
training_set.columns=['citing_paper_ID', 'cited_paper_ID', 'has_citation']

test_set = pd.read_csv('testing_set.txt', sep=' ', header=None)
test_set.columns=['citing_paper_ID', 'cited_paper_ID']

node_info = pd.read_csv('node_information_preprocessed_abstracts_authornames.csv', header=None)
node_info.columns=['id', 'year', 'title', 'authors', 'journal', 'abstract']

########### starts building features ##############3

joined = pd.merge(pd.merge(training_set, node_info, left_on='citing_paper_ID', right_on='id'),
                  node_info, left_on='cited_paper_ID', right_on='id', suffixes=['_citing','_cited'])

print('started calculating year_diff')
year_diff = []
for index, row in joined.loc[:,['year_citing', 'year_cited']].iterrows():
    year_diff.append(row[1] - row[0])
feature_year_diff = pd.DataFrame(data={'year_diff':year_diff})


print('started calculating authors')
num_authors_citing = []
num_authors_cited = []
num_overlapping_authors = []
for index, row in joined.loc[:,['authors_citing', 'authors_cited']].iterrows():
    authors_citing = row[0].split() 
    authors_cited = row[1].split()
    num_authors_citing.append(len(authors_citing))
    num_authors_cited.append(len(authors_cited))
    count = 0
    for i in authors_citing:
        for j in authors_cited:
            if i == j:
                count += 1
    num_overlapping_authors.append(count)
feature_num_authors_citing = pd.DataFrame(data={'num_authors_citing':num_authors_citing})
feature_num_authors_cited = pd.DataFrame(data={'num_authors_cited':num_authors_cited})
feature_num_overlapping_authors = pd.DataFrame(data={'num_overlapping_authors':num_overlapping_authors})


print('started calculating journals')
known_journal_citing = []
known_journal_cited = []
same_journal = []
for index, row in joined.loc[:,['journal_citing', 'journal_cited']].iterrows():
    bool_known_journal_citing = type(row[0]) is str and len(row[0]) != 0
    bool_known_journal_cited = type(row[0]) is str and len(row[0]) != 0
    known_journal_citing.append(bool_known_journal_citing)
    known_journal_cited.append(bool_known_journal_cited)
    same_journal.append(known_journal_citing and row[0] == row[1])
feature_known_journal_citing = pd.DataFrame(data={'known_journal_citing':known_journal_citing})
feature_known_journal_cited = pd.DataFrame(data={'known_journal_cited':known_journal_cited})
feature_same_journal = pd.DataFrame(data={'same_journal':same_journal})


print('started calculating TF-IDF')
# TF(t, d) = (number of occurrences of term t in doc d) / (number of words of d)
# IDF(t) = log (N/(1+Nt)), where N is the total number of docs and Nt the number of docs containing t    
# TF[id] = dict {word : TF(word,id)} for document of identifier 'id'
TF = {}
# docs_with_word[word] = number of documents containing word 
docs_with_word = {}
# IDF = {word : IDF(word)}
IDF = {}
# TF
for index, row in joined.loc[:,['id', 'abstract']].iterrows():
    freq = {}
    words = row[1].split()
    for word in words:
        freq[word] = freq.get(word,0) + 1
    for word in freq:
        docs_with_word[word] = docs_with_word.get(word,0) + 1
    number_of_words = len(words)
    TF[row[0]] = {word : freq[word]/number_of_words for word in freq}
# IDF
number_of_documents = len(TF)
IDF = {word : log(number_of_documents/(1 + docs_with_word[word])) for word in docs_with_word}            
# weigth[id] = {word : weigth(word,id)} for document of identifier 'id'
weigth = {ID : {word : TF_dict_for_word*IDF[word] for word,TF_dict_for_word in TF_dict_for_doc.items()} for ID,TF_dict_for_doc in TF.items()}
# now calculates the cosine for each pair of documents in the training set
cosine = []
weigth_norm_for_document = {ID : sqrt(sum(value ** 2 for value in weigth_for_doc.values())) for ID,weigth_for_doc in weigth.items()}
for index, (i,j) in joined.loc[:,['citing_paper_ID', 'cited_paper_ID']].iterrows():
    nominator = 0
    for word in weigth[i]:
        nominator += weigth[i].get(word,0) * weigth[j].get(word,0)
    for word in weigth[j]:
        if word not in weigth[i]:
            nominator += weigth[i].get(word,0) * weigth[j].get(word,0)
    cosine.append(nominator / (weigth_norm_for_document[i] * weigth_norm_for_document[j]))
feature_cosine = pd.DataFrame(data={'cosine':cosine})


features = pd.concat([
        joined['has_citation'],
        joined['year_citing'],
        feature_year_diff, 
        feature_num_authors_citing, 
        feature_num_authors_cited,
        feature_num_overlapping_authors,
        feature_known_journal_citing,
        feature_known_journal_cited,
        feature_same_journal,
        feature_cosine
        ], axis=1)

citation = ...

         
  
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)