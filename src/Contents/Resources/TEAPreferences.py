'''Controller for TEA preferences window'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

from TEAforEspresso import TEAforEspresso
import tea_actions as tea
import BWToolkitFramework

class TEAPreferences(TEAforEspresso):
    '''Controller for TEA preference window'''
    customSheet = objc.IBOutlet()
    example = objc.IBOutlet()
    
    @objc.signature('B@:@')
    def performActionWithContext_error_(self, context):
        '''
        Presents a preferences window for the user to set TEA-specific
        preferences
        '''
        # Load the sheet
        if not self.customSheet:
            NSBundle.loadNibNamed_owner_('TEAPreferences', self)
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.customSheet,
            context.windowForSheet(),
            self,
            'didEndSheet:returnCode:contextInfo:',
            None
        )
        # Save the context for later reference (once the sheet is complete)
        self.context = context
        return True
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 1)
    
    @objc.IBAction
    def cancel_(self, sender):
        NSApp.endSheet_returnCode_(self.customSheet, 0)
    
    @AppHelper.endSheetMethod
    def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
        sheet.orderOut_(self)
