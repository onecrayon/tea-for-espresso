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
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        spaces = self.numSpaces.stringValue()
        NSLog(spaces)
    
    @objc.IBAction
    def cancel_(self, sender):
        pass

class TEASpacesToTabs(TEAforEspresso):
    '''Class for entabbing and detabbing current document or selection'''
    
    def performActionWithContext_error_(self, context):
        '''
        Gets the user's preferred number of spaces and switches the 
        indentation style accordingly
        '''
        tea_bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso')
        NSBundle.loadNibNamed_owner_('SpacesPerTabsSheet', tea_bundle)
        NSLog('changing indent style')
        return True
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_info(self, sheet, code, info):
        pass
