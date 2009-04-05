'''
Text Editor Actions Loader

A loader class to execute arbitrary shell scripts within Espresso
'''

from Foundation import *
import objc

import tea_actions as tea
from espresso import *

# This really shouldn't be necessary thanks to the Foundation import
# but for some reason the plugin dies without it
NSObject = objc.lookUpClass('NSObject')

class TEALoader(NSObject):
    '''
    Determines what info is necessary and feeds it to external scripts,
    then inserts their return value into the Espresso document
    '''
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        '''Required by Espresso; initializes the plugin settings'''
        self = super(TEALoader, self).init()
        if self is None: return None
        
        # Set object's internal variables
        
        # Set the syntax context
        if 'syntax-context' in dictionary:
            self.syntax_context = dictionary['syntax-context']
        else:
            self.syntax_context = None
        
        # By looking up the bundle, third party sugars can call
        # TEA for Espresso actions or include their own custom actions
        self.bundle_path = bundlePath
        
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        if self.syntax_context is not None:
            ranges = context.selectedRanges()
            range = ranges[0].rangeValue()
            selectors = SXSelectorGroup.selectorGroupWithString_(self.syntax_context)
            zone = context.syntaxTree().root().zoneAtCharacterIndex_(range.location);
            if selectors.matches_(zone):
                return True
            else:
                return False
        else:
            return True
    
    def performActionWithContext_error_(self, context):
        '''
        Gathers the necessary info, populates the environment, and runs
        the script
        '''
        pass
