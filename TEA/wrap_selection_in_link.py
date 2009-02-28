'''Wraps selected text in a link (what kind of link based on context)'''

import subprocess

import tea_actions as tea

def act(context, undo_name='Wrap Selection In Link',
        default='<a href="${1:$URL}"#{2: title="#3"}>$SELECTED_TEXT</a>$0',
        **syntaxes):
    '''
    Required action method
    
    A flexible link generator which uses the clipboard text (if there's
    a recognizable link there) and formats the snippet based on the
    active syntax of the context
    '''
    # Get the clipboard contents
    process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    clipboard, error = process.communicate(None)
    # Construct the default link
    url = clipboard
    
    text, range = tea.get_single_selection(context)
    if text == None:
        return False
    # Get the syntax zone
    zone = ''
    # Get the snippet based on the zone
    snippet = default
    snippet = tea.construct_snippet(text, snippet)
    snippet.replace('$URL', url)
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             undo_name)
