'''
The main action class; responsible for dynamically loading generic Python
actions that use the TEA act() method
'''

from Foundation import *
import objc

from tea_utils import *
from espresso import *

class TEAforEspresso(NSObject):
    '''
    Performs initialization and is responsible for loading and calling
    the various external actions when the plugin is invoked
    '''
    # Class variable; allows us to do one-time initialization
    initialized = False
    
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        '''Required by Espresso; initializes the plugin settings'''
        self = super(TEAforEspresso, self).init()
        if self is None: return None
        
        # Set object's internal variables
        # action is required; name of a Python TEA module
        if 'target_action' in dictionary:
            # backwards compatible fix
            self.action = dictionary['target_action']
        else:
            self.action = dictionary["action"]
        
        # options is an optional dictionary with named extra arguments
        # for the act() call
        if 'arguments' in dictionary:
            # backwards compatible fix
            dictionary['options'] = dictionary['arguments']
        if "options" in dictionary:
            # In order to pass dictionary as keyword arguments it has to:
            # 1) be a Python dictionary
            # 2) have both the key and the value encoded as strings
            # This dictionary comprehension takes care of both issues
            self.options = dict(
                [str(arg), str(value)] \
                for arg, value in dictionary["options"].iteritems()
            )
        else:
            self.options = None
        
        # Set the syntax context
        if 'syntax-context' in dictionary:
            self.syntax_context = dictionary['syntax-context']
        else:
            self.syntax_context = None
        
        # By looking up the bundle, third party sugars can call
        # TEA for Espresso actions or include their own custom actions
        self.bundle_path = bundlePath
        self.tea_bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso').\
                          bundlePath()
        if self.bundle_path == self.tea_bundle:
            self.search_paths = [self.bundle_path]
        else:
            self.search_paths = [self.bundle_path, self.tea_bundle]
        
        # Run one-time initialization items
        if not TEAforEspresso.initialized:
            TEAforEspresso.initialized = True
            refresh_symlinks(self.tea_bundle)
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        if self.syntax_context is not None:
            ranges = context.selectedRanges()
            range = ranges[0].rangeValue()
            selectors = SXSelectorGroup.selectorGroupWithString_(self.syntax_context)
            zone = context.syntaxTree().root().zoneAtCharacterIndex_(range.location)
            if selectors.matches_(zone):
                return True
            else:
                return False
        else:
            return True
    
    def performActionWithContext_error_(self, context):
        '''Imports and calls the action's act() method'''
        target_module = load_action(self.action, *self.search_paths)
        if target_module is None:
            # Couldn't find the module, log the error
            NSLog('TEA: Could not find the module ' + self.action)
            return False
        if self.options != None:
            # We've got options, pass them as keyword arguments
            return target_module.act(context, **self.options)
        return target_module.act(context)