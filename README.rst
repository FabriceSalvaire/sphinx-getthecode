.. |Pypi Version| image:: https://img.shields.io/pypi/v/sphinxcontrib-getthecode.svg
   :target: https://pypi.python.org/pypi/sphinxcontrib-getthecode
   :alt: sphinxcontrib-getthecode last version

.. |Pypi License| image:: https://img.shields.io/pypi/l/sphinxcontrib-getthecode.svg
   :target: https://pypi.python.org/pypi/sphinxcontrib-getthecode
   :alt: sphinxcontrib-getthecode license

.. |Pypi Python Version| image:: https://img.shields.io/pypi/pyversions/sphinxcontrib-getthecode.svg
   :target: https://pypi.python.org/pypi/sphinxcontrib-getthecode
   :alt: sphinxcontrib-getthecode python version

.. |Python| replace:: Python
.. _Python: http://python.org

.. |PyPI| replace:: PyPI
.. _PyPI: https://pypi.python.org/pypi

.. |Sphinx| replace:: Sphinx
.. _Sphinx: http://sphinx-doc.org

==============================
 GetTheCode plugin for Sphinx
==============================

|Pypi License|
|Pypi Python Version|

|Pypi Version|

This plugin implements an enhanced ``literalinclude`` directive for the `Sphinx`_ Documentation Generator.

For a demo, look at `Pyterate <https://github.com/FabriceSalvaire/Pyterate>`_.

Authored by `Fabrice Salvaire <http://fabrice-salvaire.fr>`_.

Source code is hosted at https://github.com/FabriceSalvaire/sphinx-getthecode

Installation
------------

Using ``pip``:

.. code-block:: bash

    pip install sphinxcontrib-getthecode

Else clone the Git repository:

.. code-block:: sh

  git clone git@github.com:FabriceSalvaire/sphinx-getthecode

then install the plugin using:

.. code-block:: bash

    python setup.py install

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

This plugin implements a directive ``getthecode`` which is equivalent to the ``literalinclude``
directive, but it adds a header before the ``pre`` element.  This header contains the file name and
a link to download the file.

.. code-block:: ReST

    .. getthecode:: example.py
        :language: python3
        :hidden: ### optional, add a class highlight-hidden

will result in:

.. code-block:: html

    <div class="getthecode">
        <div class="getthecode-header">
    	<ul>
    	    <li class="getthecode-filename">example.py</li>
    	    <li class="getthecode-filename-link">
    		<a href="../../_downloads/example.py">
    		    <span>example.py</span>
    		    <i class="fa fa-download" aria-hidden="true"></i>
    		</a></li>
    	    <li class="show-code-button" title="Show/Hide the code">
    		<i class="fa fa-eye" aria-hidden="true"></i>
    		<i class="fa fa-eye-slash" aria-hidden="true" style="display: none;"></i>
    	    </li></ul>
        </div>
        <div class="highlight-python3 highlight-hidden" style="display: none;">
    	<div class="highlight">
    	    <pre>
	    ...
    	    </pre>
    	</div>
        </div>
    </div>

You can find in the ``static`` directory an example of **CSS stylesheet** and a **Javascript code to show/hide the code**.
