from collections import defaultdict
with open("result_tsv","r") as f:
	file = f.readlines()
result = defaultdict(int)
for line in file:
	string, occurences = line.split("\t")
	for values in string[string.find("(")+1:string.find(")")].split(","):
		result[values.strip()] += int(occurences)


params = sorted(result, key=result.get, reverse=True)

with open("how_rfc_is_instantiated.csv","w") as g:
	for param, occ in map(lambda x: (x, result[x]), params):
		g.write(param + "," + str(occ) + "\n")

