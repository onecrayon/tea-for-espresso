'''Converts word or selection into an open/close tag pair'''

import tea_actions as tea

def act(context):
    '''
    Required action method
    
    Transforms the word under the cursor (or the word immediately previous
    to the cursor) into an open/close tag pair with the cursor in the middle
    
    If some text is selected, then it is turned into an open/close tag with
    attributes intelligently stripped from the closing tag.
    
    Based heavily on Textmate's Insert Open/Close Tag (With Current Word)
    '''
    pass
