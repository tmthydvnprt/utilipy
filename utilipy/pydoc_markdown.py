"""
pydoc_markdown.py - generate python documenation in markdown

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

"""

# pylint: disable=no-init
# pylint: disable=no-self-use
# pylint: disable=too-many-locals
# pylint: disable=protected-access
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements

import os
import sys
import imp
import glob
import pydoc
import inspect
import pkgutil
import __builtin__

TOPLINE = """title: %s
description: %s
author: %s

"""
LINKLINE = """<ul class="breadcrumb">
<li><a href="index.html">quilt</a></li>
<li><a href="%s.html">%s</a></li>
</ul>
****************************************************************************************************************
[TOC]
"""
INDEX = """%s
#%s
%s
### Package Contents:
%s
"""
CONTENT = """### [%s](%s.html)
%s
"""

def escape_md(mrkdn=''):
    """escape __ (e.g. for __init__.py)"""
    return mrkdn.replace(r'_', r'\_').replace(r'=', r'\=')

def escape_equal(mrkdn=''):
    """escape = """
    return mrkdn

class MarkdownDoc(pydoc.TextDoc):
    """markdown based pydoc output"""

    underline = "*" * 16

    def process_docstring(self, obj):
        """Get the docstring and turn it into a list."""
        docstring = pydoc.getdoc(obj)
        if docstring:
            return docstring + "\n\n"
        return ""

    def process_class_name(self, name, bases, module):
        """Format the class's name and bases."""
        title = "### class " + self.bold(name)
        if bases:
            # get the names of each of the bases
            base_titles = [pydoc.classname(base, module) for base in bases]
            # if its not just obj
            if len(base_titles) > 1:
                # append the list to the title
                title += "(%s)" % (", ".join(base_titles))
        return title

    def process_subsection(self, name):
        """format the subsection as a header"""
        return "#### " + name

    def bold(self, text):
        """ Formats text as bold in markdown. """
        return "__%s__" % text.replace(r'_', r'\_')

    def emphasis(self, text):
        """ Formats text with emphasis in markdown. """
        return "_%s_" % text.replace(r'_', r'\_')

    def indent(self, text, prefix=''):
        """Indent text by prepending a given prefix to each line."""
        return text

    def section(self, title, contents):
        """Format a section with a given heading."""
        clean_contents = self.indent(contents).rstrip()
        return "## %s\n\n%s\n\n" % (self.bold(title), clean_contents)

    def docmodule(self, obj, name=None, mod=None):
        """Produce markdown documentation for a given module obj."""
        name = obj.__name__ # ignore the passed-in name
        synop, desc = pydoc.splitdoc(pydoc.getdoc(obj))
        result = self.section('NAME', name.replace(r'_', r'\_') + (synop and ' - ' + synop))

        try:
            moduleall = obj.__all__
        except AttributeError:
            moduleall = None

        try:
            filepath = os.path.dirname(inspect.getabsfile(obj))
        except TypeError:
            filepath = '(built-in)'
        result = result + self.section('FILE', '`'+filepath+'`')

        docloc = self.getdocloc(obj)
        if docloc is not None:
            result = result + self.section('MODULE DOCS', docloc)

        if desc:
            result = result + self.section('DESCRIPTION', desc)

        if hasattr(obj, '__version__'):
            version = pydoc._binstr(obj.__version__)
            if version[:11] == '$Revision: ' and version[-1:] == '$':
                version = version[11:-1].strip()
            result = result + self.section('VERSION', version)
        if hasattr(obj, '__date__'):
            result = result + self.section('DATE', pydoc._binstr(obj.__date__))
        if hasattr(obj, '__author__'):
            result = result + self.section('AUTHOR', pydoc._binstr(obj.__author__))
        if hasattr(obj, '__credits__'):
            result = result + self.section('CREDITS', pydoc._binstr(obj.__credits__))

        classes = []
        for key, value in inspect.getmembers(obj, inspect.isclass):
            # if __all__ exists, believe it.  Otherwise use old heuristic.
            if moduleall is not None or (inspect.getmodule(value) or obj) is obj:
                if pydoc.visiblename(key, moduleall, obj):
                    classes.append((key, value))
        funcs = []
        for key, value in inspect.getmembers(obj, inspect.isroutine):
            # if __all__ exists, believe it.  Otherwise use old heuristic.
            if moduleall is not None or inspect.isbuiltin(value) or inspect.getmodule(value) is obj:
                if pydoc.visiblename(key, moduleall, obj):
                    funcs.append((key, value))
        data = []
        for key, value in inspect.getmembers(obj, pydoc.isdata):
            if pydoc.visiblename(key, moduleall, obj):
                data.append((key, value))

        modules = []
        for key, _ in inspect.getmembers(obj, inspect.ismodule):
            modules.append(key)
        if modules:
            modules = sorted(modules)
            contents = ', '.join(['[%s](https://www.google.com/#q=python+%s)' % (m, m) for m in modules]) + '\n{: .lead}'
            result = result + self.section('MODULES', contents)

        modpkgs = []
        modpkgs_names = set()
        if hasattr(obj, '__path__'):
            for _, modname, ispkg in pkgutil.iter_modules(obj.__path__):
                modpkgs_names.add(modname)
                if ispkg:
                    modpkgs.append(modname + ' (package)')
                else:
                    modpkgs.append(modname)

            modpkgs.sort()
            result = result + self.section('PACKAGE CONTENTS', pydoc.join(modpkgs, '\n'))

        # Detect submodules as sometimes created by C extensions
        submodules = []
        for key, value in inspect.getmembers(obj, inspect.ismodule):
            if value.__name__.startswith(name + '.') and key not in modpkgs_names:
                submodules.append(key)
        if submodules:
            submodules.sort()
            result = result + self.section('SUBMODULES', pydoc.join(submodules, '\n'))

        if funcs:
            contents = []
            for key, value in funcs:
                contents.append(self.document(value, key, name))
            result = result + self.section('FUNCTIONS', pydoc.join(contents, '\n'))

        if classes:
            classlist = [x[1] for x in classes]
            contents = [self.formattree(inspect.getclasstree(classlist, 1), name)]
            for key, value in classes:
                contents.append(self.document(value, key, name))
            result = result + self.section('CLASSES', pydoc.join(contents, '\n'))

        if data:
            contents = []
            for key, value in data:
                contents.append(self.docother(value, key, name))
            result = result + self.section('DATA', pydoc.join(contents, '\n'))

        return result

    def docclass(self, cls, name=None, mod=None):
        """Produce markdown documentation for the class obj cls."""

        # the overall document, as a line-delimited list
        document = []

        # get the obj's actual name, defaulting to the passed in name
        name = name or cls.__name__

        # get the obj's bases
        bases = cls.__bases__

        # get the obj's module
        mod = cls.__module__

        # get the obj's classname, which should be printed
        classtitle = self.process_class_name(name, bases, mod)
        document.append(classtitle)

        # get the obj's docstring, which should be printed
        docstring = self.process_docstring(cls)
        document.append(self.process_subsection("description"))
        document.append(self.underline)
        document.append(docstring)

        # get all the attributes of the class
        attrs = []
        for name, kind, classname, value in pydoc.classify_class_attrs(cls):
            if pydoc.visiblename(name):
                if kind is not __builtin__.object:
                    if classname == cls:
                        obj = (name, kind, classname, value)
                        attrs.append(obj)

        # sort them into categories
        data = [attr for attr in attrs if attr[1] == "data"]
        descriptors = [attr for attr in attrs if attr[1] == "data descriptor"]
        methods = [attr for attr in attrs if "method" in attr[1]]

        # start the data section
        if data:
            document.append(self.process_subsection("data"))
            document.append(self.underline)

        # process your attributes
        for name, kind, classname, value in data:
            document.append(self.document(getattr(cls, name), name, mod, cls))

        # start the descriptors section
        if descriptors:
            document.append(self.process_subsection("descriptors"))
            document.append(self.underline)

        # process your descriptors
        for _ in descriptors:
            document.append(self._docdescriptor(name, value, mod))

        # start the methods section
        if methods:
            document.append(self.process_subsection("methods"))
            document.append(self.underline)

        # process your methods
        for f in methods:
            if not f[0].startswith("__"):
                document.append(self.docroutine(f[-1]))

        return "\n".join(document).replace('\n', '\n> ')

    def docroutine(self, obj, name=None, mod=None, cl=None):
        """Produce text documentation for a function or method obj."""
        realname = obj.__name__
        name = name or realname
        note = ''
        skipdocs = 0
        if inspect.ismethod(obj):
            obj = obj.__func__
        if name == realname:
            title = self.bold(realname)
        else:
            if cl and realname in cl.__dict__ and cl.__dict__[realname] is obj:
                skipdocs = 1
            title = '%s = %s' % (self.bold(name), realname)
        if inspect.isfunction(obj):
            args, varargs, keywords, defaults = inspect.getargspec(obj)
            argspec = inspect.formatargspec(args, varargs, keywords, defaults, formatvalue=self.formatvalue)

        else:
            argspec = '(...)'
        decl = "def %s(%s'):\n{: .lead}%s" % (title, escape_equal(self.emphasis(argspec[1:-1])), note)
        if skipdocs:
            return decl + '\n'
        else:
            doc = pydoc.getdoc(obj) or ''
            return '%s\n> %s' % (decl, (doc and self.indent(doc).rstrip() + '\n'))

    def docother(self, obj, name=None, mod=None, parent=None, maxlen=None, doc=None):
        """Produce text documentation for a data obj."""
        if str(type(obj)) == "<type '_sre.SRE_Pattern'>":
            line = '%s\n```\n%s\n```\n' % ((name and self.bold(name)), obj.pattern)
        else:
            if name:
                line = '%s\n```\n%s\n```\n' % ((name and self.bold(name)), str(obj))
            else:
                line = '%s\n```\n%s\n```\n' % (self.bold(str(name)), str(obj))
        return line

def main(source='', output=''):
    """run pydoc markdown"""

    project = os.path.basename('quilt')

    if not os.path.isdir(output):
        os.makedirs(output)
    py_files = glob.glob(os.path.join(source, '*.py'))
    md_doc = {}

    module_names = []
    for py_file in py_files:
        name = os.path.splitext(os.path.basename(py_file))[0]
        if name != '__main__':
            module_names.append(os.path.basename(py_file))
            # module document page
            module = imp.load_source(os.path.splitext(name)[0], py_file)
            mkdn_doc = MarkdownDoc()
            doc = mkdn_doc.document(module)
            md_doc[name] = doc
            topline = TOPLINE % ('%s docs: %s' % (project, name), module.__doc__.split('\n')[3], "markdoc.py")
            linkline = LINKLINE % (name, name)
            fid = open(os.path.join(output, '%s.md' % name), 'w')
            fid.write(''.join([topline, linkline, md_doc[name]]))
            fid.close()

    # store for index page
    py_file = os.path.join(source, '__init__.py')
    name = os.path.splitext(os.path.basename(py_file))[0]
    module = imp.load_source(os.path.splitext(name)[0], py_file)
    contents = [CONTENT % (escape_md('__init__'), escape_md('__init__'), 'package module \n{: .lead}')]

    for mod in module.__all__:
        module2 = imp.load_source(mod, os.path.join(source, '%s.py' % mod))
        contents.append(CONTENT % (escape_md(mod), escape_md(mod), '%s\n{: .lead}' % module2.__doc__.split('\n')[3]))

    topline = TOPLINE % ('%s docs' % project, '%s documentation' % project, "pydoc_markdown.py")
    name = module.__doc__.split('\n')[1]
    desc = '%s\n{: .lead}' % module.__doc__.split('\n')[3]
    indexmd = INDEX % (topline, name, desc, ''.join(contents))

    fid = open(os.path.join(output, 'index.md'), 'w')
    fid.write(indexmd)
    fid.close()

    print 'Docs generated for:\t', ' '.join(module_names)

if __name__ == "__main__":

    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2])
    else:
        print 'no source or output'
