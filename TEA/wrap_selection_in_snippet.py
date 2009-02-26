'''Wraps the currently selected text in a snippet'''

import tea_actions as tea

def act(context, opensnippet='<#{1:p}>', closesnippet='</#{1/\s.*//}>#0',
        multi_opensnippet='<#1>', multi_closesnippet='</#{1/\s.*//}>',
        undo_name='Wrap Selection In Tag'):
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
    snippet = tea.construct_snippet(text, opensnippet, closesnippet)
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             undo_name)
