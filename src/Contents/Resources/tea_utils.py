'''
This module includes common utility functions for working with
TEA actions

Most common usage is to find and load TEA actions
'''

import imp
import sys
import os

from Foundation import *

def load_action(target, *roots):
    '''
    Imports target TEA action file and returns it as a module
    (TEA modules are likely not, by default, in the system path)
    
    Searches user override directory first, and then the default
    TEA scripts directory in the Sugar bundle
    
    Usage: wrap_selection_in_tag = load_action('wrap_selection_in_tag')
    '''
    paths = [os.path.expanduser(
        '~/Library/Application Support/Espresso/TEA/Scripts/'
    )]
    for root in roots:
        paths.append(os.path.join(root, 'TEA/'))
    try:
        # Is the action already loaded?
        module = sys.modules[target]
    except (KeyError, ImportError):
        # Find the action (searches user overrides first)
        file, pathname, description = imp.find_module(target, paths)
        if file is None:
            # Action doesn't exist
            return None
        # File exists, load the action
        module = imp.load_module(
            target, file, pathname, description
        )
    return module

def refresh_symlinks(bundle_path, rebuild=False):
    '''
    Walks the file system and adds or updates symlinks to the TEA user
    actions folder
    '''
    def test_link(link, path):
        '''Utility function; tests if the symlink is pointing to the path'''
        if os.path.islink(link):
            if os.readlink(link) == path:
                return True
        return False
    
    defaults = NSUserDefaults.standardUserDefaults()
    enabled = defaults.boolForKey_('TEAEnableUserActions')
    sym_loc = bundle_path + '/TextActions/'
    if enabled:
        # user actions are enabled, so walk the user directory and refresh them
        user_dir = os.path.expanduser(
            '~/Library/Application Support/Espresso/TEA/TextActions/'
        )
        for root, dirs, filenames in os.walk(user_dir):
            # Rewrite dirs to only include folders that don't start with '.'
            dirs[:] = [dir for dir in dirs if not dir[0] == '.']
            basename = root[len(user_dir):].replace('/', '-')
            for file in filenames:
                if file[-3:] == 'xml':
                    ref = basename + file
                    # Make sure it's a unique filename
                    count = 1
                    refbase = ref[:-4]
                    prior_link = False
                    while os.path.exists(sym_loc + ref):
                        if test_link(sym_loc + ref, os.path.join(root, file)):
                            prior_link = True
                            break
                        else:
                            ref = str(count) + refbase + '.xml'
                            count += 1
                    if prior_link is False:
                        os.symlink(os.path.join(root, file), sym_loc + ref)
    elif rebuild:
        # user actions just disabled; remove any symlinks in the bundle
        for root, dirs, filenames in os.walk(sym_loc):
            for file in filenames:
                loc = os.path.join(root, file)
                if os.path.islink(loc):
                    os.remove(loc)
            break
