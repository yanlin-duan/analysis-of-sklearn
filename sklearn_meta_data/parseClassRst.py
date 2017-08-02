classes = []
with open("classes.rst","r") as f:
	line = f.readline()
	start=False
	readyToStart=False
	while line != "":
		if line=="\n" and start:
			start = False
		if start:
			classes.append(line.strip())
		if line == "\n" and readyToStart:
			start = True
			readyToStart = False
		if ":template: class.rst" in line:
			readyToStart = True
		line = f.readline()

subModule = set()
model = set()
for classInfo in classes:
	if "." in classInfo:
		val = classInfo.split(".")
		if len(val) > 2:
			print(val)
		else:
			subModule.add(val[0])
			model.add(val[1])

# Those have intermediate submodules
subModule.add('PatchExtractor')
subModule.add('image')
subModule.add('text')

model.add('PatchExtractor')
model.add('CountVectorizer')
model.add('HashingVectorizer')
model.add('TfidfTransformer')
model.add('TfidfVectorizer')


classes = []
with open("classes.rst","r") as f:
	line = f.readline()
	start=False
	readyToStart=False
	while line != "":
		if line=="\n" and start:
			start = False
		if start:
			classes.append(line.strip())
		if line == "\n" and readyToStart:
			start = True
			readyToStart = False
		if ":template: function.rst" in line:
			readyToStart = True
		line = f.readline()

subModule2 = set()
model2 = set()
for classInfo in classes:
	if "." in classInfo:
		val = classInfo.split(".")
		if val[0] == "":
			continue
		if len(val) > 2:
			subModule2.add(val[0])
			subModule2.add(val[1])
			model2.add(val[2])
		else:
			subModule2.add(val[0])
			model2.add(val[1])