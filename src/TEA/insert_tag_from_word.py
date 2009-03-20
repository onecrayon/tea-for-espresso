'''Converts word or selection under the cursor into an open/close tag pair'''

import tea_actions as tea

def act(context, check_selfclosing=True, close_string=''):
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
    tag, new_range = tea.get_word_or_selection(context, range, alpha_only=False,
                                               extra_characters='')
    if tag == '':
        # No tag, so nothing further to do
        return False
    if not tag.isalpha():
        # There's a non-alpha character, so parse it
        opentag, closetag = tea.parse_tag(tag)
    else:
        opentag = closetag = tag
    # Construct the snippet and insert it
    if check_selfclosing and tea.is_selfclosing(closetag):
        snippet = '<' + opentag
        if opentag is closetag and not opentag in ['br', 'hr']:
            snippet += ' $1'
        snippet += close_string + '>$0'
    else:
        snippet = '<' + opentag + '>$1</' + closetag + '>$0'
    return tea.insert_snippet_over_range(context, snippet, new_range,
                                             'Insert Tag From Word')
