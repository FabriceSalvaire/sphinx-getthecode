"""This plugin provides an enhanced ``literalinclude`` directive for Sphinx Documentation Generator.

* https://www.sphinx-doc.org/en/master/extdev/index.html

"""

####################################################################################################

from pathlib import Path
import codecs
import os

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
        'encoding': directives.encoding,
        'hidden': directives.flag,
        'language': directives.unchanged_required,
        'linenos': directives.flag,
        'notebook': directives.flag,
    }

    ##############################################

    def run(self):

        document = self.state.document

        if not document.settings.file_insertion_enabled:
            return [document.reporter.warning('File insertion disabled', line=self.lineno)]

        env = document.settings.env

        # arguments = [relative_source_path, ]
        relative_source_path, source_path = env.relfn2path(self.arguments[0])

        encoding = self.options.get('encoding', env.config.source_encoding)
        codec_info = codecs.lookup(encoding)
        try:
            fh = codecs.StreamReaderWriter(open(source_path, 'rb'), codec_info[2], codec_info[3], 'strict')
            text = fh.read()
            fh.close()
        except (IOError, OSError):
            return [
                document.reporter.warning(
                    'Include file {} not found or reading it failed'.format(source_path),
                    line=self.lineno,
                )
            ]
        except UnicodeError:
            template = 'Encoding {} used for reading included file {} seems to be wrong, try giving an :encoding: option'
            return [document.reporter.warning(template.format(encoding, source_path))]

        env.note_dependency(relative_source_path)

        node = GetTheCode(text, text, source=source_path, filename=None)
        set_source_info(self, node)
        if self.options.get('language', ''):
            node['language'] = self.options['language']
        if 'linenos' in self.options:
            node['linenos'] = True
        if 'hidden' in self.options:
            node['hidden'] = True
        if 'notebook' in self.options:
            # node['notebook'] = True
            source_path = Path(source_path)
            notebook_name = source_path.stem + '.ipynb'
            notebook_path = source_path.parent.joinpath(notebook_name)
            node['notebook_path'] = notebook_path

        return [node]

####################################################################################################

def process_getthedoc(app, doctree):

    """ This function is a *doctree-read* callback. It copies the download-able files to the
    directory :directory:`_downloads`.

    This code is a copy-paste with few modifications of the
    :meth:`BuildEnvironment.process_downloads` method.
    """

    # Called before visit_GetTheCode_html
    # print('process_getthedoc')

    env = app.builder.env
    document_name = env.docname # examples/document-generator/full-test .rst

    for node in doctree.traverse(GetTheCode):
        # targetname = node['reftarget']

        # /home/.../doc/sphinx/source/examples/document-generator/full-test.py
        source_path = Path(node['source'])
        relative_source_path, source_path = env.relfn2path(source_path.name, document_name)
        env.dependencies.setdefault(document_name, set()).add(relative_source_path)

        if not os.access(source_path, os.R_OK):
            env.warn_node('download file not readable: {}'.format(source_path), node)
            continue

        # c3e20896d45729b3dd37b566def9e52a/full-test.py
        unique_name = env.dlfiles.add_file(document_name, source_path)
        node['filename'] = unique_name # Fixme: filename -> ... ?

        notebook_path = node.get('notebook_path', None)
        if notebook_path is not None:
            if not os.access(notebook_path, os.R_OK):
                env.warn_node('download file not readable: {}'.format(notebook_path), node)
                continue

            unique_name = env.dlfiles.add_file(document_name, str(notebook_path))
            node['notebook_download_path'] = unique_name # Fixme: -> ... ?

####################################################################################################

def visit_GetTheCode_html(self, node):

    """
    This code is a copy-paste from :file:`sphinx/writers/html.py`.
    """

    # print('visit_GetTheCode_html')

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

    # Open the top div
    self.body.append(self.starttag(node, 'div', CLASS=('getthecode')))
    # self.context.append('</div>\n')

    # c3e20896d45729b3dd37b566def9e52a/full-test.py
    relative_path = Path(node['filename'])
    download_path = Path(self.builder.dlpath)
    # ../../_downloads/c3e20896d45729b3dd37b566def9e52a/full-test.py
    url = download_path.joinpath(relative_path)
    filename = relative_path.name

    # class="reference download internal"
    template = (
        '<div class="getthecode-header">\n'
        '  <ul>\n'
        '  <li class="getthecode-filename">{filename}</li>\n'
        '  <li class="getthecode-filename-link"><a href="{url}"><span>{filename}</span></a></li>\n'
    )
    notebook_path = node.get('notebook_path', None)
    if notebook_path is not None:
        notebook_filename = notebook_path.name
        notebook_url = download_path.joinpath(notebook_path)
        template += '  <li class="getthecode-notebook-link"><a href="{notebook_url}"><span>{notebook_filename}</span></a></li>\n'
    else:
        notebook_filename = None
        notebook_url = None
    # '<button id="copy-button" data-clipboard-target="clipboard_pre">Copy to Clipboard</button>'
    # '<pre id="clipboard_pre">' + node.rawsource + </pre>'
    template += (
        '  </ul>\n'
        '</div>\n'
    )
    self.body.append(template.format(
        filename=filename, url=url,
        notebook_filename=notebook_filename, notebook_url=notebook_url
    ))

    if node.rawsource != node.astext():
        # most probably a parsed-literal block -- don't highlight
        return BaseTranslator.visit_literal_block(self, node)

    lang = node.get('language', 'default')
    linenos = node.get('linenos', False)
    highlight_args = node.get('highlight_args', {})
    highlight_args['force'] = node.get('force', False)
    if lang is self.builder.config.highlight_language:
        # only pass highlighter options for original language
        opts = self.builder.config.highlight_options
    else:
        opts = {}

    highlighted = self.highlighter.highlight_block(
        node.rawsource, lang, opts=opts, linenos=linenos,
        location=(self.builder.current_docname, node.line), **highlight_args
    )

    _class = 'highlight-{}'.format(lang)
    if node.get('hidden', False):
        _class += ' highlight-hidden'
    starttag = self.starttag(node, 'div', suffix='', CLASS=_class)
    self.body.append(starttag + highlighted + '</div>\n')

    # Close the top div
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

def setup(app):

    # https://www.sphinx-doc.org/en/master/extdev/appapi.html#sphinx.application.Sphinx.add_js_file
    app.add_js_file('getthecode.js') # , async='async'

    app.add_node(
        GetTheCode,
        html=(visit_GetTheCode_html, depart_GetTheCode_html),
        # text=(visit_GetTheCode_text, depart_GetTheCode_text),
    )

    app.add_directive('getthecode', GetTheCodeDirective)

    app.connect('doctree-read', process_getthedoc)
