from bigquery_python_framework.table import Content_py_full
pyTable = Content_py_full()
line = pyTable['content'].split_to_line()
query = pyTable[line, 'repo_name'].filter(lambda line, repo_name: "sklearn" not in repo_name and 
        regexp_match(line, "from sklearn.*? import .+"))[:10]