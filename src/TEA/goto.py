'''
Attempts to go to (select) a location in the document
'''

import tea_actions as tea

def act(context, target=None, source=None, trim=False, discard_indent=False,
        prompt=None, search_string=None, regex=False):
    '''
    Required action method
    
    target dictates what we're looking for:
    - text
    - zone (syntax zone selector string)
    - if unspecified, simply selects the source
    
    source dictates how to gather the string to search for:
    - user (user will be prompted to enter a string)
    - selection
    - word (word under the caret)
    - line (line under the caret)
    
    Setting trim=True will cause the source to be trimmed
    
    Setting discard_indent=True will cause even indentation characters
    to be trimmed (unnecessary unless trim=True)
    
    prompt will set the text of the dialog box if source='user'
    
    search_string will set the string to search for if target is text or zone
    - $SELECTED_TEXT will be replaced with the source text
    
    Setting regex=True will cause search_string to be evaluated as regex
    '''
    pass
