'''Converts spaces in the document to tabs and vice-versa'''

import re

import tea_actions as tea

# This is a special variable; if it exists in a module, the module will be
# passed the actionObject as the second parameter
req_action_object = True

def act(context, actionObject, operation='entab'):
    # Leave sheet open with "processing" spinner
    actionObject.spinner.startAnimation_(actionObject)
    
    spaces = int(actionObject.numSpaces.stringValue())
    if operation == 'entab':
        target = re.compile(r'^(\t* +\t*)+', re.MULTILINE)
        search = ' ' * spaces
        replace = '\t'
    else:
        target = re.compile(r'^( *\t+ *)+', re.MULTILINE)
        search = '\t'
        replace = ' ' * spaces
    insertions = tea.new_recipe()
    ranges = tea.get_ranges(context)
    if len(ranges) == 1 and ranges[0].length == 0:
        # No selection, use the document
        ranges[0] = tea.new_range(0, context.string().length())
    for range in ranges:
        text = tea.get_selection(context, range)
        # Non-Unix line endings will bork things; convert them
        text = tea.unix_line_endings(text)
        text = re.sub(target, replacements, text)
        if tea.get_line_ending(context) != '\n':
            text = tea.clean_line_endings(context, text)
        insertions.addReplacementString_forRange_(text, range)
    insertions.setUndoActionName_(operation.title())
    context.applyTextRecipe_(insertions)
    actionObject.spinner.stopAnimation_(actionObject)
    
    return True
