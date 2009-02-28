'''Inserts arbitrary text over all selections'''

import tea_actions as tea

def act(context, default='<br />', prefix_selection=False,
        suffix_selection=False, undo_name=None, **syntaxes):
    '''
    Required action method
    
    Inserts arbitrary text over all selections; specific text can be
    syntax-specific (same procedure as Wrap Selection In Link)
    
    If you set prefix_selection to true, the inserted text will precede
    any selected text; if suffix_selection is true it will follow any
    selected text; if both are true it will wrap the text
    '''
    # Fetch the root zone's insert text
    # Selection-specific zones are checked later
    root_zone = tea.get_root_zone(context)
    if root_zone in syntaxes:
        insert = syntaxes[root_zone]
    else:
        insert = default
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
        zone = tea.get_active_zone(context, range)
        if zone in syntaxes:
            insert = syntaxes[zone]
        text = text.replace('$INSERT', insert)
        # Insert the text, or replace the selected text
        if range.length is 0:
            insertions.addInsertedString_forIndex_(text, range.location)
        else:
            insertions.addReplacementString_forRange_(text, range)
    # Set undo name and run the recipe
    if undo_name != None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
