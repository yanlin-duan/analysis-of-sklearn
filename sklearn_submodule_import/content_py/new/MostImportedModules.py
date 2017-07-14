from collections import defaultdict
with open("result_tsv","r") as f:
	file = f.readlines()
result = defaultdict(int)
for line in file:
	string, occurences = line.split("\t")
	if "from sklearn import" in string:
		modules = string.split("from sklearn import ")[-1]
		for importModule in modules.split(","):
			moduleOriginalName = importModule.split(" as ")[0].strip(" ();")
			if moduleOriginalName != "":
				result[moduleOriginalName] += int(occurences)
	elif "from sklearn." in string:
		moduleOriginalNames = string.split("from sklearn.")[-1].split("import")[0].strip(" ();")
		for moduleOriginalName in moduleOriginalNames.split("."):
			if moduleOriginalName != "":
					result[moduleOriginalName.strip(" ();")] += int(occurences)


modules = sorted(result, key=result.get, reverse=True)

with open("most_imported_module_name.csv","w") as g:
	for module, occ in map(lambda x: (x, result[x]), modules):
		g.write(module + "," + str(occ) + "\n")
		if module.startswith("_"):
			print(module, occ)

