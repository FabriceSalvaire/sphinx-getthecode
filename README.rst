==============================
 GetTheCode plugin for Sphinx
==============================

This plugin provides an enhanced ``literalinclude`` directive for `Sphinx`_ Documentation Generator.

Written by `Fabrice Salvaire <http://fabrice-salvaire.pagesperso-orange.fr>`_.

Installation
------------

See `sphinx-contrib`_ for more details.

To install the plugin, you have to run these commands:

.. code-block:: bash

    python setup.py build
    python setup.py install

The PySpice source code is hosted at https://github.com/FabriceSalvaire/sphinx-getthecode

To clone the Git repository, run this command in a terminal:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/sphinx-getthecode

Usage
-----

To load the plugin, you have to add it in your ``conf.py`` file.

.. code-block:: python

    extensions = [
      ...
      'sphinxcontrib.getthecode',
      ]

Directives
----------

This plugin adds a new directive ``getthecode`` which is equivalent to the ``literalinclude``
directive, but adds in front of the code block an header with the file name and an icon
to download the file.

  .. code-block:: ReST

    .. getthecode:: example.py
      :language: python

will result in:

  .. code-block:: html

    <div class="getthecode">
      <div class="getthecode-header">
        <span class="getthecode-filename">example.py</span>
        <a href="../../../_downloads/example.py"><span>example.py</span></a>
      </div>
      <div class="highlight-python">
        <div class="highlight"><pre>
        ...
        </pre></div>
      </div>
    </div>

To work properly, you must add some definitions in your CSS style, for example:

  .. code-block:: css

    div.getthecode {
      border-radius: 3px;
    }
    
    div.getthecode-header {
      padding: 5px;
      margin-bottom: 0px;
      border-bottom: 1px solid rgb(216, 216, 216);
      background-repeat: repeat-x;
      background-color: rgb(234, 234, 234);
      background-image: linear-gradient(rgb(250, 250, 250), rgb(234, 234, 234));
    }
    
    div.getthecode-header span {
    }
    
    div.getthecode-header a {
      margin-left: .5em;
      display: inline-block;
      background-image: url("file-text-small.png");
      background-repeat: no-repeat;
      width: 16px;
      height: 16px;
      /* text-indent :-9999px; */ /* hide text */
    }
    
    div.getthecode-header a span {
      display: none;
    }
    
    div.getthecode pre {
      margin-top: 0px;
      padding: 3px;
    }

.. .............................................................................

.. _Sphinx: http://sphinx-doc.org
.. _sphinx-contrib:  https://bitbucket.org/birkenfeld/sphinx-contrib

.. End
