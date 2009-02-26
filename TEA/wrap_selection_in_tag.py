'''
Wraps the currently selected text in a tag snippet
'''

import tea_actions as tea

def act(context, tag='p'):
    '''
    Required action method
    
    This action is simple enough that it merely implements several
    utility functions
    '''
    text, range = tea.get_single_selection(context)
    if text == None:
        return False
    snippet = tea.construct_tag_snippet(text, default_tag=tag)
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             'Wrap Selection in Tag')
