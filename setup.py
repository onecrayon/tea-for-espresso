# Usage: python setup.py py2app
# Dev:   python setup.py py2app -A
# Built plugin will show up in ./dist directory
# Install in the standard Sugars directory and relaunch Espresso to run

from distutils.core import setup
import py2app

setup(
    name='TEA for Espresso',
    plugin = ['TEAforEspresso.py'],
    data_files = [('../../TextActions', ['TextActions/Actions.xml',
                   'TextActions/Categories.xml'])],
    options=dict(py2app=dict(
        extension='.sugar',
        semi_standalone = True,
    )),
)