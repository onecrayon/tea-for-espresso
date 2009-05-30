# Usage: python setup.py py2app
# Dev:   python setup.py py2app -A
# Built plugin will show up in ./dist directory
# Install in the standard Sugars directory and relaunch Espresso to run

from distutils.core import setup
import py2app
import os

# === CONFIG ===

# Update this info by hand; defines the required Info.plist elements
info = dict(
    CFBundleVersion = '1.0b13',
    CFBundleIdentifier = 'com.onecrayon.tea.espresso',
    NSHumanReadableCopyright = '(c) 2009 Ian Beck under the MIT license',
)

# Sets what directory to crawl for files to include
# Relative to location of setup.py; leave off trailing slash
includes_dir = 'src'

# Set the root directory for included files
# Relative to the bundle's Resources folder, so '../../' targets bundle root
includes_target = '../../'

# === END CONFIG ===


# Initialize an empty list so we can use list.append()
includes = []

# Walk the includes directory and include all the files
for root, dirs, filenames in os.walk(includes_dir):
    if root is includes_dir:
        final = includes_target
    else:
        final = includes_target + root[len(includes_dir)+1:] + '/'
    files = []
    for file in filenames:
        if (file[0] != '.'):
            files.append(os.path.join(root, file))
    includes.append((final, files))

# Here's where the magic happens
setup(
    name='TEA for Espresso',
    plugin = ['main.py'],
    data_files = includes,
    options=dict(py2app=dict(
        extension='.sugar',
        semi_standalone = True,
        site_packages = True,
        plist = info
    )),
)
