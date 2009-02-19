'''
Textmate Emulation Actions for Espresso

A collection of Python scripts that enable useful actions
from Textmate into Espresso
'''

from Foundation import *
import objc

NSObject = objc.lookUpClass('NSObject')

class TEAforEspresso(NSObject):
    '''Docstring here'''
    
    # Don't need a signature definition if we return an object and all
    # arguments are objects
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        '''Required by Espresso; initializes the plugin settings'''
        self = super(TEAforEspresso, self).init()
        if self is None: return None
        self.target_action = dictionary.valueForKey_("target_action")
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        return True
    
    def performActionWithContext_error_(self, context):
        '''This function defines the primary class action logic'''
        # example:   `exec "import " + self.target_action`
        # example 2: `globals()[self.target_action](arguments)`
        #            `locals()[self.target_action](arguments)`
        return False
