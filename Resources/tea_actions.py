'''Utility functions for working with TEA for Espresso'''

import re

from Foundation import *

from espresso import *

# ===============================================================
# Interact with the user and output information
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

def log(message):
    '''Convenience function for logging messages to console'''
    NSLog(message)

# ===============================================================
# Common text manipulations
# ===============================================================

def parse_tag(opentag):
    '''
    Convenience function to extract the tag from a string including
    attributes
    
    Returns the opentag (in case it included carets) and the closetag:
    parse_tag('p class="stuff"') => opentag = 'p class="stuff"', closetag = 'p'
    
    If you pass anything except an opening XML tag, the regex will fail
    '''
    matches = re.search(r'^<?(([^\s]+)\s*.*)>?$', opentag)
    if matches == None:
        return None, None
    return matches.group(1), matches.group(2)

# ===============================================================
# Preference lookup shortcuts
# ===============================================================

def get_prefs(context):
    '''
    Convenience function; returns a CETextPreferences object with
    current preferences
    '''
    return context.textPreferences()

def get_line_ending(context):
    prefs = get_prefs(context)
    return prefs.lineEndingString()

# ===============================================================
# Interact with the text window
# ===============================================================

def get_ranges(context):
    '''
    Convenience function to get a list of all ranges in the document
    
    Automatically cleans them up into NSRanges from NSConcreateValues
    '''
    ranges = context.selectedRanges()
    return [range.rangeValue() for range in ranges]

def get_selection(context, range):
    '''Convenience function; returns selected text within a given range'''
    return context.string().substringWithRange_(range)

def get_single_range(context, with_errors=True):
    '''
    Returns the range of a single selection, or throws an optional
    error if there are multiple selections
    '''
    ranges = context.selectedRanges()
    # Since there aren't good ways to deal with discontiguous selections
    # verify that we're only working with a single selection
    if len(ranges) != 1:
        if with_errors:
            say(
                context, "Error: multiple selections detected",
                "You must have a single selection in order to use this action."
            )
        return None
    # For some reason, range is not an NSRange; it's an NSConcreteValue
    # This converts it to an NSRange which we can work with
    return ranges[0].rangeValue()

def get_single_selection(context, with_errors=True):
    '''
    If there's a single selection, returns the selected text,
    otherwise throws optional descriptive errors
    
    Returns a tuple with the selected text first and its range second
    '''
    range = get_single_range(context, with_errors)
    if range == None:
        # More than one range, apparently
        return False
    if range.length is 0:
        if with_errors:
            say(
                context, "Error: selection required",
                "You must select some text in order to use this action."
            )
        return None, range
    return get_selection(context, range), range

def new_range_set(context):
    '''
    Convenience function; returns the MRRangeSet for the selection in
    the current context
    
    For range set methods, see Espresso.app/Contents/Headers/MRRangeSet.h
    '''
    return MRRangeSet.alloc().initWithRangeValues_(context.selectedRanges())

def new_recipe():
    '''
    Convenience function to create a new text recipe
    
    For recipe methods, see Espresso.app/Contents/Headers/EspressoTextCore.h
    '''
    return CETextRecipe.textRecipe()

def insert_text_over_selection(context, text, range, undo_name=None):
    '''Immediately replaces the text at range with passed in text'''
    insertions = new_recipe()
    insertions.addReplacementString_forRange_(text, range)
    if undo_name != None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)

# ===============================================================
# Snippet utilities
# ===============================================================

def sanitize_for_snippet(text):
    '''Escapes special characters used by snippet syntax'''
    text = text.replace('#', '\#')
    return text.replace('`', '\`')

def construct_tag_snippet(text, number=1, default_tag='p'):
    '''
    Sets up the standard single-tag snippet; can be repeated
    for a string of mirrored tags
    '''
    # Escape special snippet characters in the text
    text = sanitize_for_snippet(text)
    if number > 1:
        first_segment = '#1'
    else:
        first_segment = '#{1:' + default_tag + '}'
    return '<' + first_segment + '>' + text + '</#{1/\s.*//}>#0'

def insert_snippet(context, snippet):
    '''Convenience function to insert a text snippet'''
    snippet = CETextSnippet.snippetWithString_(snippet)
    return context.insertTextSnippet_(snippet)

def insert_snippet_over_selection(context, snippet, range, undo_name=None):
    '''Replaces text at range with a text snippet'''
    deletions = new_recipe()
    deletions.addDeletedRange_(range)
    if undo_name != None:
        deletions.setUndoActionName_(undo_name) 
    # Apply the deletions
    context.applyTextRecipe_(deletions)
    # Insert the snippet
    return insert_snippet(context, snippet)
