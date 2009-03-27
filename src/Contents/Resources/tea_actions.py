'''Utility functions for working with TEA for Espresso'''

import re
from types import StringTypes

from Foundation import *

from espresso import *
import html_replace

# ===============================================================
# Interact with the user and output information
# ===============================================================

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
    if context.windowForSheet() is not None:
        return alert.beginSheetModalForWindow_modalDelegate_didEndSelector_contextInfo_(
            context.windowForSheet(), None, None, None
        )
    else:
        return alert.runModal()

def log(message):
    '''
    Convenience function for logging messages to console
    
    Please make sure they are strings before you try to log them; wrap
    anything you aren't sure of in str()
    '''
    NSLog(message)

# ===============================================================
# Text manipulations and helper functions
# ===============================================================

def parse_tag(opentag):
    '''
    Extract the tag from a string including optional attributes
    
    Returns the opentag (in case it included carets) and the closetag:
    parse_tag('p class="stuff"') => opentag = 'p class="stuff"', closetag = 'p'
    
    If you pass anything except an opening XML tag, the regex will fail
    '''
    matches = re.match(r'<?(([^\s]+)\s*.*)>?$', opentag)
    if matches == None:
        return None, None
    return matches.group(1), matches.group(2)

def is_selfclosing(tag):
    '''Checks a tag and returns True if it's a self-closing XHTML tag'''
    # For now, we're just checking off a list
    selfclosing = ['img', 'input', 'br', 'hr', 'link', 'base', 'meta']
    # Make sure we've just got the tag
    if not tag.isalpha():
        opentag, tag = parse_tag(tag)
    return tag in selfclosing

def encode_ampersands(text, enc='&amp;'):
    '''Encodes ampersands'''
    return re.sub('&(?!([a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', enc, text)

def named_entities(text):
    '''Converts Unicode characters into named HTML entities'''
    text = text.encode('ascii', 'html_replace')
    return encode_ampersands(text)

def numeric_entities(text, ampersands='named'):
    '''Converts Unicode characters into numeric HTML entities'''
    text = text.encode('ascii', 'xmlcharrefreplace')
    if ampersands == 'numeric':
        return encode_ampersands(text, '&#38;')
    else:
        return encode_ampersands(text)

# ===============================================================
# Preference lookup shortcuts
# ===============================================================

def get_prefs(context):
    '''
    Convenience function; returns the CETextPreferences object with
    current preferences
    '''
    return context.textPreferences()

def get_line_ending(context):
    '''Shortcut function to get the line-endings for the context'''
    prefs = get_prefs(context)
    return prefs.lineEndingString()

# ===============================================================
# Espresso object convenience methods
# ===============================================================

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

def new_snippet(snippet):
    '''
    Initializes a string as a CETextSnippet object
    '''
    return CETextSnippet.snippetWithString_(snippet)

# ===============================================================
# Working with ranges and selected text
# ===============================================================

def new_range(location, length):
    '''Convenience function for creating an NSRange'''
    return NSMakeRange(location, length)

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

def set_selected_range(context, range):
    '''Sets the selection to the single range passed as an argument'''
    context.setSelectedRanges_([NSValue.valueWithRange_(range)])

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

def get_word_or_selection(context, range, alpha_only=True,
                          extra_characters='_-'):
    '''
    Selects and returns the current word and its range from the passed range,
    or if there's already a selection returns the contents and its range
    
    By default it defines a word as a contiguous string of alphabetical
    characters. Setting alpha_only to False will define a word as a
    contiguous string of alpha-numeric characters plus extra_characters
    '''
    def test_alpha():
        # Mini-function to cut down on code bloat
        if alpha_only:
            return char.isalpha()
        else:
            return all(c.isalnum() or c in extra_characters for c in char)
    
    if range.length == 0:
        # Set up basic variables
        index = range.location
        word = ''
        maxlength = context.string().length()
        # Make sure the cursor isn't at the end of the document
        if index != maxlength:
            # Check if cursor is mid-word
            char = get_selection(context, NSMakeRange(index, 1))
            if test_alpha():
                inword = True
                # Parse forward until we hit the end of word or document
                while inword:
                    char = get_selection(context, NSMakeRange(index, 1))
                    if test_alpha():
                        word += char
                    else:
                        inword = False
                    index += 1
                    if index == maxlength:
                        inword = False
            else:
                # lastindex logic assumes we've been incrementing as we go,
                # so bump it up one to compensate
                index += 1
        lastindex = index - 1 if index < maxlength else index
        # Reset index to one less than the cursor
        index = range.location - 1
        # Only walk backwards if we aren't at the beginning
        if index > 0:
            # Parse backward to get the word ahead of the cursor
            inword = True
            while inword:
                char = get_selection(context, NSMakeRange(index, 1))
                if test_alpha():
                    word = char + word
                else:
                    inword = False
                index -= 1
                if index < 0:
                    inword = False
        # Since index is left-aligned and we've overcompensated,
        # need to increment +2
        firstindex = index + 2 if index > 0 else 0
        # Switch last index to length for use in range
        lastindex = lastindex - firstindex
        range = NSMakeRange(firstindex, lastindex)
        return word, range
    else:
        return get_selection(context, range), range

# ===============================================================
# Syntax zone methods
# ===============================================================

def get_root_zone(context):
    '''Returns the string identifier of the current root zone'''
    # This is terrible, but I can't find a good way to detect
    # if the object is null
    if context.syntaxTree().root().typeIdentifier() is not None:
        return context.syntaxTree().root().typeIdentifier().stringValue()
    else:
        return False

def get_active_zone(context, range):
    '''Returns the zone under the cursor'''
    # TODO: I need to implement better syntax zone sniffing to find
    #       the most applicable root zone available
    if context.syntaxTree().zoneAtCharacterIndex_(range.location) is not None:
        return context.syntaxTree().zoneAtCharacterIndex_(range.location).\
               typeIdentifier().stringValue()
    else:
        return False

# ===============================================================
# Snippet methods
# ===============================================================

def sanitize_for_snippet(text):
    '''
    Escapes special characters used by snippet syntax
    '''
    # text = text.replace('$', '\$')
    text = re.sub(r'\$(?!{|[0-9]|(SELECTED_TEXT)|(URL))', r'\$', text)
    return text.replace('`', '\`')

def construct_snippet(text, snippet):
    '''
    Constructs a simple snippet by replacing $SELECTED_TEXT with
    sanitized text
    '''
    text = sanitize_for_snippet(text)
    return snippet.replace('$SELECTED_TEXT', text)

# ===============================================================
# Insertion methods
# ===============================================================

def insert_text_over_range(context, text, range, undo_name=None):
    '''Immediately replaces the text at range with passed in text'''
    insertions = new_recipe()
    insertions.addReplacementString_forRange_(text, range)
    if undo_name != None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)

def insert_snippet(context, snippet):
    '''
    Convenience function to insert a text snippet
    
    Make sure to set the selection intelligently before calling this
    '''
    if type(snippet) in StringTypes:
        snippet = new_snippet(snippet)
    return context.insertTextSnippet_(snippet)

def insert_snippet_over_range(context, snippet, range, undo_name=None):
    '''Replaces text at range with a text snippet'''
    if range.length is not 0:
        # Need to first delete the text under the range
        deletions = new_recipe()
        deletions.addDeletedRange_(range)
        if undo_name != None:
            deletions.setUndoActionName_(undo_name)
        # Apply the deletions
        context.applyTextRecipe_(deletions)
    # Insert the snippet
    return insert_snippet(context, snippet)
