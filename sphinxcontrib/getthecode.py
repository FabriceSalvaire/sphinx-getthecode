# -*- coding: utf-8 -*-

"""This plugin provides an enhanced ``literalinclude`` directive for Sphinx Documentation
Generator.

"""

####################################################################################################

import codecs
import os
import posixpath

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.writers.html4css1 import HTMLTranslator as BaseTranslator

from sphinx.util.nodes import set_source_info

####################################################################################################

class GetTheCode(nodes.literal_block):
    pass

####################################################################################################

class GetTheCodeDirective(Directive):

    """This code is a copy-paste from :file:`sphinx/directives/code.py` :class:`LiteralInclude`. See
    also :file:`sphinx/roles.py` :class:`XRefRole`.

    """

    ##############################################

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'linenos': directives.flag,
        'language': directives.unchanged_required,
        'encoding': directives.encoding,
        'hidden': directives.flag,
        }

    ##############################################

    def run(self):

        document = self.state.document
        if not document.settings.file_insertion_enabled:
            return [document.reporter.warning('File insertion disabled', line=self.lineno)]
        env = document.settings.env
        relative_filename, filename = env.relfn2path(self.arguments[0])

        encoding = self.options.get('encoding', env.config.source_encoding)
        codec_info = codecs.lookup(encoding)
        try:
            f = codecs.StreamReaderWriter(open(filename, 'rb'),
                                          codec_info[2], codec_info[3], 'strict')
            text = f.read() # file content
            f.close()
        except (IOError, OSError):
            return [document.reporter.warning('Include file %r not found or reading it failed' % filename,
                                              line=self.lineno)]
        except UnicodeError:
            return [document.reporter.warning('Encoding %r used for reading included file %r seems to '
                                              'be wrong, try giving an :encoding: option' %
                                              (encoding, filename))]

        retnode = GetTheCode(text, text, source=filename, filename=None)
        set_source_info(self, retnode)
        if self.options.get('language', ''):
            retnode['language'] = self.options['language']
        if 'linenos' in self.options:
            retnode['linenos'] = True
        if 'hidden' in self.options:
            retnode['hidden'] = True
        env.note_dependency(relative_filename)

        return [retnode]

####################################################################################################

def visit_GetTheCode_html(self, node):

    """
    This code is a copy-paste from :file:`sphinx/writers/html.py`.
    """

    # {
    #   'rawsource': u"...",
    #   'parent': <section "introduction": <title...><paragraph...><paragraph...><literal_block...> ...>,
    #   'source': '/home.../open-source-frontends.rst',
    #   'tagname': 'GetTheCode',
    #   'attributes': {'language': 'python', 'dupnames': [], 'xml:space': 'preserve', 'ids': [], 'backrefs': [],
    #                  'source': u'/home.../SimpleRectifierWithTransformer-jmodelica.py',
    #                  'classes': [], 'names': []},
    #   'line': 42,
    #   'document': <document: <comment...><comment...><section "open source frontends"...>>,
    #   'children': [<#text: 'from pymodelica import compile_fmu\nfrom pyfmi import load_fmu\n\ni ...'>]
    #  }

    self.body.append(self.starttag(node, 'div', CLASS=('getthecode')))
    # self.context.append('</div>\n')

    basename = os.path.basename(node['filename'])
    download_path = posixpath.join(self.builder.dlpath, node['filename'])
    # class="reference download internal"
    self.body.append(
        '<div class="getthecode-header">\n'
        '  <ul>\n'
        '  <li class="getthecode-filename">%s</li>\n'
        '  <li class="getthecode-filename-link"><a href="%s"><span >%s</span></a></li>\n'
        # '<button id="copy-button" data-clipboard-target="clipboard_pre">Copy to Clipboard</button>'
        # '<pre id="clipboard_pre">' + node.rawsource + </pre>'
        '  </ul>\n'
        '</div>\n' %
        (basename, download_path, basename))

    if node.rawsource != node.astext():
        # most probably a parsed-literal block -- don't highlight
        return BaseTranslator.visit_literal_block(self, node)
    lang = self.highlightlang
    highlight_args = node.get('highlight_args', {})
    if node.has_key('language'):
        # code-block directives
        lang = node['language']
        highlight_args['force'] = True
    linenos = node.rawsource.count('\n') >= self.highlightlinenothreshold - 1
    if node.has_key('linenos'):
        linenos = node['linenos']
    def warner(msg):
        self.builder.warn(msg, (self.builder.current_docname, node.line))
    highlighted = self.highlighter.highlight_block(node.rawsource, lang, warn=warner,
                                                   linenos=linenos, **highlight_args)
    _class = 'highlight-%s' % lang
    if node.get('hidden', False):
        _class += ' highlight-hidden'
    starttag = self.starttag(node, 'div', suffix='', CLASS=_class)
    self.body.append(starttag + highlighted + '</div>\n')
    self.body.append('</div>\n')

    # don't call depart_GetTheCode_html else dump source code
    raise nodes.SkipNode

####################################################################################################

def depart_GetTheCode_html(self, node):
    # print 'depart_GetTheCode_html'
    pass
    # BaseTranslator.depart_literal_block(self, node)
    #   self.body.append('\n</pre>\n')

####################################################################################################

def process_getthedoc(app, doctree):

    """ This function is a *doctree-read* callback. It copies the download-able files to the
    directory :directory:`_downloads`.

    This code is a copy-paste with few modifications of the
    :meth:`BuildEnvironment.process_downloads` method.
    """

    env = app.builder.env
    docname = env.docname

    for node in doctree.traverse(GetTheCode):
        # targetname = node['reftarget']
        targetname = os.path.basename(node['source'])
        rel_filename, filename = env.relfn2path(targetname, docname)
        # print 'target:', targetname
        # print rel_filename
        # print filename
        env.dependencies.setdefault(docname, set()).add(rel_filename)
        if not os.access(filename, os.R_OK):
            env.warn_node('download file not readable: %s' % filename, node)
            continue
        uniquename = env.dlfiles.add_file(docname, filename)
        node['filename'] = uniquename

####################################################################################################

def setup(app):

    app.add_node(
        GetTheCode,
        html=(visit_GetTheCode_html, depart_GetTheCode_html),
        # text=(visit_GetTheCode_text, depart_GetTheCode_text),
    )

    app.add_directive('getthecode', GetTheCodeDirective)

    app.connect('doctree-read', process_getthedoc)
