'''
Trims the text; what is trimmed depends on what's passed in via XML
'''

import tea_actions as tea

def act(context, input=None, alternate=None, trim='both', respect_indent=False):
    '''
    Required action method
    
    input dictates what should be trimmed:
    - None (default): falls back to alternate
    - selection: ignores lines if they exist, just trims selection
    - selected_lines: each line in the selection
    
    alternate dictates what to fall back on
    - None (default): will do nothing if input is blank
    - line: will trim the line the caret is on
    - all_lines: all lines in the document
    
    trim dictates what part of the text should be trimmed:
    - both (default)
    - start
    - end
    
    If respect_indent is True, indent characters (as defined in preferences)
    at the beginning of the line will be left untouched.
    '''
    pass
