'''Classes that allow TEA to convert between spaces and tabs for indenting'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

from TEAforEspresso import TEAforEspresso


class TEASpacesToTabs(TEAforEspresso):
    '''Class for entabbing and detabbing current document or selection'''
    customSheet = objc.IBOutlet()
    numSpaces = objc.IBOutlet()
    
    def performActionWithContext_error_(self, context):
        '''
        Gets the user's preferred number of spaces and switches the 
        indentation style accordingly
        '''
        if not self.customSheet:
            NSBundle.loadNibNamed_owner_('TEASpacesPerTabsSheet', self)
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.customSheet,
            context.windowForSheet(),
            self,
            'didEndSheet:returnCode:contextInfo:',
            None
        )
        return True
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        spaces = self.numSpaces.stringValue()
        NSLog('spaces: ' + spaces)
        NSApp.endSheet_(self.window())
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_(self.window())
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        NSLog('time to process that sheet!')
        sheet.orderOut_(self)
