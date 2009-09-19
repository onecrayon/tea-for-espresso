'''
A stub class; used as a common ancestor to share methods between TEA classes
'''

import os.path

from Foundation import *
import objc

from espresso import *

class TEAGenericAction(NSObject):
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        self = super(TEAGenericAction, self).init()
        if self is None: return None
        # Set the syntax context
        self.syntax_context = dictionary['syntax-context'] if \
                              'syntax-context' in dictionary else None
        # Set the selection context
        self.selection_context = dictionary['selection-context'] if \
                                 'selection-context' in dictionary else None
        # By looking up the bundle, third party sugars can call
        # TEA for Espresso actions or include their own custom actions
        self.bundle_path = bundlePath
        self.tea_path = NSBundle.bundleWithIdentifier_(
            'com.onecrayon.tea.espresso'
        ).bundlePath()
        # Sets up root_paths, which tracks the possible locations
        # of Support folders
        self.root_paths = [os.path.expanduser(
            '~/Library/Application Support/Espresso/'
        ), self.bundle_path]
        if self.bundle_path != self.tea_path:
            self.root_paths.append(self.tea_path)
        
        return self
    
    # Signature is necessary for Objective-C to be able to find the method
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
        '''Returns bool; can the action be performed in the given context'''
        # Possible for context to be empty if it's partially initialized
        if context.string() is None:
            return False
        # By default, allow actions to be run
        possible = True
        if self.syntax_context is not None:
            ranges = context.selectedRanges()
            range = ranges[0].rangeValue()
            selectors = SXSelectorGroup.selectorGroupWithString_(self.syntax_context)
            if context.string().length() == range.location:
                zone = context.syntaxTree().rootZone()
            else:
                zone = context.syntaxTree().rootZone().zoneAtCharacterIndex_(
                    range.location
                )
            if not selectors.matches_(zone):
                possible = False
        if self.selection_context is not None:
            # selection_context might be none, one, one+, or multiple
            ranges = context.selectedRanges()
            if len(ranges) == 1:
                if self.selection_context.lower() == 'multiple':
                    possible = False
                elif ranges[0].rangeValue().length > 0 and \
                     self.selection_context.lower() == 'none':
                    possible = False
                elif ranges[0].rangeValue().length == 0 and \
                     (self.selection_context.lower() == 'one' or\
                     self.selection_context.lower() == 'one+'):
                    possible = False
            elif self.selection_context.lower() != 'multiple' or\
                 self.selection_context.lower() != 'one+':
                possible = False
        
        return possible
