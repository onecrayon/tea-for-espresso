'''Converts word or selection into an open/close tag pair'''

from Foundation import NSMakeRange, NSArray, NSValue

import tea_actions as tea

def act(context):
    '''
    Required action method
    
    Transforms the word under the cursor (or the word immediately previous
    to the cursor) into an open/close tag pair with the cursor in the middle
    
    If some text is selected, then it is turned into an open/close tag with
    attributes intelligently stripped from the closing tag.
    
    Inspired by Textmate's Insert Open/Close Tag (With Current Word)
    '''
    range = tea.get_single_range(context)
    if range == None:
        return False
    if range.length == 0:
        # Set up basic variables
        index = range.location
        tag = ''
        maxlength = context.string().length()
        # Make sure the cursor isn't at the end of the document
        if index != maxlength:
            # Check if cursor is mid-word
            char = tea.get_selection(context, NSMakeRange(index, 1))
            if char.isalpha():
                inword = True
                # Parse forward until we hit the end of word or document
                while inword:
                    char = tea.get_selection(context, NSMakeRange(index, 1))
                    if char.isalpha():
                        tag += char
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
                char = tea.get_selection(context, NSMakeRange(index, 1))
                if char.isalpha():
                    tag = char + tag
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
        # setSelectedRanges requires an array of ranges, which actually means
        # an array of NSValue range objects
        ranges = NSArray.arrayWithObjects_(NSValue.valueWithRange_(range))
        context.setSelectedRanges_(ranges)
        opentag = closetag = tag
    else:
        tag = tea.get_selection(context, range)
        # Parse the tag since there's almost certainly attributes
        opentag, closetag = tea.parse_tag(tag)
    # Construct the snippet and insert it
    snippet = '<' + opentag + '>$1</' + closetag + '>$0'
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             'Insert Tag From Word')
