'''Inserts a snippet at the user's cursor; useful for tab completions'''

import tea_actions as tea

def act(context, default=None, **syntaxes):
    '''
    Required action method
    
    Inserts an arbitrary text snippet after the cursor with provisions for
    syntax-specific alternatives
    
    This method requires at least the snippet default to be defined in the XML
    '''
    if default is None:
        return False
    # Get the cursor position
    range = tea.get_single_range(context)
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
    # Insert that snippet!
    return tea.insert_snippet(context, snippet)
