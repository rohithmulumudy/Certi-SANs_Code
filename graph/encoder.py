import sys
import pickle

nodelist = dict()
with open("nodelist.unique", "r") as f:
	nodes = f.readlines()
	for node in enumerate(nodes):
		nodelist[node[1].replace("\n", "")] = node[0]

if "n" in sys.argv[1]:
	with open("nodelist.enc", "wb") as f:
		pickle.dump(nodelist, f)

if "e" in sys.argv[1]:
	with open("edgelist.enc", "w") as f:
		with open("edgelist.final", "r") as fr:
			for line in fr.readlines():
				print(line)
				line = line.replace("\n", "")
				if " " not in line:
					continue					
				ns = line.split(" ")
				if len(ns) != 2:
					continue
				n1, n2 = ns
				print("%d %d\n" % (nodelist[n1], nodelist[n2]))
				f.write("%d %d\n" % (nodelist[n1], nodelist[n2]))
