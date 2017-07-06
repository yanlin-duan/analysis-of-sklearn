SELECT
  line,
  COUNT(*) count
FROM (
    SELECT
      SPLIT(content, '\n') line,
      id
    FROM
      [fh-bigquery:github_extracts.contents_py]
    WHERE
      content CONTAINS 'import'
      AND sample_path LIKE '%.py'
      AND (NOT RIGHT(sample_repo_name,12) = "scikit-learn")
      AND (NOT Right(sample_repo_name,7) = "sklearn")
    HAVING
      REGEXP_MATCH(line, r'from sklearn.*? import .+') )
GROUP BY
  1
ORDER BY
  count DESC