from sklearn.externals.joblib import Memory
from .GithubPython import GithubPython
memory = Memory(cachedir=".",verbose=0)

@memory.cache
def run(query):
    return GithubPython().run(query)

def prettyPrintPythonCode(code):
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from IPython.display import HTML
    from pygments.formatters import HtmlFormatter
    import IPython

    IPython.display.display(HTML('<style type="text/css">{}</style>{}'.format(
            HtmlFormatter().get_style_defs('.highlight'),
            highlight(code, PythonLexer(), HtmlFormatter()))))

def prettyPrintContext(context):
    i = 1
    for val, path, repo_name, count in context:
        print("%d."%i,)
        getGithubURL([(repo_name, path)])
        prettyPrintPythonCode(val)
        i +=1

def getGithubURL(result):
    for repo_name, path in result:
        print("https://github.com/{}/tree/master/{}".format(repo_name,path))

# The getContext function can only return the first 
# occurence of modelName in each file
@memory.cache
def getContext(modelName):
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
      if (lines[i].indexOf("%s")!==-1){
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
      if (lines[i].indexOf("%s")!==-1){
        return b;
      }
    }
  """;

  SELECT
    parsePythonFile(content) match,
    parsePythonFile2(content,sample_path) path,
    parsePythonFile2(content,sample_repo_name) repo_name,
    count(*) count
  FROM   
    `scikit-learn-research.pyfiles.content_py` 
  WHERE
     STRPOS(sample_repo_name, 'sklearn') = 0
     AND STRPOS(sample_repo_name, 'scikit-learn') = 0
     AND STRPOS(sample_path,'sklearn') = 0
     AND STRPOS(sample_path,'scikit-learn') = 0
     AND NOT(STRPOS(content, 'sklearn') = 0)
  GROUP BY
  1,2,3
  ORDER BY 
  count DESC
  '''% (modelName,modelName)
  return run(query)

# The getContext function can only return the first 
# occurence of modelName in each file
@memory.cache
def getContextAfter(modelName, lineNum=10):
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
      if (lines[i].indexOf("%s")!==-1){
        return lines.slice(i,Math.min(i+%d,lines.length-1)).join("\\\\n");
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
      if (lines[i].indexOf("%s")!==-1){
        return b;
      }
    }
  """;

  SELECT
    parsePythonFile(content) match,
    parsePythonFile2(content,sample_path) path,
    parsePythonFile2(content,sample_repo_name) repo_name,
    count(*) count
  FROM   
    `scikit-learn-research.pyfiles.content_py` 
  WHERE
     STRPOS(sample_repo_name, 'sklearn') = 0
     AND STRPOS(sample_repo_name, 'scikit-learn') = 0
     AND STRPOS(sample_path,'sklearn') = 0
     AND STRPOS(sample_path,'scikit-learn') = 0
     AND NOT(STRPOS(content, 'sklearn') = 0)
  GROUP BY
  1,2,3
  ORDER BY 
  count DESC
  '''% (modelName,lineNum, modelName)
  return run(query)


# The getContext function can only return the first 
# occurence of modelName in each file

def getContextAll(modelName):
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
      if (lines[i].indexOf("%s")!==-1){
        return a;
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
      if (lines[i].indexOf("%s")!==-1){
        return b;
      }
    }
  """;

  SELECT
    parsePythonFile(content) match,
    parsePythonFile2(content,sample_path) path,
    parsePythonFile2(content,sample_repo_name) repo_name,
    count(*) count
  FROM   
    `scikit-learn-research.pyfiles.content_py` 
  WHERE
     STRPOS(sample_repo_name, 'sklearn') = 0
     AND STRPOS(sample_repo_name, 'scikit-learn') = 0
     AND STRPOS(sample_path,'sklearn') = 0
     AND STRPOS(sample_path,'scikit-learn') = 0
     AND NOT(STRPOS(content, 'sklearn') = 0)
  GROUP BY
  1,2,3
  ORDER BY 
  count DESC
  '''% (modelName, modelName)
  return run(query)

@memory.cache
def parseInstantiation(L,param):
    d = dict()
    for val, count in L:
        val = val.replace(" ","")
        startIndex = val.find(param+"=")
        if startIndex != -1:
            startIndex = startIndex + len(param)
            startIndex += 1 # for '=' character
            endIndex = startIndex
            while endIndex < len(val) and val[endIndex] != ',':
                endIndex += 1
            d[val[startIndex:endIndex].strip(") ")] = d.get(val[startIndex:endIndex].strip(") "),0) + count 
            if (val[startIndex:endIndex].strip(") ") == ''):
                print(val)
    return d

@memory.cache
def queryByKeyword(keyword):
    keywordQuery = GithubPython().run("""\
    SELECT
        sample_repo_name,
        sample_path
    FROM (
    SELECT
      SPLIT(content, '\n') line,
      sample_repo_name,
      sample_path
    FROM
      [scikit-learn-research:pyfiles.content_py] 
    WHERE
      (NOT sample_repo_name CONTAINS "scikit-learn") AND
      (NOT sample_repo_name CONTAINS "sklearn") AND
      (NOT sample_path CONTAINS "scikit-learn") AND
      (NOT sample_path CONTAINS "sklearn")
    HAVING
      line CONTAINS '%s'
    )
    """ % keyword
    )
    return keywordQuery

@memory.cache
def getInstantiation(modelName):
    instantiateQuery = """\
    SELECT
      REGEXP_EXTRACT(content, r'(%s *\(.*?\))') match,
      count(*) count
    FROM   
      [scikit-learn-research:pyfiles.content_py] 
    WHERE
      (NOT sample_repo_name CONTAINS "scikit-learn") AND
      (NOT sample_repo_name CONTAINS "sklearn") AND
      (NOT sample_path CONTAINS "scikit-learn") AND
      (NOT sample_path CONTAINS "sklearn")
    GROUP BY
    match
    HAVING
      (NOT match is NULL)
    ORDER BY
    count DESC
    """ % (modelName)
    return run(instantiateQuery)

@memory.cache
def defaultInstantiationWithGridSearch(modelName):
    withGridSearch = """\
    SELECT
      COUNT(*) count from (
      SELECT
        REGEXP_EXTRACT(content, r'(%s *\(\))') match,
        content,
      FROM
        [scikit-learn-research:pyfiles.content_py]
      WHERE
        (NOT sample_repo_name CONTAINS "scikit-learn") AND
        (NOT sample_repo_name CONTAINS "sklearn") AND
        (NOT sample_path CONTAINS "scikit-learn") AND
        (NOT sample_path CONTAINS "sklearn") 
      )
    WHERE
      match!=""
      AND content CONTAINS 'GridSearchCV'
    """ % modelName
    withGridSearchNum = GithubPython().run(withGridSearch)[0][0]
    withoutGridSearch = """\
    SELECT
      COUNT(*) count from(
      SELECT
        REGEXP_EXTRACT(content, r'(%s *\(\))') match,
        content,
      FROM
        [scikit-learn-research:pyfiles.content_py]
      WHERE
        (NOT sample_repo_name CONTAINS "scikit-learn") AND
        (NOT sample_repo_name CONTAINS "sklearn") AND
        (NOT sample_path CONTAINS "scikit-learn") AND
        (NOT sample_path CONTAINS "sklearn")
      )
    WHERE
      match!=""
      AND NOT content CONTAINS 'GridSearchCV'
    """ % modelName
    withoutGridSearchNum = GithubPython().run(withoutGridSearch)[0][0]
    return (withGridSearchNum, withoutGridSearchNum)

def barhplot(result, xlabel, title,  color='green'):
    fig, ax = plt.subplots()
    xs = [x for x, _ in result]
    y_pos = range(len(xs))
    ys = [y for _, y in result]
    ax.barh(y_pos, ys, align='center', color=color, ecolor='black')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(xs)
    ax.invert_yaxis()  # labels read top-to-bottom
    for i, v in enumerate(ys):
        ax.text(v + 3, i + .25, str(v), color=color)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    plt.show()

def plotPie(labels, sizes):
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()

@memory.cache
def scatterPlotForPythonIpynbComparison(a,b,num):
    common_keys = list(set([key for key, _ in a[:num]]) & set([key for key, _ in b[:num]]))
    import numpy as np
    N = len(common_keys)
    x = [dict((key, val) for key, val in a)[key] for key in common_keys]
    y = [dict((key, val) for key, val in b)[key] for key in common_keys]
    colors = np.random.rand(N)

    fig, ax = plt.subplots(figsize=(10,10))
    ax.scatter(x, y, s=10, c=colors)
    ax.set_xlabel('Python')
    ax.set_ylabel('ipynb')

    for i, txt in enumerate(common_keys):
        ax.annotate(txt, (x[i],y[i]))

    plt.show()

@memory.cache
def getResult(d, count=20):
    ks = sorted(d,key=d.get)[::-1][:count]
    return [(k,d[k]) for k in ks]