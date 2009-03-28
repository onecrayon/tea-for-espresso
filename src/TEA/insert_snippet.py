'''Inserts a snippet at the user's cursor; useful for tab completions'''

import tea_actions as tea

def act(context, default=None, undo_name=None, **syntaxes):
    '''
    Required action method
    
    Inserts an arbitrary text snippet after the cursor with provisions for
    syntax-specific alternatives
    
    Accepts $SELECTED_TEXT placeholder
    
    This method requires at least the snippet default to be defined in the XML
    '''
    if default is None:
        return False
    # Get the cursor position
    text, range = tea.get_single_selection(context, False)
    # Check for root-zone specific override
    root_zone = tea.get_root_zone(context)
    if root_zone in syntaxes:
        snippet = syntaxes[root_zone]
    else:
        snippet = default
    # Check for specific zone override
    zone = tea.get_active_zone(context, range)
    if zone in syntaxes:
        snippet = syntaxes[zone]
    # Construct the snippet
    snippet = tea.construct_snippet(text, snippet)
    # Insert that snippet!
    return tea.insert_snippet_over_range(context, snippet, range, undo_name)
