from collections import Counter
import pickle

files = ["whois_tld/" + a.replace("\n", "") for a in open("whois_tld_ls", "r").readlines()]

c = Counter()

for file in files:
	if ".whois" in file:
		try:
			lines = open(file, "r").readlines()
			fields = [a.split(":")[0] for a in lines if ":" in a and len(a.split(":")[0].split(" ")) <= 6]
			print(file, fields)
			c.update(fields)
		except:
			pass

with open("fields.pickle", "wb") as f:
	pickle.dump(c, f)

