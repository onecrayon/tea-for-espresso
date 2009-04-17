'''
Visits a URL, filling a placeholder with selected text (or similar)
'''

import urllib

from Foundation import NSWorkspace, NSURL

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
    text, range = tea.get_single_selection(context)
    if text is None:
        range = tea.get_single_range(context)
        if input == 'word':
            text, range = tea.get_word(context, range)
        elif input == 'line':
            text, range = tea.get_line(context, range)
    # If we still don't have text, there's nothing to work with
    if text is None:
        return False
    # URL escape the selected text
    text = urllib.quote_plus(text)
    root_zone = tea.get_root_zone(context)
    if root_zone in syntaxes:
        root_url = syntaxes[root_zone]
    else:
        root_url = default
    zone = tea.get_active_zone(context, range)
    if zone in syntaxes:
        url = syntaxes[zone]
    else:
        url = root_url
    # Got the URL, let's run the URL
    url = url.replace('$SELECTED_TEXT', text)
    NSWorkspace.sharedWorkspace().openURL_(NSURL.URLWithString_(url))
    # Because this gets passed through to Obj-C, using int prevents beeping
    return True
