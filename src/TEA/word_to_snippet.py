'''Converts word or selection under the cursor into a snippet'''

import tea_actions as tea

from zencoding import zen_core
from zencoding.settings import zen_settings

def act(context, default=None, alpha_numeric=True, extra_characters='',
        mode=None, close_string='', undo_name=None, **syntaxes):
    '''
    Required action method
    
    Transforms the word under the cursor (or the word immediately previous
    to the cursor) into a snippet
    
    The snippet offers two placeholders:
    $SELECTED_TEXT: replaced with the word, or any selected text
    $WORD: if text is selected, replaced just with the first word
    '''
    # If we're using zen-coding, set up the config variables
    if mode == 'zen':
        zen_core.newline = tea.get_line_ending(context)
        zen_core.insertion_point = '$1'
        zen_core.sub_insertion_point = '$2'
        zen_settings['indentation'] = tea.get_indentation_string(context)
        # Need to detect the document type (html, css, xml, xsl)
        # Currently defaulting to HTML
        doc_type = 'html'
    
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
        if word is None:
            word = ''
    else:
        fullword = word
    
    # We've got some extra work if the mode is HTML
    # This is a really hacky solution, but I can't think of a concise way to
    # represent this functionality via XML
    if mode == 'zen':
        snippet = zen_core.expand_abbr(fullword, doc_type)
        snippet = tea.indent_snippet(context, snippet, new_range)
        snippet += '$0'
    else:
        # Indent the snippet
        snippet = tea.indent_snippet(context, snippet, new_range)
        # Special replacement in case we're using $WORD
        snippet = snippet.replace('$WORD', word)
        # Construct the snippet
        snippet = tea.construct_snippet(fullword, snippet)
    return tea.insert_snippet_over_range(context, snippet, new_range, undo_name)
