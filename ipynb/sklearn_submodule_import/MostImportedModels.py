from collections import defaultdict
with open("result_tsv","r") as f:
	file = f.readlines()
result = defaultdict(int)
for line in file:
	string, occurences = line.split("\t")
	if "util" in string:
		continue
	imports = string.split(" import ")[1]
	for importModule in imports.split(","):
		moduleOriginalName = importModule.split(" as ")[0].strip(" ();")
		if moduleOriginalName != "":
			result[moduleOriginalName] += int(occurences)

modules = sorted(result, key=result.get, reverse=True)
with open("most_imported_model_function.csv","w") as g:
	for module, occ in map(lambda x: (x, result[x]), modules):
		g.write(module + "," + str(occ) + "\n")

