'''Inserts arbitrary text over all selections'''

import tea_actions as tea

def act(context, default='<br />', prefix_selection=False,
        suffix_selection=False, undo_name='Insert BR', **syntaxes):
    '''
    Required action method
    
    Inserts arbitrary text over all selections; specific text can be
    syntax-specific (same procedure as Wrap Selection In Link)
    
    If you set prefix_selection to true, the inserted text will precede
    any selected text; if suffix_selection is true it will follow any
    selected text; if both are true it will wrap the text
    '''
    pass
