import token
import tokenize
import nbformat
from nbconvert import PythonExporter
import os
import io

class Tokenizer:
	
	@staticmethod
	def tokenize_lambda_func(val, within, notebook_name=None):
		if notebook_name:
			notebook_path = os.getcwd() + "/{}.ipynb".format(notebook_name)
			with open(notebook_path, 'r') as f:
				notebook = nbformat.reads(f.read(), nbformat.NO_CONVERT)
				exporter = PythonExporter()
				source, _ = exporter.from_notebook_node(notebook)
			readline = io.StringIO(source).readline
		else:
			readline = open(val.__code__.co_filename).readline
		first_line = val.__code__.co_firstlineno
		flag = False
		source = ""
		for t in tokenize.generate_tokens(readline):
			t_type,t_string,(r_start,c_start),(r_end,c_end),line = t
			t_name = token.tok_name[t_type]
			if r_start == first_line:
				if t_name == 'NAME' and t_string==within:
					flag = True
					res = t_string
					start = 0 # number of parenthesis
					continue
			if flag:
				source += ' ' + t_string
				if t_name == 'OP':
						if t_string=='(':
							start += 1
						elif t_string == ')':
							start -= 1
							if start == 0:
								break
		return source.strip()