'''
Textmate Emulation Actions for Espresso

A collection of Python scripts that enable useful actions
from Textmate into Espresso

Copyright (c) 2009 Ian Beck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

from Foundation import *
import objc

from tea_utils import *

# This really shouldn't be necessary thanks to the Foundation import
# but for some reason the plugin dies without it
NSObject = objc.lookUpClass('NSObject')

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
        # target_action is required; name of a Python TEA module
        self.target_action = dictionary["target_action"]
        
        # arguments is an optional dictionary with named extra arguments
        # for the act() call
        if "arguments" in dictionary:
            # In order to pass dictionary as keyword arguments it has to:
            # 1) be a Python dictionary
            # 2) have both the key and the value encoded as strings
            # This dictionary comprehension takes care of both issues
            self.arguments = dict(
                [str(arg), str(value)] \
                for arg, value in dictionary["arguments"].iteritems()
            )
        else:
            self.arguments = None
        
        # Append the bundle's resource path so that we can use common libraries
        sys.path.append(bundlePath + '/Contents/Resources/')
        self.bundle_path = bundlePath
        
        # Run one-time initialization items
        if not TEAforEspresso.initialized:
            TEAforEspresso.initialized = True
            refresh_symlinks()
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        return True
    
    def performActionWithContext_error_(self, context):
        '''Imports and calls the target_action's act() method'''
        target_module = load_action(self.target_action, self.bundle_path)
        if target_module is None:
            # Couldn't find the module, log the error
            NSLog('TEA: Could not find the module ' + self.target_action)
            return False
        if self.arguments != None:
            # We've got arguments, pass them as keyword arguments
            return target_module.act(context, **self.arguments)
        return target_module.act(context)
