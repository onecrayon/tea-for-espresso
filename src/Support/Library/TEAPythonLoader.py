'''
The class responsible for loading the action and interacting with the
TEAforEspresso class
'''

from Foundation import *
import objc

from tea_utils import load_action

class TEAPythonLoader(NSObject):
    @objc.signature('B@:@@')
    def actInContext_forAction_(self, context, actionObject):
        '''This actually performs the Python action'''
        # Grab variables from the actionObject
        action = actionObject.action()
        paths = actionObject.supportPaths()
        
        if actionObject.options() is not None:
            # In order to pass dictionary as keyword arguments it has to:
            # 1) be a Python dictionary
            # 2) have the key encoded as a string
            # This dictionary comprehension takes care of both issues
            options = dict(
                [str(arg), value] \
                for arg, value in actionObject.options().iteritems()
            )
        else:
            options = None
        
        # Find and run the action
        target_module = load_action(action, *paths)
        if target_module is None:
            # Couldn't find the module, log the error
            NSLog('TEA: Could not find the module ' + action)
            return False
        
        # We may need to pass the action object as the second argument
        if "req_action_object" in target_module.__dict__ and \
           target_module.req_action_object:
            if options is not None:
                return target_module.act(context, actionObject, **options)
            else:
                return target_module.act(context, actionObject)
        elif options is not None:
            # We've got options, pass them as keyword arguments
            return target_module.act(context, **options)
        else:
            return target_module.act(context)
