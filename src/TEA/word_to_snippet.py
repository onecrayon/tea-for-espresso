'''Converts word or selection under the cursor into a snippet'''

import tea_actions as tea

def act(context, default=None, alpha_numeric=True, extra_characters='',
        mode=None, undo_name=None, **syntaxes):
    '''
    Required action method
    
    Transforms the word under the cursor (or the word immediately previous
    to the cursor) into a snippet
    
    The snippet offers two placeholders:
    $SELECTED_TEXT: replaced with the word, or any selected text
    $WORD: if text is selected, replaced just with the first word
    '''
    if default is None:
        return False
    range = tea.get_single_range(context, True)
    if range == None:
        return False
    root_zone = tea.get_root_zone(context)
    if root_zone in syntaxes:
        snippet = syntaxes[root_zone]
    else:
        snippet = default
    # Check for specific zone override
    zone = tea.get_active_zone(context, range)
    if zone in syntaxes:
        snippet = syntaxes[zone]
    # Fetch the word
    word, new_range = tea.get_word_or_selection(context, range, alpha_numeric,
                                                extra_characters)
    if word == '':
        # No word, so nothing further to do
        return False
    # If we're using $WORD, make sure the word is just a word
    if snippet.find('$WORD') >= 0:
        fullword = word
        word = tea.parse_word(word)
    else:
        fullword = word
    
    # We've got some extra work if the mode is HTML
    # This is a really hacky solution, but I can't think of a concise way to
    # represent this functionality via XML
    if mode == 'HTML':
        if tea.is_selfclosing(word):
            snippet = '<' + fullword
            if fullword == word and not fullword in ['br', 'hr']:
                snippet += ' $1'
            snippet += word + '>$0'
    
    # Indent the snippet
    snippet = tea.indent_snippet(context, snippet, new_range)
    # Special replacement in case we're using $WORD
    snippet = snippet.replace('$WORD', word)
    # Construct the snippet
    snippet = tea.construct_snippet(fullword, snippet)
    return tea.insert_snippet_over_range(context, snippet, new_range, undo_name)
