'''
Attempts to go to (select) a location in the document
'''

import re

import tea_actions as tea

def act(context, target=None, source=None, trim=False, discard_indent=False,
        search_string=None, regex=False):
    '''
    Required action method
    
    target dictates what we're looking for:
    - text
    - if unspecified, simply selects the source
    
    source dictates how to gather the string to search for:
    - word (word under the caret)
    - line (line under the caret)
    - if unspecified, defaults to selection
    
    Setting trim=True will cause the source to be trimmed
    
    Setting discard_indent=True will cause leading whitespace
    to be trimmed (unnecessary unless trim=True)
    
    search_string will set the string to search for if target is text or zone
    - $SELECTED_TEXT will be replaced with the source text
    
    Setting regex=True will cause search_string to be evaluated as regex
    '''
    range = tea.get_ranges(context)[0]
    if source == 'word':
        text, range = tea.get_word(context, range)
    elif source == 'line':
        text, range = tea.get_line(context, range)
    elif range.length > 0:
        text = tea.get_selection(context)
    
    # Make sure that we've got some text, even if it's an empty string
    if text is None:
        text = ''
    
    # Trim the source
    if trim:
        if discard_indent:
            trimmed = tea.trim(context, text, False)
        else:
            trimmed = tea.trim(context, text, False, 'end')
        
        start = text.find(trimmed)
        if start != -1:
            start = range.location + start
        length = len(trimmed)
        range = tea.new_range(start, length)
        text = trimmed
    
    if target is not None and text:
        if search_string is not None:
            search = search_string.replace('$SELECTED_TEXT', text)
        else:
            search = text
        # Find the start and end points of the substring
        start = end = None
        if regex:
            match = re.search(r'(' + search + r')', context.string())
            if match:
                # Get the start and end points
                start, end = match.span(1)
        else:
            start = context.string().find(search)
            if start != -1:
                end = start + len(start)
            else:
                start = None
        # Construct the new target range
        if start is not None and end is not None:
            range = tea.new_range(start, end - start)
    
    # Set the new range
    tea.set_selected_range(context, range)
    return True
