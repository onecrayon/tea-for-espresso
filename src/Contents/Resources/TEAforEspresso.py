'''
The main action class; responsible for dynamically loading generic Python
actions that use the TEA act() method
'''

from Foundation import *
import objc

from TEAGenericAction import TEAGenericAction
from tea_utils import *

class TEAforEspresso(TEAGenericAction):
    '''
    Performs initialization and is responsible for loading and calling
    the various external actions when the plugin is invoked
    '''
    # Class variable; allows us to do one-time initialization
    initialized = False
    
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        '''Required by Espresso; initializes the plugin settings'''
        # Call the generic action's init method
        self = super(TEAforEspresso, self).initWithDictionary_bundlePath_(
            dictionary, bundlePath
        )
        if self is None: return None
        
        # Set object's internal variables
        # action is required; name of a Python TEA module
        if 'target_action' in dictionary:
            # backwards compatible fix
            self.action = dictionary['target_action']
        else:
            self.action = dictionary['action'] if 'action' in dictionary else \
                          None
        
        # options is an optional dictionary with named extra arguments
        # for the act() call
        if 'arguments' in dictionary:
            # backwards compatible fix
            dictionary['options'] = dictionary['arguments']
        if 'options' in dictionary:
            # In order to pass dictionary as keyword arguments it has to:
            # 1) be a Python dictionary
            # 2) have the key encoded as a string
            # This dictionary comprehension takes care of both issues
            self.options = dict(
                [str(arg), value] \
                for arg, value in dictionary['options'].iteritems()
            )
        else:
            self.options = None
        
        # Run one-time initialization items
        if not TEAforEspresso.initialized:
            TEAforEspresso.initialized = True
            # Add default preferences to shared user defaults
            bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso')
            defaults = NSUserDefaults.standardUserDefaults()
            defaults.registerDefaults_(NSDictionary.dictionaryWithContentsOfFile_(
                bundle.pathForResource_ofType_('Defaults', 'plist')
            ))
            refresh_symlinks(self.tea_path)
        return self
    
    @objc.signature('B@:@@')
    def performActionWithContext_error_(self, context, error):
        '''Imports and calls the action's act() method'''
        target_module = load_action(self.action, *self.root_paths)
        if target_module is None:
            # Couldn't find the module, log the error
            NSLog('TEA: Could not find the module ' + self.action)
            return False
        if self.options != None:
            # We've got options, pass them as keyword arguments
            return target_module.act(context, **self.options)
        return target_module.act(context)
