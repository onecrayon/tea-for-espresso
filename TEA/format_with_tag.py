'''
Formats the selected text by wrapping it in the passed tag

Will use a snippet for a single selection, or a simple text replacement
for multiple selections

Specific to HTML/XML
'''

import tea_actions as tea

def act(context, tag='p', undo_name=None):
    '''
    Required action method
    
    Note the use of extra keyword arguments; if you wish to use extra
    arguments they must be defined as keyword arguments with a 
    sensible default.  See TextActions/Actions.xml for an example of
    how to construct those arguments in XML definition.
    '''
    # Set the legible tag name
    if undo_name == None:
        # Remember, setting a keyword argument changes its default for every
        # call of the function
        undo_final = 'Format With ' + tag.capitalize()
    else:
        undo_final = undo_name
    # In case the tag has attributes, parse it
    opentag, closetag = tea.parse_tag(tag)
    if opentag == None:
        # Total regex failure, abort, abort!
        return False
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
        snippet = '${1:<' + opentag + '>${2:$SELECTED_TEXT}</' + \
                  closetag + '>}$0'
        snippet = tea.construct_snippet(text, snippet)
        # Insert the text via recipe
        return tea.insert_snippet_over_selection(context, snippet, range,
                                                 undo_final)
    # We're handling multiple, discontiguous ranges; wrap all of them
    # with the tag
    insertions = tea.new_recipe()
    for range in ranges:
        text = tea.get_selection(context, range)
        text = '<' + opentag + '>' + text + '</' + closetag + '>'
        insertions.addReplacementString_forRange_(text, range)
    insertions.setUndoActionName_('Format with ' + tagname)
    return context.applyTextRecipe_(insertions)
