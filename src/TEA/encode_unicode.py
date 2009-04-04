'''
Converts unicode characters in selection (or character preceding the cursor)
into various types of ASCII strings
'''

import tea_actions as tea

def act(context, type='named', wrap='$HEX', undo_name=None):
    '''
    Required action method
    
    Type can be:
    named: named HTML entities, with high value numeric entities if no name
    numeric: numeric HTML entities
    hex: hexadecimal encoding; use the 'wrap' option for specific output
    
    Wrap will be used if type is 'hex' and will replace $HEX with the actual
    hex value.  For example '\u$HEX' will be result in something like '\u0022'
    '''
    ranges = tea.get_ranges(context)
    if len(ranges) == 1 and ranges[0].length == 0:
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
            text = tea.numeric_entities(text, type)
        elif type == 'hex':
            # Convert characters to hex via numeric entities
            text = tea.numeric_entities(text)
            text = tea.entities_to_hex(text, wrap)
        insertions.addReplacementString_forRange_(text, range)
    if undo_name is not None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
