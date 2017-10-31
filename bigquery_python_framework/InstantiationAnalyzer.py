class InstantiationAnalyzer:
    def __init__(self, modelName):
        from collections import defaultdict
        self.modelName = modelName
        self.d = defaultdict(lambda : defaultdict(int))
        self.counter = 0

    def parse(self,code):
        import parso
        node = parso.parse(sample_code)
        self.dfs(node)
    
    def dfs(self, node):
        if hasattr(node, 'children'):
            for child in node.children:
                self.dfs(child)
        else:
            if node.value == self.modelName:
                p = node.parent
                if p.type =="atom_expr" and p.children[0] == node:
                    self.parseArg(p.children[1].children[1])

    def parseArg(self,node):
        if node.type == "arglist":
            for child in node.children:
                if child.type == "argument":
                    keyword = self.getVal(child.children[0])
                    val = None
                    if len(child.children) >= 3:
                        val = getVal(child.children[2])
                    self.d[keyword][val] += 1
                    self.counter += 1
        elif node.type == "argument":        
            keyword = self.getVal(node.children[0])
            val = None
            if len(node.children) >= 3:
                val = self.getVal(node.children[2])
            else:
                keyword = node
            self.d[keyword][val] += 1
            self.counter += 1

    def getVal(self, node):
        if node.type != "factor" and node.type != "atom" and node.type != "atom_expr" and node.type != "term" and node.type != "arith_expr":
            return node.value
        else:
            return node