'''
Converts characters in selection (or character preceding the cursor)
into HTML entities
'''

import tea_actions as tea

def act(context, type='named', undo_name=None):
    '''
    Required action method
    
    Will convert into either named entities (with any high-value, non-named
    entities as numeric entities) or numeric entities
    '''
    ranges = tea.get_ranges(context)
    insertions = tea.new_recipe()
    for range in ranges:
        text = tea.get_selection(context, range)
        if type == 'named':
            # Convert any characters we can into named HTML entities
            text = tea.named_entities(text)
        elif type == 'numeric':
            # Convert any characters we can into numeric HTML entities
            text = tea.numeric_entities(text)
        insertions.addReplacementString_forRange_(text, range)
    if undo_name is not None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
