# twine
[![Build Status](https://travis-ci.org/joshuacurl/twine.svg?branch=master)](https://travis-ci.org/joshuacurl/twine)

twine is a simple scripting language for automated Web browsing and testing.  With twine, you can programmatically navigate through sites that use all standard Web features including forms, cookies, and JavaScript.

twine builds on the [twill](https://github.com/ctb/twill) scripting language and includes large portions of its code.

## Install

twine requires PyQt4, which cannot be installed via pip, and the development libraries for Python and X11. Most Linux distributions have packages for these. On Ubuntu, for example, you can install python-qt4, python-dev, and libx11-dev.

The remaining dependencies can be installed via pip:

    pip install -r requirements.txt

Lastly, to install twine itself run:

    python setup.py install

## Run

When run without any arguments twine will run in interactive mode.

You can also provide twine with one or more scripts. For example:

    twine script1.twine script2.twine ...
