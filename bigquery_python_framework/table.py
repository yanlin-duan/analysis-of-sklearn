from .BigQuerySelect import Select

class Table(object):
	def __init__(self, from_item):
		self.from_item = '[%s]' % from_item

	def __getattr__(self, attr):
		return self[attr]

	def __getitem__(self, columns):
		# Can be string (single value), tuple or slice
		if type(columns) is slice:
			if columns == slice(None, None, None):
				columns = ('*',) # select all
			else:
				raise Exception("Cannot specify a slice other than [:]!")
		elif type(columns) is str:
			columns = (columns,)
		elif not type(columns) is tuple:
			raise Exception("Cannot specify getitem other than type \
				slice (e.g. [:]), str (e.g. T['foo_column']) or tuple (e.g. T['foo_column', 'bar_column']!")
		return Select(columns, self.from_item)

class Content_py(Table):
	def __init__(self):
		super(Content_py, self).__init__('scikit-learn-research.pyfiles.content_py')

class Content_py_full(Table):
	def __init__(self):
		super(Content_py_full, self).__init__('scikit-learn-research.pyfiles.content_py_full')
