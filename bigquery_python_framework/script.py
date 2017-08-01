from google.cloud import bigquery
client = bigquery.Client()
query = """\
SELECT
  REGEXP_EXTRACT(content, r'(RandomForestClassifier *\(.*?\))') match,
  count(*) count
FROM   
  [scikit-learn-research:pyfiles.content_py] 
WHERE
  (NOT RIGHT(sample_repo_name,12) = "scikit-learn")
   AND (NOT Right(sample_repo_name,7) = "sklearn")
GROUP BY
1
ORDER BY 
count DESC
"""

result = client.run_sync_query(query)