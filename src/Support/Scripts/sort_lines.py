'''Sorts selected lines ascending or descending'''

import random

import tea_actions as tea

def act(context, direction=None, remove_duplicates=False, undo_name=None):
    '''
    Required action method
    
    This sorts the selected lines (or document, if no selection)
    either ascending, descending, or randomly.
    '''
    # Check if there is a selection, otherwise take all lines
    ranges = tea.get_ranges(context)
    if len(ranges) == 1 and ranges[0].length == 0:
        ranges = [tea.new_range(0, context.string().length())]
    
    # Setup the text recipe
    recipe = tea.new_recipe()
    
    for range in ranges:
        text = tea.get_selection(context, range)
        
        # A blank range means we have only one range and it's empty
        # so we can't do any sorting
        if text == '':
            return False

        # Split the text into lines, not maintaining the linebreaks
        lines = text.splitlines(False)
        
        # Remove duplicates if set
        if remove_duplicates:
            if direction is None:
                seen = {}
                result = []
                for x in lines:
                    if x in seen: continue
                    seen[x] = 1
                    result.append(x)
                lines = result
            else:
                lines = list(set(lines))
        
        # Sort lines ascending or descending
        if direction == 'asc' or direction == 'desc':
            lines.sort()
            if direction == 'desc':
                lines.reverse()
        
        # If direction is random, shuffle lines
        if direction == 'random':
            random.shuffle(lines)
    
        # Join lines to one string
        linebreak = tea.get_line_ending(context)
        sortedText = unicode.join(linebreak, lines)
        
        # Add final linebreak if selected text has one
        if text.endswith(linebreak):
            sortedText += linebreak
        
        # Insert the text
        recipe.addReplacementString_forRange_(sortedText, range)
    
    if undo_name is not None:
        recipe.setUndoActionName_(undo_name)
    # Apply the recipe
    return context.applyTextRecipe_(recipe)
