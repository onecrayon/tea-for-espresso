'''Inserts a snippet at the user's cursor; useful for tab completions'''

import tea_actions as tea

def act(context, default=None, undo_name=None, **syntaxes):
    '''
    Required action method
    
    Inserts an arbitrary text snippet after the cursor with provisions for
    syntax-specific alternatives
    
    Accepts $EDITOR_SELECTION placeholder
    
    This method requires at least the snippet default to be defined in the XML
    '''
    if default is None:
        return False
    # Get the cursor position
    text, range = tea.get_single_selection(context)
    # Check for root-zone specific override
    snippet = tea.select_from_zones(context, range, default, **syntaxes)
    # Construct the snippet
    snippet = tea.construct_snippet(text, snippet)
    # Insert that snippet!
    return tea.insert_snippet(context, snippet)
