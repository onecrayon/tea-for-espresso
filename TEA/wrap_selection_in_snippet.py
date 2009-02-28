'''Wraps the currently selected text in a snippet'''

import tea_actions as tea

def act(context, first_snippet='<#{1:p}>$SELECTED_TEXT</#{1/\s.*//}>#0',
        following_snippet='<#1>$SELECTED_TEXT</#{1/\s.*//}>',
        final_append='', undo_name='Wrap Selection In Tag'):
    '''
    Required action method
    
    Wraps the selected text in a snippet
    
    Support for discontiguous selections will be implemented when recipes
    can support snippets; until then only opensnippet and closesnippet will
    be used
    '''
    # TODO: change to a loop once snippets in recipes are supported
    # This function will handle the logic of when to use open vs. multi
    text, range = tea.get_single_selection(context)
    if text == None:
        return False
    count = 1
    snippet = tea.construct_snippet(text, first_snippet)
    snippet += final_append
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             undo_name)
