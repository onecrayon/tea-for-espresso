'''
This module enables on-the-fly loading of other TEA actions
(which are not, by default, in the system path)

Used by the main plugin initializer to find and load actions
'''

import imp
import sys
import os.path

def load_action(target):
    '''
    Imports target action file and returns it as a module
    
    Searches user override directory first, and then the default
    TEA scripts directory
    
    Usage: wrap_selection_in_tag = load_action('wrap_selection_in_tag')
    '''
    user_modules = os.path.expanduser(
        '~/Library/Application Support/Espresso/TEA/'
    )
    default_modules = os.path.expanduser(
        '~/Library/Application Support/Espresso/Sugars/'
        'TEA for Espresso.sugar/TEA/'
    )
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