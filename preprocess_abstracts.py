import csv

with open("node_information.csv", "r") as f:
    reader = csv.reader(f)
    node_info  = list(reader)
    
    stopwords = {"we", "can", "not", "can't", "cant", "but", "this", "that", "these",
                 "those", "and", "or", "also", "as", "a", "an", "of", "one", "two",
                 "three", "four", "at", "on", "to", "so", 
                 "on", "for", "from", "the", "then", "than", "in", "out", "where", "when", 
                 "what", "which", "is", "be", "are", "been", "would", "will", "was", "should", 
                 "has", "have", "had", "by", "with",
                 "thus", "therefore", "because", "due", "show", "know", "find", "study",
                 "consider", "discuss", "particular", "general", "shown", "theory", "theories",
                 "experiment", "experiments", "analysis", "new", "old", "present", "classical", 
                 "well", "give", "gives", "given", "our", "such", "some", "each", "case"}
    with open("node_information_preprocessed_abstracts.csv", "w", newline='') as out:
        csv_out = csv.writer(out)
        for row in node_info:
            preprocessed_abstract = ""
            for word in row[5].split():
                if word not in stopwords:
                    preprocessed_abstract += (word+" ")
            csv_out.writerow([row[0], row[1], row[2], row[3], row[4], preprocessed_abstract])