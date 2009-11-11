'''Converts word or selection under the cursor into a snippet'''

import tea_actions as tea

from zencoding import zen_core, settings_loader

def act(context, default=None, alpha_numeric=True, extra_characters='',
        bidirectional=True, mode=None, close_string='', undo_name=None,
        **syntaxes):
    '''
    Required action method
    
    Transforms the word under the cursor (or the word immediately previous
    to the cursor) into a snippet (or processes it using zen-coding)
    
    The snippet offers two placeholders:
    $SELECTED_TEXT: replaced with the word, or any selected text
    $WORD: if text is selected, replaced just with the first word
    '''
    
    if default is None:
        return False
    range = tea.get_single_range(context, True)
    if range == None:
        return False
    # Check for specific zone override
    snippet = tea.select_from_zones(context, range, default, **syntaxes)
    # Fetch the word
    word, new_range = tea.get_word_or_selection(context, range, alpha_numeric,
                                                extra_characters, bidirectional)
    if word == '':
        # No word, so nothing further to do
        return False
    # If we're using $WORD, make sure the word is just a word
    if snippet.find('$WORD') >= 0:
        fullword = word
        word = tea.parse_word(word)
        if word is None:
            word = ''
    else:
        fullword = word
    
    # We've got some extra work if the mode is HTML or zen
    # This is a really hacky solution, but I can't think of a concise way to
    # represent this functionality via XML
    if mode == 'zen' and fullword.find(' ') < 0:
        # Explicitly load zen settings
        zen_settings = settings_loader.load_settings()
        zen_core.update_settings(zen_settings)
        
        # Set up the config variables
        zen_core.newline = tea.get_line_ending(context)
        zen_settings['variables']['indentation'] = tea.get_indentation_string(context)
        
        # This allows us to use smart incrementing tab stops in zen snippets
        point_ix = [0]
        def place_ins_point(text):
            point_ix[0] += 1
            return '$%s' % point_ix[0]
        zen_core.insertion_point = place_ins_point
    
        # Detect the type of document we're working with
        zones = {
            'css, css *': 'css',
            'xsl, xsl *': 'xsl',
            'xml, xml *': 'xml'
        }
        doc_type = tea.select_from_zones(context, range, 'html', **zones)
        
        # Setup the zen profile based on doc_type and XHTML status
        profile = {}
        if doc_type == 'html':
            close_string = tea.get_tag_closestring(context)
            if close_string == '/':
                profile['self_closing_tag'] = True
            elif close_string != ' /':
                profile['self_closing_tag'] = False
        elif doc_type == 'xml':
            profile = {'self_closing_tag': True, 'tag_nl': True}
        
        zen.setup_profile('tea_profile', profile)
        
        # Prepare the snippet
        snippet = zen_core.expand_abbreviation(fullword, doc_type, 'tea_profile')
    elif (mode == 'zen' or mode == 'html') and tea.is_selfclosing(word):
        # Self-closing, so construct the snippet from scratch
        snippet = '<' + fullword
        if fullword == word and not fullword in ['br', 'hr']:
            snippet += ' $1'
        snippet += '$E_XHTML>$0'
    # Indent the snippet
    snippet = tea.indent_snippet(context, snippet, new_range)
    # Special replacement in case we're using $WORD
    snippet = snippet.replace('$WORD', word)
    # Construct the snippet
    snippet = tea.construct_snippet(fullword, snippet)
    return tea.insert_snippet_over_range(context, snippet, new_range, undo_name)
