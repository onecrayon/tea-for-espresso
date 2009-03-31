'''
This module includes common utility functions for working with
TEA actions

Most common usage is to find and load TEA actions
'''

import imp
import sys
import os

from Foundation import *

def load_action(target, default_root):
    '''
    Imports target TEA action file and returns it as a module
    (TEA modules are likely not, by default, in the system path)
    
    Searches user override directory first, and then the default
    TEA scripts directory in the Sugar bundle
    
    Usage: wrap_selection_in_tag = load_action('wrap_selection_in_tag')
    '''
    user_modules = os.path.expanduser(
        '~/Library/Application Support/Espresso/TEA/Scripts/'
    )
    default_modules = os.path.join(default_root, 'TEA/')
    try:
        # Is the action already loaded?
        module = sys.modules[target]
    except (KeyError, ImportError):
        # Find the action (searches user overrides first)
        file, pathname, description = imp.find_module(
            target,
            [user_modules, default_modules]
        )
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
                    while os.path.exists(sym_loc + ref):
                        ref = ref[:-4] + str(count) + '.xml'
                        count += 1
                    os.symlink(os.path.join(root, file), sym_loc + ref)
    elif rebuild:
        # user actions just disabled; remove any symlinks in the bundle
        for root, dirs, filenames in os.walk(sym_loc):
            for file in filenames:
                loc = os.path.join(root, file)
                if os.path.islink(loc):
                    os.remove(loc)
            break
