'''
Textmate Emulation Actions for Espresso

A collection of Python scripts that enable useful actions
from Textmate into Espresso
'''

import imp
import sys
import os.path

from Foundation import *
import objc

NSObject = objc.lookUpClass('NSObject')

class TEAforEspresso(NSObject):
    '''
    Performs initialization and is responsible for loading and calling
    the various external actions when the plugin is invoked
    '''
    
    # Don't need a signature definition if we return an object and all
    # arguments are objects
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        '''Required by Espresso; initializes the plugin settings'''
        self = super(TEAforEspresso, self).init()
        if self is None: return None
        
        # Set object's internal variables
        self.target_action = dictionary.valueForKey_("target_action")
        
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        return True
    
    def performActionWithContext_error_(self, context):
        '''Imports and calls the target_action's act() method'''
        self.target_module = self.import_action()
        if self.target_module is None:
            # Couldn't find the module, throw an error of some sort
            print('Could not find the module')
            return False
        return self.target_module.act()
    
    def import_action(self):
        user_modules = os.path.expanduser(
            '~/Library/Application Support/Espresso/TEA/'
        )
        default_modules = os.path.expanduser(
            '~/Library/Application Support/Espresso/Sugars/TEA for Espresso.sugar/TEA/'
        )
        try:
            # Is the action already loaded?
            module = sys.modules[self.target_action]
        except KeyError:
            # Find the action (searches user overrides first)
            file, pathname, description = imp.find_module(
                self.target_action,
                [user_modules, default_modules]
            )
            if file is None:
                # Action doesn't exist
                return None
            # File exists, load the action
            module = imp.load_module(
                self.target_action, file, pathname, description
            )
        return module
