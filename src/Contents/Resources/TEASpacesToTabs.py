'''Class that allow TEA to convert between spaces and tabs for indenting'''

import re

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

from TEAforEspresso import TEAforEspresso
import tea_actions as tea

class TEASpacesToTabs(TEAforEspresso):
    '''Class for entabbing and detabbing current document or selection'''
    customSheet = objc.IBOutlet()
    numSpaces = objc.IBOutlet()
    spinner = objc.IBOutlet()
    
    @objc.signature('B@:@@')
    def performActionWithContext_error_(self, context, error):
        '''
        Gets the user's preferred number of spaces and switches the 
        indentation style accordingly
        '''
        # Load the sheet
        if not self.customSheet:
            NSBundle.loadNibNamed_owner_('TEASpacesPerTabsSheet', self)
        # Set up the default number
        prefs = tea.get_prefs(context)
        num_spaces = prefs.numberOfSpacesForTab()
        self.numSpaces.setStringValue_(num_spaces)
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.customSheet,
            context.windowForSheet(),
            self,
            'didEndSheet:returnCode:contextInfo:',
            None
        )
        # Save the context for later reference (once the sheet is complete)
        self.context = context
        # Because this gets passed through to Obj-C, using int prevents beeping
        return True
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 1)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 0)
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        def replacements(match):
            '''Utility function for replacing items'''
            return match.group(0).replace(self.search, self.replace)
        
        if code == 1:
            # Leave sheet open with "processing" spinner
            self.spinner.startAnimation_(self)
            
            spaces = int(self.numSpaces.stringValue())
            if self.action == 'entab':
                target = re.compile(r'^(\t* +\t*)+', re.MULTILINE)
                self.search = ' ' * spaces
                self.replace = '\t'
            else:
                target = re.compile(r'^( *\t+ *)+', re.MULTILINE)
                self.search = '\t'
                self.replace = ' ' * spaces
            insertions = tea.new_recipe()
            ranges = tea.get_ranges(self.context)
            if len(ranges) == 1 and ranges[0].length == 0:
                # No selection, use the document
                ranges[0] = tea.new_range(0, self.context.string().length())
            for range in ranges:
                text = tea.get_selection(self.context, range)
                # Non-Unix line endings will bork things; convert them
                text = tea.unix_line_endings(text)
                text = re.sub(target, replacements, text)
                if tea.get_line_ending(self.context) != '\n':
                    text = tea.clean_line_endings(self.context, text)
                insertions.addReplacementString_forRange_(text, range)
            insertions.setUndoActionName_(self.action.title())
            self.context.applyTextRecipe_(insertions)
            self.spinner.stopAnimation_(self)
        
        sheet.orderOut_(self)
