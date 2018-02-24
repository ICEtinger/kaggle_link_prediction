import csv

with open("node_information.csv", "r") as f:
    reader = csv.reader(f)
    node_info  = list(reader)
    
    stopwords = {"we", "can", "not", "can't", "cant", "but", "thi", "that", "these",
                 "those", "and", "or", "also", "a", "an", "of", "one", "two",
                 "three", "four", "at", "on", "to", "so", 
                 "on", "for", "from", "the", "then", "than", "in", "out", "where", "when", 
                 "what", "which", "i", "be", "are", "were", "been", "would", "will", "wa",
                 "should", "could", "would", "ha", "have", "had", "by", "with",
                 "thu", "therefore", "because", "due", "show", "know", "find", "study",
                 "consider", "discus", "particular", "general", "shown", "theory", "theorie",
                 "experiment", "analysi", "new", "old", "present", "classical", 
                 "well", "give", "given", "our", "such", "some", "each", "case"}
    with open("node_information_preprocessed_abstracts.csv", "w", newline='') as out:
        csv_out = csv.writer(out)
        for row in node_info:
            plural_to_singular = row[5].replace("s ", " ")
            preprocessed_abstract = ""
            for word in plural_to_singular.split():
                if word not in stopwords:
                    preprocessed_abstract += (word+" ")
            csv_out.writerow([row[0], row[1], row[2], row[3], row[4], preprocessed_abstract])