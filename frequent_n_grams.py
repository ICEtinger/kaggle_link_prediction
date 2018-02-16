import csv

#with open("node_information.csv", "r") as f:
with open("node_information_preprocessed_abstracts.csv", "r") as f:
    reader = csv.reader(f)
    node_info  = list(reader)

    """
    # for BIGRAMS
    freq = {}
    for line in node_info:
        # line[5] = abstract
        words = line[5].split()
        for i in range (len(words) - 1):
            ngram = words[i] + "_" + words[i+1]
            if ngram in freq:
                freq[ngram] += 1
            else:
                freq[ngram] = 1
    
    """
    
    """
    # for TRIGRAMS            
    freq = {}
    for line in node_info:
        # line[5] = abstract
        words = line[5].split()
        for i in range (len(words) - 2):
            ngram = words[i] + "_" + words[i+1] + "_" + words[i+2]
            if ngram in freq:
                freq[ngram] += 1
            else:
                freq[ngram] = 1
    """
    
    # for QUADRIGRAMS            
    freq = {}
    for line in node_info:
        # line[5] = abstract
        words = line[5].split()
        for i in range (len(words) - 3):
            ngram = words[i] + "_" + words[i+1] + "_" + words[i+2] + "_" + words[i+3]
            if ngram in freq:
                freq[ngram] += 1
            else:
                freq[ngram] = 1
####################    
    
    freq_list = [(freq[key],key) for key in freq]
    freq_list.sort(reverse=True)
    for i in range(100):
        print(freq_list[i])
    