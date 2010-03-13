'''
Formats the selected text by wrapping it in the passed segment

Will use an automatically formatted snippet for a single selection,
or a simple text replacement for multiple selections
'''

import tea_actions as tea

def act(context, default=None, undo_name=None, **syntaxes):
    '''
    Required action method
    
    default parameter is not a snippet, but should contain the
    $EDITOR_SELECTION placeholder
    '''
    # Get the selected ranges
    ranges = tea.get_ranges(context)
    if len(ranges) is 1:
        # Since we've only got one selection we can use a snippet
        range = ranges[0]
        insertion = tea.select_from_zones(context, range, default, **syntaxes)
        # Make sure the range is actually a selection
        if range.length > 0:
            text = tea.get_selection(context, range)
            snippet = '${1:' + insertion.replace('$EDITOR_SELECTION',
                                                 '${2:$EDITOR_SELECTION}') + '}$0'
        else:
            # Not a selection, just wrap the cursor
            text = ''
            snippet = insertion.replace('$EDITOR_SELECTION', '$1') + '$0'
        snippet = tea.construct_snippet(text, snippet)
        return tea.insert_snippet(context, snippet)
    # Since we're here, it must not have been a single selection
    insertions = tea.new_recipe()
    for range in ranges:
        insertion = tea.select_from_zones(context, range, default, **syntaxes)
        text = tea.get_selection(context, range)
        # DEPRECATED: $SELECTED_TEXT will go away in future; don't use it
        insertion = insertion.replace('$SELECTED_TEXT', text)
        insertion = insertion.replace('$EDITOR_SELECTION', text)
        insertions.addReplacementString_forRange_(insertion, range)
    if undo_name is not None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
