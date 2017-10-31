class GithubPython(object):
	def __init__(self):
		self.where = None
		self.c = None
		self.select = None
		self.excludeRepoName = None
		super(GithubPython, self).__init__()

	def files(self):
		self.where = "[scikit-learn-research.pyfiles.content_py_full]"
		return self

	def uniqueFiles(self):
		self.where = "[scikit-learn-research.pyfiles.content_py]"
		return self

	def contains(self, keyword):
		self.c = keyword
		return self

	def excludeByRepoName(self, keyword):
		self.excludeRepoName = keyword
		return self

	def getCount(self):
		self.select = 'COUNT(*) count'
		return self

	def buildString(self):
		s = ""
		if self.select != None:
			s += """\
			SELECT
			{}""".format(self.select)
		if self.where:
			s += """\
			FROM
			{}""".format(self.where)
		if self.c or self.excludeRepoName:
			s += """
			WHERE
			"""

			if self.c:
				s += """
			content CONTAINS '{}'
			""".format(self.c)
			if self.c and self.excludeRepoName:
				s += """
				AND
			"""
			if self.excludeRepoName:
				s += """
			(NOT sample_repo_name CONTAINS '{}')\
			""".format(self.excludeRepoName)
		return s

	def run(self, query=None):
		if query is None:
			query = self.buildString()
		from google.cloud import bigquery
		client = bigquery.Client()
		result = client.run_sync_query(query)
		result.timeout_ms = 99999999
		result.run()
		return list(result.fetch_data())

	def module_with_most_import(self):
		query = """\
SELECT
  sample_repo_name,
  COUNT(*) count
FROM (
    SELECT
      SPLIT(content, '\n') line,
      sample_repo_name
    FROM
      [fh-bigquery:github_extracts.contents_py]
    WHERE
      content CONTAINS 'import'
      AND sample_path LIKE '%.py'
      AND (NOT RIGHT(sample_repo_name,12) = "scikit-learn")
      AND (NOT Right(sample_repo_name,7) = "sklearn")
    HAVING
      REGEXP_MATCH(line, r'from sklearn.*? import .+')
)
GROUP BY
  1
ORDER BY
  count DESC
"""
		return self.run(query)
