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
    text, range = tea.get_single_selection(context)
    # Check for root-zone specific override
    snippet = tea.select_from_zones(context, range, default, **syntaxes)
    # Indent the snippet
    snippet = tea.indent_snippet(context, snippet, range)
    # Construct the snippet
    snippet = tea.construct_snippet(text, snippet)
    # Insert that snippet!
    return tea.insert_snippet_over_range(context, snippet, range, undo_name)
