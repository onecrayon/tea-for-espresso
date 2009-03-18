'''
Converts characters in selection (or character preceding the cursor)
into HTML entities
'''

import tea_actions as tea

def act(context, type='named', ampersands='named', undo_name=None):
    '''
    Required action method
    
    Will convert into either named entities (with any high-value, non-named
    entities as numeric entities) or numeric entities
    
    The ampersands parameter applies only to numeric entities (sets whether
    to use named or numeric ampersands)
    '''
    ranges = tea.get_ranges(context)
    if len(ranges) is 1 and ranges[0].length is 0:
        # We've got one empty range; make sure it's not at the
        # beginning of the document
        if ranges[0].location > 0:
            # Set the new target range to the character before the cursor
            ranges[0] = tea.new_range(ranges[0].location - 1, 1)
        else:
            return False
    # Since we're here we've got something to work with
    insertions = tea.new_recipe()
    for range in ranges:
        text = tea.get_selection(context, range)
        if type == 'named':
            # Convert any characters we can into named HTML entities
            text = tea.named_entities(text)
        elif type == 'numeric':
            # Convert any characters we can into numeric HTML entities
            text = tea.numeric_entities(text, ampersands)
        insertions.addReplacementString_forRange_(text, range)
    if undo_name is not None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
