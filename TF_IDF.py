import csv
from math import log, sqrt
    
# TF(t, d) = (number of occurrences of term t in doc d) / (number of words of d)
# IDF(t) = log (N/(1+Nt)), where N is the total number of docs and Nt the number of docs containing t    

# TF[i] = dict {word : TF(word,i)} for document i
TF = []
# docs_with_word[word] = number of documents containing word 
docs_with_word = {}
# IDF = {word : IDF(word)}
IDF = {}
with open("node_information_preprocessed_abstracts_authornames.csv", "r") as f:
    reader = csv.reader(f)
    node_info  = list(reader)
    distinct_words = set()
    # TF
    for row in node_info:
        freq = {}
        words = row[5].split()
        for word in words:
            freq[word] = freq.get(word,0) + 1
        for word in freq:
            docs_with_word[word] = docs_with_word.get(word,0) + 1
        number_of_words = len(words)
        TF.append({word : freq[word]/number_of_words for word in freq})
    # IDF
    number_of_documents = len(TF)
    IDF = {word : log(number_of_documents/(1 + docs_with_word[word])) for word in docs_with_word}        

# weigth[i] = {word : weigth(word,i)} for document i
weigth = [{word : TF_dict_for_document[word]*IDF[word] for word in TF_dict_for_document} for TF_dict_for_document in TF]

##########   CALCULATE COSINE   ##############
weigth_norm_for_document = [sqrt(sum(value ** 2 for value in weigth_for_doc.values())) for weigth_for_doc in weigth]

"""
with open("TF_IDF_cosine_between_papers.csv", "w", newline='') as out:
    csv_out = csv.writer(out)
    for i in range(len(weigth)):
        if i % 100 == 0:
            print("line", i)
        to_print = []
        for j in range(len(weigth)):
            nominator = 0
            for word in weigth[i]:
                nominator += weigth[i].get(word,0) * weigth[j].get(word,0)
            for word in weigth[j]:
                if word not in weigth[i]:
                    nominator += weigth[i].get(word,0) * weigth[j].get(word,0)
            to_print.append(nominator / (weigth_norm_for_document[i] * weigth_norm_for_document[j]))
        csv_out.writerow(to_print)
"""
