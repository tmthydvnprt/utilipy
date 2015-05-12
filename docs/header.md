title: quilt docs: header
description: 
author: markdoc.py

<ul class="breadcrumb">
<li><a href="index.html">quilt</a></li>
<li><a href="header.html">header</a></li>
</ul>
****************************************************************************************************************
[TOC]
## __NAME__

header

## __FILE__

`/Users/timothydavenport/GitHub/utilipy/utilipy`

## __DESCRIPTION__

header.py
========

Auto generate headers for all files in a project

project    : utilipy
version    : 0.1.0
status     : development
modifydate : 2015-05-12 05:56:00 -0700
createdate : 2015-05-07 05:38:00 -0700
website    : https://github.com/tmthydvnprt/utilipy
author     : tmthydvnprt
email      : tmthydvnprt@users.noreply.github.com
maintainer : tmthydvnprt
license    : MIT
copyright  : Copyright 2015, utilipy
credits    :

## __MODULES__

[codecs](https://www.google.com/#q=python+codecs), [copy](https://www.google.com/#q=python+copy), [datetime](https://www.google.com/#q=python+datetime), [dateutil](https://www.google.com/#q=python+dateutil), [fnmatch](https://www.google.com/#q=python+fnmatch), [os](https://www.google.com/#q=python+os), [re](https://www.google.com/#q=python+re), [subprocess](https://www.google.com/#q=python+subprocess)
{: .lead}

## __FUNCTIONS__

def __extend\_copyright\_string__(_copydate_'):
{: .lead}
> create string of copyright date, and extend if date is before the current year
2015 -> '2015'
2014 -> '2014-2015'

def __generate__(_startpath='', project\_info=None_'):
{: .lead}
> generate headers for all py files in project

example input:

startpath = '/Users/timothydavenport/GitHub/utilipy/'
project_info = {
    'project'    : 'Utilipy',
    'website'    : 'https://github.com/tmthydvnprt/utilipy',
    'author'     : 'tmthydvnprt',
    'email'      : 'tmthydvnprt@users.noreply.github.com',
    'maintainer' : 'tmthydvnprt'
}

def __get\_git\_create\_modify\_dates__(__'):
{: .lead}
> use shell command to get create modify dates form git commits and return as dictionary of relative paths

def __replace\_init\_meta__(_source='', info=None_'):
{: .lead}
> replace meta data inside __init__ file

## __DATA__

__DEFAULT\_INFO__
```
{'status': 'development', 'website': '', 'maintainer': '', 'createdate': '', 'credits': '', 'copydate': 2015, 'modifydate': '', 'license': 'MIT', 'copyright': '', 'author': '', 'project': '', 'version': '0.1.0', 'email': ''}
```

__DOCSTRING\_QUOTES__
```
"""{}"""
```

__DOCSTRING\_STR__
```

project    : {project}
version    : {version}
status     : {status}
modifydate : {modifydate}
createdate : {createdate}
website    : {website}
author     : {author}
email      : {email}
maintainer : {maintainer}
license    : {license}
copyright  : Copyright {copydate}, {copyright}
credits    : {credits}

```

__FIRST\_EMPTY\_LINE\_RE__
```
\n\s*\n
```

__FIRST\_KEY\_RE__
```
.*\s*:\s*[A-Za-z0-9_-]+
```

__GIT\_CHANGES\_SH__
```
git diff --no-commit-id --name-only -r HEAD
```

__GIT\_DATES\_SH__
```
#!/bin/bash
# get the create and lastmod date of each file in a git tree
for file in `git ls-files`;
do
    # get create date
    FIRSTHASH=`git rev-list HEAD $file | tail -n 1`;
    CREATEDATE=`git show -s --format="%ci" $FIRSTHASH --`;
    # get mod date
    LASTHASH=`git rev-list HEAD $file | head -n 1`;
    MODDATE=`git show -s --format="%ci" $LASTHASH --`;
    # dump it out
    printf "%s,%s,%s
" $file "$CREATEDATE" "$MODDATE";
done

```

__IGNORE__
```
set(['.DS_Store', '.localized'])
```

__METADATA\_STR__
```

__version__ = '{version}'
__status__ = '{status}'
__date__ = '{modifydate}'
__website__ = '{website}'
__author__ = '{author}'
__email__ = '{email}'
__maintainer__ = '{maintainer}'
__license__ = '{license}'
__copyright__ = 'Copyright {copydate}, {copyright}'
__credits__ = '{credits}'

```

__PACKAGE\_VARIABLE\_RE__
```
__.*?__
```

__REPLACE\_DOCSTRING\_RE__
```
"""(.*?)"""
```

__SPLIT\_DOCSTRING\_RE__
```
"""(.*?)"""(.*)
```

