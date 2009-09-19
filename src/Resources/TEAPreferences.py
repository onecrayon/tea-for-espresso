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
    
    @objc.signature('B@:@@')
    def performActionWithContext_error_(self, context, error):
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
    '''
    Controls the actual preferences window; manages all tasks,
    and cleans it up afterward
    '''
    arrayController = objc.IBOutlet()
    tableView = objc.IBOutlet()
    
    @objc.IBAction
    def addListItem_(self, sender):
        '''Adds an item to a table, and selects it for editing'''
        self.arrayController.add_(sender)
        self.performSelector_withObject_afterDelay_(
            'editInsertedRow:', self.tableView, 0
        )
    
    def editInsertedRow_(self, tableView):
        '''
        Edits the most recently inserted row
        
        Many thank to Todd Ransom for pointing me in this direction!
        '''
        row = self.arrayController.arrangedObjects().count() - 1
        self.arrayController.setSelectionIndex_(row)
        tableView.editColumn_row_withEvent_select_(
            0, tableView.selectedRow(), None, True
        )
    
    @objc.IBAction
    def toggleUserActions_(self, sender):
        '''Performs the symlink refresh when custom user actions are toggled'''
        # Add or remove the symlinks
        bundle = NSBundle.bundleWithIdentifier_('com.onecrayon.tea.espresso')
        refresh_symlinks(bundle.bundlePath(), True)
    
    @objc.IBAction
    def customActionsHelp_(self, sender):
        '''Opens URL with help info for custom user actions'''
        url = 'http://wiki.github.com/onecrayon/tea-for-espresso'
        NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(url))
    
    def windowWillClose_(self, notification):
        '''Delegate method to auto-release everything'''
        # Unless we retain then self-release, we'll lose the window to the
        # default garbage collector; this delegate method is automatic
        self.autorelease()

class NilToString(NSValueTransformer):
    '''
    Transforms a nil value in a binding to an empty string
    
    Allows empty text fields to save empty strings to defaults
    '''
    @classmethod
    def transformedValueClass(cls):
        return NSString
    
    @classmethod
    def allowsReverseTransformation(cls):
        return True
    
    def transformedValue_(self, value):
        '''From defaults to text field'''
        return value
    
    def reverseTransformedValue_(self, value):
        '''From text field to defaults'''
        if value is None:
            return ''
        else:
            return value
