'''
The class responsible for loading the action and interacting with the
TEAforEspresso class
'''

from Foundation import *
import objc

class TEAPythonLoader(NSObject):
    @objc.signature('B@:@@@')
    def actInContext_withOptions_forAction_(self, context, options, actionObject):
        '''This actually performs the Python action'''
        # For now, just verify that the damn thing works
        NSLog("Action fired: " + actionObject.action())
        
        return True;
