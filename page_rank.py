import csv

# constructs graphs of citations between papers
paper_graph = {}
with open("training_set.txt", "r") as f:
    reader = csv.reader(f)
    edges  = list(reader)
    for edge in edges:
        from_paper, to_paper, exists = edge[0].split()
        if exists == '1':
            if from_paper in paper_graph:
                paper_graph[from_paper] += [to_paper]
            else:
                paper_graph[from_paper] = [to_paper]    
    
# constructs graphs of citations between authors author_graph and 
# dict author_name_to_id mapping author name to an unique id used in the author_graph
author_name_to_id = {}
author_graph = []
with open("node_information_preprocessed_abstracts_authornames.csv", "r") as f:
    reader = csv.reader(f)
    node_info  = list(reader)
    # constructs paper_to_author_graph mapping papers' ids to its authors' ids.
    paper_to_author_graph = {}
    for row in node_info:
        author_ids = []
        for author in row[3].split(','):
            if author in author_name_to_id:
                author_ids += [author_name_to_id[author]]
            else:
                author_ids += [len(author_name_to_id)]
                author_name_to_id[author] = len(author_name_to_id)
        paper_to_author_graph[row[0]] = author_ids
    # transfers citing information from paper_graph to author_graph
    author_graph = [[] for x in author_name_to_id]
    for paper_citing in paper_graph:
        for paper_being_cited in paper_graph[paper_citing]:
            for author_citing in paper_to_author_graph[paper_citing]:
                for author_being_cited in  paper_to_author_graph[paper_being_cited]:
                    author_graph[author_citing] += [author_being_cited]

##########   NOW WE APPLY PAGERANK   ##############

damping_factor = 0.85
max_iter = 100
abs_avg_relative_change_to_stop = 0.0001

print("Started running PageRank!")
rank = [1/len(author_name_to_id) for x in author_name_to_id]
abs_avg_rel_change = 10000
n_iter = 1
while abs(abs_avg_rel_change) > abs_avg_relative_change_to_stop and n_iter < max_iter:
    print("iteration: ", n_iter, " abs avg relative change: ", abs(abs_avg_rel_change))
    # iterate on every author
    old_rank = rank
    rank = [(1-damping_factor)/len(rank) for x in old_rank]
    for author_citing in range(len(rank)):
        for author_being_cited in author_graph[author_citing]:
            rank[author_being_cited] += damping_factor * old_rank[author_citing] / len(author_graph[author_citing])
    # update auxiliary parameters
    abs_avg_rel_change = 0
    for author in range(len(rank)):
        abs_avg_rel_change += abs(rank[author] / old_rank[author] - 1.)
    abs_avg_rel_change /= len(rank)
    n_iter += 1
print("Stopped running PageRank!")    

with open("page_rank.csv", "w", newline='') as out:
    csv_out = csv.writer(out)
    author_list = [(rank[author_name_to_id[author]], author) for author in author_name_to_id]
    author_list.sort(reverse=True)    
    for a_rank, a_name in author_list:
        csv_out.writerow([a_name, a_rank])

