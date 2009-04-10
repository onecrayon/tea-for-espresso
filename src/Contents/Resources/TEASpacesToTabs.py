'''Classes that allow TEA to convert between spaces and tabs for indenting'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

from TEAforEspresso import TEAforEspresso

class TEASpacesPerTabsSheet(NSWindowController):
    '''
    Defines the sheet necessary for choosing the number of spaces to equate
    with a tab
    '''
    numSpaces = objc.IBOutlet()
    customSheet = objc.IBOutlet()
    
    @classmethod
    def showSheetForWindow_delegate_(self, window, delegate):
        controller = self.alloc().initWithWindowNibName_('TEASpacesPerTabsSheet')
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            controller.window(),
            window,
            delegate,
            'didEndSheet:returnCode:info:',
            None
        )
        NSLog('sheet is up, returning')
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        spaces = self.numSpaces.stringValue()
        NSLog(spaces)
        NSApp.endSheet_returnCode_(self.customSheet(), 0)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet(), 0)


class TEASpacesToTabs(TEAforEspresso):
    '''Class for entabbing and detabbing current document or selection'''
    
    def performActionWithContext_error_(self, context):
        '''
        Gets the user's preferred number of spaces and switches the 
        indentation style accordingly
        '''
        NSLog('changing indent style')
        TEASpacesPerTabsSheet.showSheetForWindow_delegate_(
            context.windowForSheet(), self
        )
        return True
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_info(self, sheet, code, info):
        NSLog('we have a sheet response!')
