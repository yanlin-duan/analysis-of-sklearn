def openRandomFile():
	from google.cloud import bigquery
	client = bigquery.Client()
	query = """\
	SELECT
	  sample_repo_name,
	  sample_path,
	FROM   
	  [scikit-learn-research:pyfiles.content_ipynb] 
	WHERE
	  (NOT RIGHT(sample_repo_name,12) = "scikit-learn")
	   AND (NOT Right(sample_repo_name,7) = "sklearn")
	   AND RAND() < 10/164656
	LIMIT
	1
	"""
	result = client.run_sync_query(query)
	result.run()
	sample_repo_name, sample_path = result.rows[0]
	import webbrowser
	webbrowser.open(u"https://github.com/%s/blob/master/%s" % (sample_repo_name, sample_path))

def openFileByKeyword(keyword):
	from google.cloud import bigquery
	client = bigquery.Client()
	query = """\
	SELECT
	  sample_repo_name,
	  sample_path,
	FROM   
	  [scikit-learn-research:pyfiles.content_py] 
	WHERE
	  (NOT RIGHT(sample_repo_name,12) = "scikit-learn")
	   AND (NOT Right(sample_repo_name,7) = "sklearn")
	   AND content CONTAINS "%s"
	LIMIT
	1
	""" % keyword

	result = client.run_sync_query(query)
	result.run()

	sample_repo_name, sample_path = result.rows[0]

	import webbrowser

	webbrowser.open(u"https://github.com/%s/blob/master/%s" % (sample_repo_name, sample_path))
