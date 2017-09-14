class Func:
	def __init__(self, func_name, args, call_as = ""):
		self.func_name = func_name.upper()
		self.args = args
		self.call_as = call_as

	def __str__(self):
		return "%s(%s) %s" % (self.func_name, ",".join(self.args), self.call_as)
