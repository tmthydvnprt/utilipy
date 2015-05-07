"""
header.py
========

Auto generate headers for all files in a project

project    : Utilipy
version    : 0.1.0
status     : development
modifydate : 2015-05-07 05:45:00 -0700
createdate : 2015-05-07 05:38:00 -0700
website    : https://github.com/tmthydvnprt/utilipy
author     : tmthydvnprt
email      : tmthydvnprt@users.noreply.github.com
maintainer : tmthydvnprt
license    : MIT
copyright  : Copyright 2015, Utilipy
credits    :

"""

__all__ = ['']
__version__ = '0.1.0'
__status__ = 'development'
__date__ = '2015-05-07 05:18:22 -0700'
__website__ = ''
__author__ = 'tmthydvnprt'
__email__ = 'tmthydvnprt@users.noreply.github.com'
__maintainer__ = 'tmthydvnprt'
__license__ = 'MIT'
__copyright__ = 'Copyright 2015, utilipy'
__credits__ = ''

import os
import re
import copy
import codecs
import fnmatch
import datetime
import dateutil
import subprocess
import dateutil.parser

IGNORE = {'.DS_Store','.localized'}
GIT_DATES_SH = '''#!/bin/bash
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
    printf "%s,%s,%s\n" $file "$CREATEDATE" "$MODDATE";
done
'''
GIT_CHANGES_SH = 'git diff --no-commit-id --name-only -r HEAD'
METADATA_STR = '''
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
'''
DOCSTRING_STR = '''
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
'''
SPLIT_DOCSTRING_RE = re.compile(r'"""(.*?)"""(.*)', re.DOTALL)
REPLACE_DOCSTRING_RE = re.compile(r'"""(.*?)"""', re.DOTALL)
FIRST_EMPTY_LINE_RE = re.compile(r'\n\s*\n')
FIRST_KEY_RE = re.compile(r'.*\s*:\s*[A-Za-z0-9_-]+')
DOCSTRING_QUOTES = '"""{}"""'
PACKAGE_VARIABLE_RE = re.compile(r'__.*?__')

DEFAULT_INFO = {
    'project'    : '',
    'version'    : '0.1.0',
    'status'     : 'development',
    'modifydate' : '',
    'createdate' : '',
    'website'    : '',
    'author'     : '',
    'email'      : '',
    'maintainer' : '',
    'license'    : 'MIT',
    'copyright'  : '',
    'copydate'   : datetime.datetime.now().year,
    'credits'    : ''
}

def _read_file(file_path=''):
    """read a file into a string. assumes utf-8 encoding."""
    source = ''
    if os.path.exists(file_path) and os.path.isfile(file_path):
        fid = codecs.open(file_path, 'r', 'utf-8')
        source = fid.read()
        fid.close()
    return source

def _write_file(file_path='', data=''):
    """write a file from a string."""
    fid = codecs.open(file_path, 'w', 'utf-8')
    fid.write(data)
    fid.close()

def _replace_docstring_meta(source='', info=None):
    """replace meta data inside docstring"""
    
    docstring, code = SPLIT_DOCSTRING_RE.match(source).groups()
    
    backwards = docstring[::-1]
    split_backwards = backwards.split('\n', 3)
    if any([FIRST_KEY_RE.match(x) for x in split_backwards[0:3]]):
        first_key = next((i for i, j in enumerate(split_backwards[0:3]) if j), 0)
        meta_doc = '\n'.join(split_backwards[first_key:])
        meta, doc = FIRST_EMPTY_LINE_RE.split(meta_doc, 1)
        meta, doc = meta[::-1], doc[::-1]
    else:
        meta, doc = None, docstring

    formated_info = DOCSTRING_STR.format(**info)
    new_docstring = '{}\n{}\n'.format(doc, formated_info)
    new_docstring = '\n'.join([x.rstrip() for x in new_docstring.split('\n')])

    new_source = DOCSTRING_QUOTES.format(new_docstring) + code

    return new_source

def extend_copyright_string(copydate):
    """
    create string of copyright date, and extend if date is before the current year
    2015 -> '2015'
    2014 -> '2014-2015'
    """
    current_year = datetime.datetime.now().year
    copydate_string = '{}-{}'format(copydate, current_year) if copydate < current_year else str(current_year)
    return copydate_string

def generate(startpath='', project_info=None, project=''):
    """ 
    generate headers for all py files in project 
    
    example input:
    
    startpath = '/Users/timothydavenport/GitHub/utilipy/'
    project_info = {
        'project'    : 'Utilipy',
        'version'    : '0.1.0',
        'status'     : 'development',
        'modifydate' : '',
        'createdate' : '',
        'website'    : 'https://github.com/tmthydvnprt/utilipy',
        'author'     : 'tmthydvnprt',
        'email'      : 'tmthydvnprt@users.noreply.github.com',
        'maintainer' : 'tmthydvnprt',
        'license'    : 'MIT',
        'copyright'  : 'Utilipy',
        'copydate'   : 2015,
        'credits'    : ''
    }
    
    """
    
    # if no project passed, use the current directory as project name
    project = project if project else [ x for x in startpath.split(os.path.sep) if x][-1]
    
    # update default info with project into
    info = copy.deepcopy(DEFAULT_INFO)
    info.update(project_info)
    
    # add info if not defined
    if 'project' not in info.keys() or info['project'] == '':
        info['project'] = project
    if 'copyright' not in info.keys() or info['copyright'] == '':
        info['copyright'] = project
    info['copydate'] = extend_copyright_string(info['copydate'])
    
    # project init file
    package_init = os.path.join(startpath, project, '__init__.py')

    # change directories
    os.chdir(startpath)

    # get create/modify dates from git
    date_strings = subprocess.check_output(GIT_DATES_SH, shell=True).split('\n')
    dates = {line.split(',')[0]: dict(
                zip(['createdate', 'modifydate'], 
                [dateutil.parser.parse(x).strftime('%Y-%m-%d %H:%M:00 %z') for x in line.split(',')[1:]])
            ) for line in date_strings if not line == ''}

    # get changed files
    changed = [x for x in subprocess.check_output(GIT_CHANGES_SH, shell=True).split('\n') if x]
    print startpath
    # go thru files and add metadata
    for root, _, files in os.walk(startpath):    
        for f in fnmatch.filter(files, '*.py'):
            # get file
            filepath = os.path.join(root, f)
            relpath = filepath.replace(startpath, '')
            print relpath
            source = _read_file(filepath)
            # change meta
            fileinfo = copy.deepcopy(info)
            if relpath in changed :
                fileinfo['modifydate'] = datetime.datetime.fromtimestamp(
                    os.path.getmtime(filepath), 
                    dateutil.tz.tzlocal()
                ).strftime('%Y-%m-%d %H:%M:30 %z')
            else:
                fileinfo['modifydate'] = dates[relpath]['modifydate']
            fileinfo['createdate'] = dates[relpath]['createdate']
            # replace meta
            new_source = _replace_docstring_meta(source, fileinfo)

            if filepath == package_init:
                package_variables = [x for x in METADATA_STR.format(**fileinfo).split('\n') if x]
                for v in PACKAGE_VARIABLE_RE.findall(METADATA_STR):
                    v_replace = r'[ \t]*{}[ \t]*=[ \t]*.*'.format(v)
                    v_replacement = ''.join([x for x in package_variables if v in x]).rstrip()
                    if v in new_source:
                        new_source = re.sub(v_replace, v_replacement, new_source)
                    else: 
                        new_source += (v_replacement + '\n')

            # re-write source
            _write_file(filepath, new_source)

