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
        #self.changesToUppercase = dictionary.objectForKey_("change-to").\
        #                          isEqualToString_("uppercase")
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        return True
    
    def performActionWithContext_error_(self, context):
        '''This function defines the primary class action logic'''
        
        return False
