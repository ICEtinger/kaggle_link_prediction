import csv

translation_table = dict.fromkeys(map(ord, '!@#$.,\'\"~/\\][{}?-_'), None)

with open("node_information_preprocessed_abstracts.csv", "r") as f:
    reader = csv.reader(f)
    node_info  = list(reader)
    
    with open("node_information_preprocessed_abstracts_authornames.csv", "w", newline='') as out:
        csv_out = csv.writer(out)
        for row in node_info:
            authors_full_names = row[3].split(",")
            preprocessed_author = ""
            for full_name in authors_full_names:
                # remove everything after an '(', if there is any
                f = full_name.find("(")
                if f >= 0:
                    full_name = full_name[:f]
                # remove punctuation chars
                clean = full_name.translate(translation_table)
                # register author as first letter of first name + full last name.
                first_last_names = clean.split()
                if len(first_last_names) > 0 and len :
                    if preprocessed_author != "":
                        preprocessed_author += ","
                    preprocessed_author += (first_last_names[0][0] + ". " + first_last_names[-1])
            if preprocessed_author == "":
                preprocessed_author = "missing_authors_Paper_ID_" + str(row[0])
            csv_out.writerow([row[0], row[1], row[2], preprocessed_author, row[4], row[5]])