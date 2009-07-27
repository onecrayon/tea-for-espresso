'''Inserts arbitrary text over all selections'''

import tea_actions as tea

def act(context, default=None, prefix_selection=False,
        suffix_selection=False, undo_name=None, **syntaxes):
    '''
    Required action method
    
    Inserts arbitrary text over all selections; specific text can be
    syntax-specific (same procedure as Wrap Selection In Link)
    
    If you set prefix_selection to true, the inserted text will precede
    any selected text; if suffix_selection is true it will follow any
    selected text; if both are true it will wrap the text
    '''
    # Grab the ranges
    ranges = tea.get_ranges(context)
    # Set up our text recipe
    insertions = tea.new_recipe()
    for range in ranges:
        if prefix_selection or suffix_selection:
            # Get the selected text
            text = tea.get_selection(context, range)
            if prefix_selection:
                text = '$INSERT' + text
            if suffix_selection:
                text += '$INSERT'
            # If empty selection, only insert one
            if text == '$INSERT$INSERT':
                text = '$INSERT'
        else:
            text = '$INSERT'
        # Check for zone-specific insertion
        insert = tea.select_from_zones(context, range, default, **syntaxes)
        text = text.replace('$INSERT', insert)
        text = text.replace('$TOUCH', '')
        # Insert the text, or replace the selected text
        if range.length is 0:
            insertions.addInsertedString_forIndex_(text, range.location)
        else:
            insertions.addReplacementString_forRange_(text, range)
    # Set undo name and run the recipe
    if undo_name != None:
        insertions.setUndoActionName_(undo_name)
    reset_cursor = False
    if len(ranges) is 1 and ranges[0].length is 0:
        # Thanks to addInsertedString's wonkiness, we have to reset the cursor
        reset_cursor = True
    # Espresso beeps if I return True or False; hence this weirdness
    return_val = context.applyTextRecipe_(insertions)
    if reset_cursor:
        new_range = tea.new_range(ranges[0].location + len(text), 0)
        tea.set_selected_range(context, new_range)
    return return_val
