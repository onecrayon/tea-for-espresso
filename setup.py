# Usage: python setup.py py2app
# Dev:   python setup.py py2app -A
# Built plugin will show up in ./dist directory
# Install in the standard Sugars directory and relaunch Espresso to run

from distutils.core import setup
import py2app
import os


def include_files(path):
    '''
    Walks a given folder and returns a list of its contents
    
    List includes the folder's name (so that we can use it with data_files)
    '''
    files = []
    for root, dirs, filenames in os.walk(path):
        if filenames:
            for file in filenames:
                # Don't include hidden files
                if (file[0] != '.'):
                    files.append(os.path.join(root, file))
    return files


# Configure this by hand for any included directories
includes = [
    ('../../TextActions', include_files('./TextActions')),
    ('../../TEA', include_files('./TEA')),
    ('./', include_files('./Resources')),
]

setup(
    name='TEA for Espresso',
    plugin = ['TEAforEspresso.py'],
    data_files = includes,
    options=dict(py2app=dict(
        extension='.sugar',
        semi_standalone = True,
    )),
)