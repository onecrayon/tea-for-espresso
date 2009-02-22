'''Utility functions for working with TEA for Espresso'''

from Foundation import *
import objc

from espresso import *

# ===============================================================
# Interact with the user
# ===============================================================

def ask(context, question, default=''):
    '''Displays a dialog box asking for user input'''
    return True

def say(context, title, message,
        main_button=None, alt_button=None, other_button=None):
    '''Displays a dialog with a message for the user'''
    alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
        title,
        main_button,
        alt_button,
        other_button,
        message
    )
    
    return alert.beginSheetModalForWindow_modalDelegate_didEndSelector_contextInfo_(
        context.windowForSheet(), None, None, None
    )

# ===============================================================
# Interact with the text window
# ===============================================================

def get_range_set(context):
    '''
    Returns the MRRangeSet for the selection in the current context
    
    For range set methods, see Espresso.app/Contents/Headers/MRRangeSet.h
    '''
    return MRRangeSet.alloc().initWithRangeValues_(context.selectedRanges())

def new_recipe():
    '''
    Shortcut to create a new text recipe
    
    For recipe methods, see Espresso.app/Contents/Headers/EspressoTextCore.h
    '''
    return CETextRecipe.textRecipe()

def snippet(snippet):
    '''Shortcut to create a new text snippet'''
    return CETextSnippet.snippetWithString_(snippet)
