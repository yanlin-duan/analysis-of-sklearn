from .visitor import *
from .tokenizer import Tokenizer
from .func import Func

class Select(object):
	def __init__(self, exp, from_item = None):
		self.select = exp
		self.from_item = [from_item]
		self.having = []
		self.order_by = []
		self.limit = None
		self.desc = False

	def excludes_sklearn(self, prefix=''):
		fields = ['repo_name', 'path']
		self.having += ["NOT %s CONTAINS 'sklearn'" % prefix + field for field in fields]
		return self

	def count(self, alias=""):
		return Func("COUNT", self.select, alias)

	def sort(self, keys=None):
		if keys is None:
			raise Exception("Please specify the key to order by!")
		else:
			if type(keys) is tuple:
				self.order_by += [self.getSortStrHelper(key) for key in keys]
			else:
				self.order_by.append(self.getSortStrHelper(keys))
		return self

	def getSortStrHelper(self, key):
		if isinstance(key, Select):
			return key.select
		elif type(key) is str:
			return key
		else:
			raise Exception("Cannot understand the key to order by!")

	def split(self, by, to):
		return Func("SPLIT", [self.select[0], "'%s'"%by], to)

	def split_to_line(self, to="line"):
		return self.split('\\n', to)

	def filter(self, val):
#		import inspect
#		source = inspect.getsource(val)
#		self.having.append(parse(source[source.find('lambda'):-1]))
		source = Tokenizer.tokenize_lambda_func(val,"filter")
		print(source)        
		self.having.append(parse(source))
		return self

	def __str__(self):
		query = "SELECT %s FROM %s" % (' , '.join([str(val) for val in self.select]), " , ".join(self.from_item))
		if self.having:
			query += " HAVING %s" % ' AND '.join(self.having)
		hasCount = False
		for val in self.select:
			if isinstance(val, Func) and val.func_name == "COUNT":
					hasCount = True
		if hasCount:
			group_by_list = []
			for val in self.select:
				if isinstance(val, Func):
					if val.func_name != "COUNT":
						group_by_list.append(val.call_as)
				elif type(val) is str:
					group_by_list.append(val)
				else:
					raise Exception("Cannot understand select %s!" % val)
			query += " GROUP BY %s" % ','.join(group_by_list)
		if self.order_by:
			query += " ORDER BY %s" % ','.join(self.order_by)
			if self.desc:
				query += " DESC"
		if self.limit:
			query += " LIMIT %s" % self.limit
		return query

	def __getitem__(self, columns):
		if type(columns) is slice:
			if columns == slice(None, None, None):
				columns = ('*',) # select all
			else:
				if columns.start is None and columns.step is None and columns.stop is not None:
					self.limit = columns.stop
					return self
				elif columns.start is None and columns.stop is None and columns.step == -1:
					self.desc = True
					return self
				else:
					raise Exception('Cannot understand slice!')
		elif type(columns) is str:
			columns = (columns,)
		elif not type(columns) is tuple:
			raise Exception("Cannot specify getitem other than type \
				slice (e.g. [:]), str (e.g. T['foo_column']) or tuple (e.g. T['foo_column', 'bar_column']!")
		return Select(columns, "( " + str(self) + " )")

	def run(self):
		from google.cloud import bigquery
		client = bigquery.Client()
		result = client.run_sync_query(str(self))
		result.timeout_ms = 99999999
		result.run()
		return result.rows


def a(b):
    import inspect
    print(inspect.getsource(b))