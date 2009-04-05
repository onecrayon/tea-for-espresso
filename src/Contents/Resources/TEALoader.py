'''
Text Editor Actions Loader

A loader class to execute arbitrary shell scripts within Espresso
'''

import subprocess
import os

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
        self.script = dictionary['script'] if 'script' in dictionary else None
        self.input = dictionary['input'] if 'input' in dictionary else None
        self.alternative = dictionary['alternative'] \
                           if 'alternative' in dictionary else None
        self.output = dictionary['output'] if 'output' in dictionary else None
        self.undo = dictionary['undo_name'] if 'undo_name' in dictionary else None
        
        # Set the syntax context
        self.syntax_context = dictionary['syntax-context'] \
                              if 'syntax-context' in dictionary else None
        
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
            zone = context.syntaxTree().root().zoneAtCharacterIndex_(range.location)
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
        def execute(file, input):
            '''Utility function for running the script'''
            script = subprocess.Popen(
                [file],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return script.communicate(input)
        
        if self.script is None:
            return False
        # Set up the environment
        # USE: os.putenv('VARNAME', 'var value')
        
        # Get the requested info
        # EXAMPLE: input, range = tea.get_single_selection(context)
        
        # Run the script
        file = os.path.join(self.bundle_path, 'TEA', self.script)
        try:
            output, error = execute(file, input)
        except:
            # Most likely cause of failure is lack of executable status on file
            try:
                os.chmod(file, 0755)
                output, error = execute(file, input)
            except:
                # Likely failure is inability to set executable status, so exit
                return tea.say(
                    context, 'Error: cannot execute script',
                    'Error: could not execute the script. Please contact the '\
                    'Sugar author.'
                )
        # Process the output
        return True
