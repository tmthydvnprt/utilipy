title: quilt docs: pydoc_markdown
description: > python pydoc_markdown.py path/to/source path/to/output
author: markdoc.py

<ul class="breadcrumb">
<li><a href="index.html">quilt</a></li>
<li><a href="pydoc_markdown.html">pydoc_markdown</a></li>
</ul>
****************************************************************************************************************
[TOC]
## __NAME__

pydoc\_markdown - pydoc_markdown.py - generate python documenation in markdown

## __FILE__

`/Users/timothydavenport/GitHub/utilipy/utilipy`

## __DESCRIPTION__

> python pydoc_markdown.py path/to/source path/to/output

project    : utilipy
version    : 0.1.0
status     : development
modifydate : 2015-05-12 05:56:00 -0700
createdate : 2015-05-12 05:32:00 -0700
website    : https://github.com/tmthydvnprt/utilipy
author     : tmthydvnprt
email      : tmthydvnprt@users.noreply.github.com
maintainer : tmthydvnprt
license    : MIT
copyright  : Copyright 2015, utilipy
credits    :

## __MODULES__

[__builtin__](https://www.google.com/#q=python+__builtin__), [glob](https://www.google.com/#q=python+glob), [imp](https://www.google.com/#q=python+imp), [inspect](https://www.google.com/#q=python+inspect), [os](https://www.google.com/#q=python+os), [pkgutil](https://www.google.com/#q=python+pkgutil), [pydoc](https://www.google.com/#q=python+pydoc), [sys](https://www.google.com/#q=python+sys)
{: .lead}

## __FUNCTIONS__

def __escape\_equal__(_mrkdn=''_'):
{: .lead}
> escape =

def __escape\_md__(_mrkdn=''_'):
{: .lead}
> escape __ (e.g. for __init__.py)

def __main__(_source='', output=''_'):
{: .lead}
> run pydoc markdown

## __CLASSES__

pydoc.TextDoc(pydoc.Doc)
    MarkdownDoc

### class __MarkdownDoc__
> #### description
> ****************
> markdown based pydoc output
> 
> 
> #### data
> ****************
> __underline__
> ```
> ****************
> ```
> 
> #### methods
> ****************
> def __bold__(_self, text_'):
> {: .lead}
> > Formats text as bold in markdown.
> 
> def __docclass__(_self, cls, name=None, mod=None_'):
> {: .lead}
> > Produce markdown documentation for the class obj cls.
> 
> def __docmodule__(_self, obj, name=None, mod=None_'):
> {: .lead}
> > Produce markdown documentation for a given module obj.
> 
> def __docother__(_self, obj, name=None, mod=None, parent=None, maxlen=None, doc=None_'):
> {: .lead}
> > Produce text documentation for a data obj.
> 
> def __docroutine__(_self, obj, name=None, mod=None, cl=None_'):
> {: .lead}
> > Produce text documentation for a function or method obj.
> 
> def __emphasis__(_self, text_'):
> {: .lead}
> > Formats text with emphasis in markdown.
> 
> def __indent__(_self, text, prefix=''_'):
> {: .lead}
> > Indent text by prepending a given prefix to each line.
> 
> def __process\_class\_name__(_self, name, bases, module_'):
> {: .lead}
> > Format the class's name and bases.
> 
> def __process\_docstring__(_self, obj_'):
> {: .lead}
> > Get the docstring and turn it into a list.
> 
> def __process\_subsection__(_self, name_'):
> {: .lead}
> > format the subsection as a header
> 
> def __section__(_self, title, contents_'):
> {: .lead}
> > Format a section with a given heading.
>

## __DATA__

__CONTENT__
```
### [%s](%s.html)
%s

```

__INDEX__
```
%s
#%s
%s
### Package Contents:
%s

```

__LINKLINE__
```
<ul class="breadcrumb">
<li><a href="index.html">quilt</a></li>
<li><a href="%s.html">%s</a></li>
</ul>
****************************************************************************************************************
[TOC]

```

__TOPLINE__
```
title: %s
description: %s
author: %s


```

