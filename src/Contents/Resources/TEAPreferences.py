'''Controller for TEA preferences window'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

import tea_actions as tea
import BWToolkitFramework

class TEAPreferences(NSObject):
    '''Controller for TEA preference window'''
    
    def initWithDictionary_bundlePath_(self, dictionary, bundlePath):
        '''Required by Espresso; initializes the plugin settings'''
        self = super(TEAPreferences, self).init()
        if self is None: return None
        return self
    
    @objc.signature('B@:@')
    def canPerformActionWithContext_(self, context):
    	return True
    
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
        prefs.setShouldCascadeWindows_(False)
        prefs.window().setFrameAutosaveName_('TEAPreferences')
        prefs.showWindow_(self)
        return True

class TEAPreferencesController(NSWindowController):
	somevar = objc.IBOutlet()
