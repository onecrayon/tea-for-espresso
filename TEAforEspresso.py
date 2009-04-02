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
        
        # Append the bundle's resource path so that we can use common libraries
        self.bundle_path = bundlePath
        # By looking up the bundle, third party sugars can call
        # TEA for Espresso actions, which is pretty cool
        bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso')
        self.tea_bundle = bundle.bundlePath()
        sys.path.append(self.tea_bundle + '/Contents/Resources/')
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
