'''Converts word or selection into an open/close tag pair'''

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
    tag, new_range = tea.get_word_or_selection(context, range)
    if not tag.isalpha():
        # There's a non-alpha character, so parse it
        opentag, closetag = tea.parse_tag(tag)
    else:
        opentag = closetag = tag
    # Construct the snippet and insert it
    snippet = '<' + opentag + '>$1</' + closetag + '>$0'
    return tea.insert_snippet_over_selection(context, snippet, new_range,
                                             'Insert Tag From Word')
