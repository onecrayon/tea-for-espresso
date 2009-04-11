'''
Visits a URL, filling a placeholder with selected text (or similar)
'''

import tea_actions as tea

def act(context, input=None, default=None, **syntaxes):
    '''
    Required action method
    
    input dictates what fills the placeholder if there is no selection:
    - word
    - line
    
    default and syntaxes will replace $SELECTED_TEXT with a URL escaped version
    of the selected text (or input, if no selected text)
    '''
    pass
