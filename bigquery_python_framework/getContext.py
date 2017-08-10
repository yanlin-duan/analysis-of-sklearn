def getContext(modelName):
  from google.cloud import bigquery
  client = bigquery.Client()
  query = '''\
  #standardSQL
  CREATE TEMPORARY FUNCTION parsePythonFile(a STRING)
  RETURNS STRING
  LANGUAGE js AS """
    if (a === null) {
      return null;
    }
    var lines = a.split('\\\\n');
    for (i=0;i<lines.length;i++) {
      if (lines[i].indexOf("%s(")!==-1 &&
        lines[i].indexOf("class")===-1
      ){
        return lines.slice(Math.max(i-10,0),Math.min(i+10,lines.length-1)).join("\\\\n");
      }
    }
  """;

  CREATE TEMPORARY FUNCTION parsePythonFile2(a STRING, b STRING)
  RETURNS STRING
  LANGUAGE js AS """
    if (a === null) {
      return null;
    }
    var lines = a.split('\\\\n');
    for (i=0;i<lines.length;i++) {
      if (lines[i].indexOf("%s(")!==-1 &&
        lines[i].indexOf("class")===-1
      ){
        return b;
      }
    }
  """;

  SELECT
    parsePythonFile(content) match,
    parsePythonFile2(content,sample_path) path,
    parsePythonFile2(content,sample_repo_name ) repo_name,
    count(*) count
  FROM   
    `scikit-learn-research.pyfiles.content_py` 
  WHERE
    (NOT ENDS_WITH(sample_repo_name, "scikit-learn"))
     AND (NOT ENDS_WITH(sample_repo_name, "sklearn"))
  GROUP BY
  1,2,3
  ORDER BY 
  count DESC
  '''% (modelName,modelName)
  result = client.run_sync_query(query)
  result.timeout_ms = 99999999
  result.run()
  return result