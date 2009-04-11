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
    
    def performActionWithContext_error_(self, context):
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
        # False prevents Espresso from beeping
        return False
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 1)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 0)
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        if code == 1:
            NSLog('Processing...')
            # Leave sheet open with "processing" spinner
            self.spinner.startAnimation_(self)
            
            spaces = int(self.numSpaces.stringValue())
            if self.action == 'entab':
                target = re.compile(r' +')
                search = ' ' * spaces
                replace = '\t'
            else:
                target = re.compile(r'\t+')
                search = '\t'
                replace = ' ' * spaces
            insertions = tea.new_recipe()
            ranges = tea.get_ranges(self.context)
            if len(ranges) == 1 and ranges[0].length == 0:
                # No selection, use the document
                ranges[0] = tea.new_range(0, self.context.string().length())
            lines = self.context.lineStorage()
            for range in ranges:
                maxindex = range.location + range.length
                linenum = lines.lineNumberForIndex_(range.location)
                linerange = lines.lineRangeForLineNumber_(linenum)
                while linerange.location < maxindex:
                    match = target.match(tea.get_selection(
                        self.context, linerange
                    ))
                    if match:
                        new = match.group(0).replace(search, replace)
                        insertions.addReplacementString_forRange_(
                            new, tea.new_range(
                                linerange.location, len(match.group(0))
                            )
                        )
                    if (linerange.location + linerange.length) < maxindex:
                        linenum += 1
                        linerange = lines.lineRangeForLineNumber_(linenum)
                    else:
                        break
            insertions.setUndoActionName_(self.action.title())
            self.context.applyTextRecipe_(insertions)
            self.spinner.stopAnimation_(self)
        sheet.orderOut_(self)
