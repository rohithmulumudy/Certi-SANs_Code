import pickle

l = pickle.load(open("suspect_edges_diff_cert_id.pickle", "rb"))

nodes = set()
for a in l:
    nodes.update([a[0], a[2]])

with open("all_nodes_unique.txt", "w") as f:
    f.write("\n".join(nodes))


