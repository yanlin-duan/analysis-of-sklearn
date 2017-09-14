# Reference: http://code.activestate.com/recipes/442447/
import ast

class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.src = ''

    def visit_Tuple(self,t):
        self.src += ','.join ( [ get_source(n) for n in t.nodes ])

    def visit_List(self,t):
        self.src += ','.join ( [ get_source(n) for n in t.nodes ])

    def visit_Name(self,t):
        self.src += t.id
        self.src += ' '

    def visit_AssName(self,t):
        self.src += t.name

    def visit_Str(self, t):
        self.src += "'%s'" %t.s

    def visit_Num(self,t):
        self.src += "%s" % t.n

    def visit_Const(self,t):
        if type(t.value) is str:
            # convert single quotes, SQL-style
            # self.src += "'%s'" %t.value.replace("'","''")
            self.src += "'%s'" %t.value
        else:
            self.src += str(t.value)

    def visit_Getattr(self,t):
        self.src += '%s.%s' %(get_source(t.expr),str(t.attrname))

    def visit_Compare(self,t):
        for oper in t.ops:
            if isinstance(oper, ast.NotIn) or isinstance(oper, ast.In):
                if isinstance(oper, ast.NotIn):
                    self.src += '(NOT '
                    oper = 'not in'
                else:
                    oper = 'in'
                self.visit(t.comparators[0])
                self.src += 'CONTAINS '
                self.visit(t.left)
                if oper == 'not in':
                    self.src += ')'
            else:
                if isinstance(oper, ast.Eq):
                    oper = '='
                self.visit(t.left)
                self.src += oper + ' '
                self.visit(t.comparators[0])
    def visit_BoolOp(self, t):
        if isinstance(t.op, ast.And):
            self.visit_And(t)
        elif isinstance(t.op, ast.Or):
            self.visit_Or(t)

    def visit_And(self,t):
        self.src += '('
        self.src += ' AND '.join([ get_source(n) for n in t.values ])
        self.src += ')'

    def visit_Or(self,t):
        self.src += '('
        self.src += ' OR '.join([ get_source(n) for n in t.values ])
        self.src += ')'

    def visit_Not(self,t):
        self.src += '(NOT ' + get_source(t.expr) + ')'

    def visit_Call(self, t):
        self.src += get_source(t.func).upper()
        self.src += '('
        self.src += ','.join([get_source(n) for n in t.args])
        self.src += ')'

    def visit(self, t):
        print(t)
        super(Visitor, self).visit(t)
        

def parse(source):
    return get_source(ast.parse(source))

def get_source(node):
    """Return the source code of the node, built by an instance of
    ge_visitor"""
    v = Visitor()
    v.visit(node)
    return v.src