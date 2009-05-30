'''Wraps the currently selected text in a snippet'''

import tea_actions as tea

def act(context, first_snippet='', following_snippet='',
        final_append='', undo_name=None):
    '''
    Required action method
    
    Wraps the selected text in a snippet
    
    Support for discontiguous selections will be implemented when recipes
    can support snippets; until then only first_snippet will be used
    '''
    # TODO: change to a loop once snippets in recipes are supported
    # This function will handle the logic of when to use open vs. multi
    text, range = tea.get_single_selection(context)
    if text == None:
        text = ''
    # Indent the snippet
    snippet = tea.indent_snippet(context, first_snippet + final_append, range)
    snippet = tea.construct_snippet(text, snippet)
    return tea.insert_snippet_over_range(context, snippet, range, undo_name)
