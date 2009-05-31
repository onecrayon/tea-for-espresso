'''Controller for TEA preferences window'''

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc

import tea_actions as tea
from tea_utils import refresh_symlinks
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
        prefs.retain()
        return True

class TEAPreferencesController(NSWindowController):
    
    @objc.IBAction
    def toggleUserDefaults_(self, sender):
        # Add or remove the symlinks
        bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso')
        refresh_symlinks(bundle.bundlePath(), True)
    
    @objc.IBAction
    def customActionsHelp_(self, sender):
        url = 'http://wiki.github.com/onecrayon/tea-for-espresso'
        NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(url))
    
    def windowWillClose_(self, notification):
        # Unless we retain then self-release, we'll lose the window to the
        # default garbage collector; this delegate method is automatic
        self.autorelease()
