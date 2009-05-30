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
    
    @objc.signature('B@:@')
    def performActionWithContext_error_(self, context):
        '''
        Presents a preferences window for the user to set TEA-specific
        preferences
        '''
        # Load the sheet
        prefs = TEAPreferencesController.alloc().initWithWindowNibName_(
        	'TEAPreferences'
        )
        prefs.showWindow_(self)
        prefs.window().center()
        return True

class TEAPreferencesController(NSWindowController):
	somevar = objc.IBOutlet()