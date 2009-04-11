'''
Trims the text; what is trimmed depends on what's passed in via XML
'''

import tea_actions as tea

def act(context, input=None, alternate=None, trim='both', respect_indent=False,
        undo_name=None):
    '''
    Required action method
    
    input dictates what should be trimmed:
    - None (default): falls back to alternate
    - selection: ignores lines if they exist, just trims selection
    - selected_lines: each line in the selection
    
    alternate dictates what to fall back on
    - None (default): will do nothing if input is blank
    - line: will trim the line the caret is on
    - all_lines: all lines in the document
    
    trim dictates what part of the text should be trimmed:
    - both (default)
    - start
    - end
    
    If respect_indent is True, indent characters (as defined in preferences)
    at the beginning of the line will be left untouched.
    '''
    # Since input is always a selection of some kind, check if we have one
    ranges = tea.get_ranges(context)
    insertions = tea.new_recipe()
    if (len(ranges) == 1 and ranges[0].length = 0) or input is None:
        if alternate == 'line':
            text, range = tea.get_line(context, ranges[0])
            text = tea.trim(context, text, False, trim, respect_indent)
        elif alternate == 'all_lines':
            range = tea.new_range(0, context.string().length())
            text = tea.get_selection(context, range)
            text = tea.trim(context, text, True, trim, respect_indent)
        insertions.addReplacementString_forRange_(text, range)
    else:
        if input == 'selected_lines':
            parse_lines = True
        else:
            parse_lines = False
        for range in ranges:
            text = tea.get_selection(context, range)
            text = tea.trim(context, text, parse_lines, trim, respect_indent)
            insertions.addReplacementString_forRange_(text, range)
    if undo_name != None:
        insertions.setUndoActionName_(undo_name)
    return context.applyTextRecipe_(insertions)
