==============================
 GetTheCode plugin for Sphinx
==============================

This plugin provides an enhanced ``literalinclude`` directive for `Sphinx`_ Documentation Generator.

Installation
------------

See `sphinx-contrib`_ for more details.

To install the plugin, you have to run these commands:

.. code-block:: bash

    python setup.py build
    python setup.py install

Usage
-----

To load the plugin, you have to add it in your ``conf.py`` file.

.. code-block:: python

    extensions = [
      ...
      'sphinxcontrib.getthecode',
      ]

Usage
-----

.. .............................................................................

.. _Sphinx: http://sphinx-doc.org
.. _sphinx-contrib:  https://bitbucket.org/birkenfeld/sphinx-contrib

.. End
