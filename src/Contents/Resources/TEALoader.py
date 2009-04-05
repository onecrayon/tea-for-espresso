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
from truthy import *

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
        self.alt = dictionary['alternate'] if 'alternate' in dictionary else None
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
        # Environment variables that won't change with repetition
        os.putenv('SUGAR_BUNDLE', self.bundle_path)
        filepath = context.documentContext().fileURL()
        if filepath is not None:
            os.putenv('FILEPATH', filepath.absoluteString())
        os.putenv('ROOT_ZONE', tea.get_root_zone(context))
        # Set up the preferences
        prefs = tea.get_prefs(context)
        os.putenv('SOFT_TABS', prefs.insertsSpacesForTab())
        os.putenv('TAB_SIZE', prefs.numberOfSpacesForTab())
        os.putenv('LINE_ENDING', prefs.lineEndingString())
        
        # Initialize our common variables
        recipe = tea.new_recipe()
        ranges = tea.get_ranges(context)
        file = os.path.join(self.bundle_path, 'TEA', self.script)
        
        # There's always at least one range; this thus supports multiple
        # discontinuous selections
        for range in ranges:
            # These environment variables may change with repetition, so reset
            os.putenv(
                'LINE_NUMBER',
                context.lineStorage().lineNumberForIndex_(range.location)
            )
            os.putenv('ACTIVE_ZONE', tea.get_active_zone(context, range))
            if self.input == 'selection':
                input = text.get_selection(context, range)
                if input == '':
                    if self.alt == 'document':
                        input = context.string()
                    elif self.alt == 'line':
                        input, range = tea.get_line(context, range)
                    elif self.alt == 'word':
                        input, range = tea.get_word(context, range)
                    elif self.alt == 'character':
                        input, range = tea.get_character(context, range)
            elif self.input == 'document':
                input = context.string()
            else:
                input = ''
            # Run the script
            try:
                output, error = execute(file, input)
            except:
                # Most likely cause of failure is lack of executable status
                try:
                    os.chmod(file, 0755)
                    output, error = execute(file, input)
                except:
                    # Failed to execute completely, so exit with error
                    return tea.say(
                        context, 'Error: cannot execute script',
                        'Error: could not execute the script. Please contact '\
                        'the Sugar author.'
                    )
            # Log errors
            if error:
                tea.log(str(error))
            # Process the output
            if self.output == 'document':
                docrange = tea.new_range(0, context.string().length())
                recipe.addReplacementString_forRange_(output, docrange)
                break
            elif self.output == 'text':
                recipe.addReplacementString_forRange_(output, range)
            elif self.output == 'snippet':
                recipe.addDeletedRange_(range)
                break
        
        # If no output, we don't need to go any further
        if self.output is None:
            return True
        
        # Made it here, so apply the recipe and return
        if self.undo is not None:
            recipe.setUndoActionName_(self.undo)
        recipe.prepare()
        if recipe.numberOfChanges() > 0:
            response = context.applyTextRecipe_(recipe)
        else:
            response = True
        if self.output == 'snippet':
            response = tea.insert_snippet(context, output)
        return response
