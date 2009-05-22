'''Converts word or selection under the cursor into a snippet'''

import tea_actions as tea

from zencoding import zen_core
from zencoding.settings import zen_settings

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
    if mode == 'zen':
        # Set up the config variables
        zen_core.newline = tea.get_line_ending(context)
        # This allows us to use smart incrementing tab stops in zen snippets
        global point_ix
        point_ix = 0
        def place_ins_point(text):
            globals()['point_ix'] += 1
            return '$%s' % point_ix
        zen_core.insertion_point = place_ins_point
        zen_core.sub_insertion_point = place_ins_point
        zen_settings['indentation'] = tea.get_indentation_string(context)
        # Detect the type of document we're working with
        zones = {
            'css, css *': 'css',
            'xsl, xsl *': 'xsl',
            'xml, xml *': 'xml'
        }
        doc_type = tea.select_from_zones(context, default='html', **zones)
        
        # Prepare the snippet
        snippet = zen_core.expand_abbr(fullword, doc_type)
        snippet = tea.indent_snippet(context, snippet, new_range)
        snippet += '$0'
        tea.log(snippet)
    else:
        if mode == 'HTML':
            # If no spaces, might be a hashed shortcut tag
            if fullword.find(' ') < 0:
                fullword = tea.string_to_tag(fullword)
            if tea.is_selfclosing(word):
                snippet = '<' + fullword
                if fullword == word and not fullword in ['br', 'hr']:
                    snippet += ' $1'
                snippet += close_string + '>$0'
        # Indent the snippet
        snippet = tea.indent_snippet(context, snippet, new_range)
        # Special replacement in case we're using $WORD
        snippet = snippet.replace('$WORD', word)
        # Construct the snippet
        snippet = tea.construct_snippet(fullword, snippet)
    return tea.insert_snippet_over_range(context, snippet, new_range, undo_name)
