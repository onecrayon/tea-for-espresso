from Foundation import *
from AppKit import *
import objc

class TEASpacesPerTabsSheet(NSWindowController):
    numSpaces = objc.IBOutlet()
    
    @objc.IBAction
    def doSubmitSheet_(self, sender):
        spaces = self.numSpaces.stringValue()
        NSLog(spaces)
    
    @objc.IBAction
    def doCancelSheet_(self, sender):
        pass
