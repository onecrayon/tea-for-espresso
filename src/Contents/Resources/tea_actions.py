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
    NSLog(str(message))

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

def get_indentation_string(context):
    '''Shortcut to retrieve the indentation string'''
    prefs = get_prefs(context)
    return prefs.tabString()

def get_xhtml_closestring():
    '''Retrieves the XHTML closing string (based on user preferences)'''
    defaults = NSUserDefaults.standardUserDefaults()
    return defaults.stringForKey_('TEASelfClosingString')

# ===============================================================
# Text manipulations and helper functions
# ===============================================================

def parse_word(selection):
    '''
    Extract the first word from a string
    
    Returns the word:
    parse_word('p class="stuff"') => word = 'p'
    '''
    matches = re.match(r'(([a-zA-Z0-9_-]+)\s*.*)$', selection)
    if matches == None:
        return None
    return matches.group(2)

def string_to_tag(string):
    '''
    Parses a string into a tag with id and class attributes
    
    For example, div#stuff.good.things translates into
    `div id="stuff" class="good things"`
    '''
    if string.find('#') > 0 or string.find('.') > 0:
        match = re.search('#([a-zA-Z0-9_-]+)', string)
        if match:
            id = match.group(1)
        else:
            id = False
        matches = re.findall('\.([a-zA-Z0-9_-]+)', string)
        classes = ''
        for match in matches:
            if classes:
                classes += ' '
            classes += match
        tag = parse_word(string)
        if id:
            tag += ' id="' + id + '"'
        if classes:
            tag += ' class="' + classes + '"'
        return tag
    else:
        return string

def is_selfclosing(tag):
    '''Checks a tag and returns True if it's a self-closing XHTML tag'''
    # For now, we're just checking off a list
    selfclosing = ['img', 'input', 'br', 'hr', 'link', 'base', 'meta']
    # Make sure we've just got the tag
    if not tag.isalnum():
        tag = parse_word(tag)
        if tag is None:
            return False
    return tag in selfclosing

def get_tag_closestring(context):
    '''
    Tries to determine if the current context is XHTML or not, and
    returns the proper string for self-closing tags
    '''
    # Currently doesn't run any logic; just defaults to user prefs
    defaults = NSUserDefaults.standardUserDefaults()
    use_xhtml = defaults.boolForKey_('TEADefaultToXHTML')
    if not use_xhtml:
        return ''
    return get_xhtml_closestring()

def encode_ampersands(text, enc='&amp;'):
    '''Encodes ampersands'''
    return re.sub('&(?!([a-zA-Z0-9]+|#[0-9]+|#x[0-9a-fA-F]+);)', enc, text)

def named_entities(text):
    '''Converts Unicode characters into named HTML entities'''
    text = text.encode('ascii', 'html_replace')
    return encode_ampersands(text)

def numeric_entities(text, ampersands=None):
    '''Converts Unicode characters into numeric HTML entities'''
    text = text.encode('ascii', 'xmlcharrefreplace')
    if ampersands == 'numeric':
        return encode_ampersands(text, '&#38;')
    elif ampersands == 'named':
        return encode_ampersands(text)
    else:
        return text

def entities_to_hex(text, wrap):
    '''
    Converts HTML entities into hexadecimal; replaces $HEX in wrap
    with the hex code
    '''
    # This is a bit of a hack to make the variable available to the function
    wrap = [wrap]
    def wrap_hex(match):
        hex = '%X' % int(match.group(2))
        while len(hex) < 4:
            hex = '0' + hex
        return wrap[0].replace('$HEX', hex)
    return re.sub(r'&(#x?)?([0-9]+|[0-9a-fA-F]+);', wrap_hex, text)

def trim(context, text, lines=True, sides='both', respect_indent=False,
         preserve_linebreaks=True):
    '''
    Trims whitespace from the text
    
    If lines=True, will trim each line in the text.
    
    sides can be both, start, or end and dictates where trimming occurs.
    
    If respect_indent=True, indent characters at the start of lines will be
    left alone (specific character determined by preferences)
    '''
    def trimit(text, sides, indent, preserve_linebreaks):
        '''Utility function for trimming the text'''
        # Preserve the indent if an indent string is passed in
        if (sides == 'both' or sides == 'start') and indent != '':
            match = re.match('(' + indent + ')+', text)
            if match:
                indent_chars = match.group(0)
            else:
                indent_chars = ''
        else:
            indent_chars = ''
        # Preserve the linebreaks at the end if needed
        match = re.search(r'[\n\r]+$', text)
        if match and preserve_linebreaks:
            linebreak = match.group(0)
        else:
            linebreak = ''
        # Strip that whitespace!
        if sides == 'start':
            text = text.lstrip()
        elif sides == 'end':
            text = text.rstrip()
        else:
            text = text.strip()
        return indent_chars + text + linebreak
    
    # Set up which characters to treat as indent
    if respect_indent:
        indent = get_indentation_string(context)
    else:
        indent = ''
    finaltext = ''
    if lines:
        for line in text.splitlines(True):
            finaltext += trimit(line, sides, indent, preserve_linebreaks)
    else:
        finaltext = trimit(text, sides, indent, preserve_linebreaks)
    return finaltext

def unix_line_endings(text):
    '''Converts all line endings to Unix'''
    if text.find('\r\n') != -1:
        text = text.replace('\r\n','\n')
    if text.find('\r') != -1:
        text = text.replace('\r','\n')
    return text

def clean_line_endings(context, text, line_ending=None):
    '''
    Converts all line endings to the default line ending of the file,
    or if line_ending is specified uses that
    '''
    text = unix_line_endings(text)
    if line_ending is None:
        target = get_line_ending(context)
    else:
        target = line_ending
    return text.replace('\n', target)

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

def get_line(context, range):
    '''Returns the line bounding range.location'''
    linerange = context.lineStorage().lineRangeForIndex_(range.location)
    return get_selection(context, linerange), linerange

def set_selected_range(context, range):
    '''Sets the selection to the single range passed as an argument'''
    context.setSelectedRanges_([NSValue.valueWithRange_(range)])

def get_single_range(context, with_errors=False):
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
    # Range is not an NSConcreteValue b/c it's stored in an array
    # This converts it to an NSRange which we can work with
    return ranges[0].rangeValue()

def get_single_selection(context, with_errors=False):
    '''
    If there's a single selection, returns the selected text,
    otherwise throws optional descriptive errors
    
    Returns a tuple with the selected text first and its range second
    '''
    range = get_single_range(context, with_errors)
    if range == None:
        # More than one range, apparently
        return None, None
    if range.length is 0:
        if with_errors:
            say(
                context, "Error: selection required",
                "You must select some text in order to use this action."
            )
        return None, range
    return get_selection(context, range), range

def get_character(context, range):
    '''Returns the character immediately preceding the cursor'''
    if range.location > 0:
        range = new_range(range.location - 1, 1)
        return get_selection(context, range), range
    else:
        return None, range

def get_word(context, range, alpha_numeric=True, extra_characters='_-',
             bidirectional=True):
    '''
    Selects and returns the current word and its range from the passed range
    
    By default it defines a word as a contiguous string of alphanumeric
    characters plus extra_characters. Setting alpha_numeric to False will
    define a word as a contiguous string of alphabetic characters plus
    extra_characters
    
    If bidirectional is False, then it will only look behind the cursor
    '''
    # Helper regex for determining if line ends with a tag
    # Includes checks for ASP/PHP/JSP/ColdFusion closing delimiters
    re_tag = re.compile(r'(<\/?[\w:-]+[^>]*|\s*(/|\?|%|-{2,3}))>$')
    
    def test_word():
        # Mini-function to cut down on code bloat
        if alpha_numeric:
            return all(c.isalnum() or c in extra_characters for c in char)
        else:
            return all(char.isalpha() or c in extra_characters for c in char)
    
    def ends_with_tag(cur_index):
        # Mini-function to check if line to index ends with a tag
        linestart = context.lineStorage().lineStartIndexLessThanIndex_(cur_index)
        text = get_selection(
            context, new_range(linestart, cur_index - linestart + 1)
        )
        return re_tag.search(text) != None
    
    # Set up basic variables
    index = range.location
    word = ''
    maxlength = context.string().length()
    if bidirectional:
        # Make sure the cursor isn't at the end of the document
        if index != maxlength:
            # Check if cursor is mid-word
            char = get_selection(context, new_range(index, 1))
            if test_word():
                inword = True
                # Parse forward until we hit the end of word or document
                while inword:
                    char = get_selection(context, new_range(index, 1))
                    if test_word():
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
    else:
        # Only parsing backward, so final index is cursor
        lastindex = range.location
    # Reset index to one less than the cursor
    index = range.location - 1
    # Only walk backwards if we aren't at the beginning
    if index >= 0:
        # Parse backward to get the word ahead of the cursor
        inword = True
        while inword:
            char = get_selection(context, new_range(index, 1))
            if test_word() and not (char == '>' and ends_with_tag(index)):
                word = char + word
                index -= 1
            else:
                inword = False
            if index < 0:
                inword = False
    # Since index is left-aligned and we've overcompensated,
    # need to increment +1
    firstindex = index + 1
    # Switch last index to length for use in range
    lastindex = lastindex - firstindex
    range = new_range(firstindex, lastindex)
    return word, range

def get_word_or_selection(context, range, alpha_numeric=True,
                          extra_characters='_-', bidirectional=True):
    '''
    Selects and returns the current word and its range from the passed range,
    or if there's already a selection returns the contents and its range
    
    See get_word() for an explanation of the extra arguments
    '''
    if range.length == 0:
        return get_word(context, range, alpha_numeric, extra_characters, bidirectional)
    else:
        return get_selection(context, range), range

# ===============================================================
# Syntax zone methods
# ===============================================================

def get_root_zone(context):
    '''
    DEPRECATED: use select_from_zones instead
    
    Returns the string identifier of the current root zone'''
    # This is terrible, but I can't find a good way to detect
    # if the object is null
    if context.syntaxTree().rootZone().typeIdentifier() is not None:
        return context.syntaxTree().rootZone().typeIdentifier().stringValue()
    else:
        return False

def get_active_zone(context, range):
    '''Returns the textual zone ID immediately under the cursor'''
    if context.syntaxTree().zoneAtCharacterIndex_(range.location) is not None:
        if context.syntaxTree().zoneAtCharacterIndex_(range.location).\
           typeIdentifier() is not None:
            return context.syntaxTree().zoneAtCharacterIndex_(range.location).\
                   typeIdentifier().stringValue()
    # Made it here, something's wrong
    return False

def select_from_zones(context, range=None, default=None, **syntaxes):
    '''
    Checks the keys in **syntaxes to see what matches the active zone,
    and returns that item's contents, or default if no match
    '''
    if range is None:
        range = get_single_range(context)
    for key, value in syntaxes.iteritems():
        selectors = SXSelectorGroup.selectorGroupWithString_(key)
        if context.string().length() == range.location:
            zone = context.syntaxTree().rootZone()
        else:
            zone = context.syntaxTree().rootZone().zoneAtCharacterIndex_(
                range.location
            )
        if selectors.matches_(zone):
            return value
    
    # If we reach this point, there's no match
    return default

def range_in_zone(context, range, selector):
    '''
    Tests the location of the range to see if it matches the provided
    zone selector string
    '''
    target = SXSelectorGroup.selectorGroupWithString_(selector)
    if context.string().length() == range.location:
        zone = context.syntaxTree().rootZone()
    else:
        zone = context.syntaxTree().rootZone().zoneAtCharacterIndex_(
            range.location
        )
    return target.matches_(zone)

def cursor_in_zone(context, selector):
    '''
    Tests the location of the range to see if it matches the provided
    zone selector string
    '''
    ranges = get_ranges(context)
    return range_in_zone(context, ranges[0], selector)

# ===============================================================
# Itemizer methods
# ===============================================================

def get_item_for_range(context, range):
    '''Returns the smallest item containing the given range'''
    return context.itemizer().smallestItemContainingCharacterRange_(range)

def get_item_parent_for_range(context, range):
    '''Returns the parent of the item containing the given range'''
    item = get_item_for_range(context, range)
    new_range = item.range()
    # Select the parent if the range is the same
    while(item.parent() and (new_range.location == range.location and \
          new_range.length == range.length)):
        item = item.parent()
        new_range = item.range()
    return item

# ===============================================================
# Snippet methods
# ===============================================================

def sanitize_for_snippet(text):
    '''
    Escapes special characters used by snippet syntax
    '''
    text = text.replace('$', '\$')
    text = text.replace('{', '\{')
    text = text.replace('}', '\}')
    return text.replace('`', '\`')

def construct_snippet(text, snippet):
    '''
    Constructs a simple snippet by replacing $SELECTED_TEXT with
    sanitized text
    '''
    if text is None:
        text = ''
    text = sanitize_for_snippet(text)
    return snippet.replace('$SELECTED_TEXT', text)

def indent_snippet(context, snippet, range):
    '''
    Sets a snippet's indentation level to match that of the line starting
    at the location of range
    '''
    # Are there newlines?
    if re.search(r'[\n\r]', snippet) is not None:
        # Check if line is indented
        line = context.lineStorage().lineRangeForIndex_(range.location)
        # Check if line is actually indented
        if line.location != range.location:
            line = get_selection(context, line)
            match = re.match(r'([ \t]+)', line)
            # Only indent if the line starts with whitespace
            if match is not None:
                current_indent = match.group(1)
                indent_string = get_indentation_string(context)
                # Convert tabs to indent_string and indent each line
                if indent_string != '\t':
                    snippet = snippet.replace('\t', indent_string)
                lines = snippet.splitlines(True)
                # Convert to iterator so we can avoid processing item 0
                lines = iter(lines)
                snippet = lines.next()
                for line in lines:
                    snippet += current_indent + line
                if re.search(r'[\n\r]$', snippet) is not None:
                    # Ends with a newline, add the indent
                    snippet += current_indent
    return snippet

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
    # Need context to get the tag closestring, so we do it here
    snippet = snippet.replace('$E_XHTML', get_tag_closestring(context))
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
