'''Wraps selected text in a link (what kind of link based on context)'''

import subprocess

import tea_actions as tea

def create_link(zone, url, text, snippet=False):
    '''
    Creates a textual link (or snippet) based on the active syntax zone
    (defaults to HTML)
    '''
    if snippet:
        return tea.construct_snippet(
            text,
            '<a href="${1:' + url + '}"#{2: title="#3"}>$SELECTED_TEXT</a>$0'
        )
    # Not a snippet, so return the text
    return '<a href="' + url + '">' + text + '</a>'


def act(context, undo_name='Wrap Selection In Link'):
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
    
    ranges = tea.get_ranges(context)
    if len(ranges) == 1:
        # If we're working with a single selection, we can use a snippet
        range = ranges[0]
        # Make sure the range is actually a selection
        if range.length == 0:
            tea.say(
                context, "Error: selection required",
                "You must select some text in order to use this action."
            )
            return False
        text = tea.get_selection(context, range)
        # Get the syntax zone
        zone = ''
        snippet = create_link(zone, url, text, snippet=True)
        # Insert the text via recipe
        return tea.insert_snippet_over_selection(context, snippet, range,
                                                 undo_name)
    # We're handling multiple, discontiguous ranges; wrap all of them
    # with the tag
    insertions = tea.new_recipe()
    for range in ranges:
        text = tea.get_selection(context, range)
        # Get the syntax zone
        zone = ''
        text = create_link(zone, url, text)
        insertions.addReplacementString_forRange_(text, range)
    insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
