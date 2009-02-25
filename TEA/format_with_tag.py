'''
Formats the selected text by wrapping it in the passed tag

When called without the second argument, the text will be wrapped in
paragraph tags
'''

import tea_actions as tea

def act(context, tag='p', tagname=None):
    '''
    Required action method
    
    Note the use of extra keyword arguments; if you wish to use extra
    arguments they must be defined as keyword arguments with a 
    sensible default.  See TextActions/Actions.xml for an example of
    how to construct those arguments in XML definition.
    '''
    # Set the legible tag name
    if tagname == None:
        tagname = tag.capitalize()
    ranges = context.selectedRanges()
    if len(ranges) <= 1:
        # If we're working with a single selection, we can use a snippet
        text, range = tea.get_single_selection(context)
        if text == None:
            return False
        snippet = '#{1:<' + tag + '>#{2:' + text + '}</' + tag + '>}#0'
        # Insert the text via recipe
        return tea.insert_snippet_over_selection(context, snippet, range,
                                                 'Format with ' + tagname)
    # We're handling multiple, discontiguous ranges; wrap all of them
    # with the tag
    insertions = tea.new_recipe()
    for range in ranges:
        # Convert NSConcreteValue to NSRange
        range = range.rangeValue()
        text = tea.get_selection(context, range)
        text = '<' + tag + '>' + text + '</' + tag + '>'
        insertions.addReplacementString_forRange_(text, range)
    insertions.setUndoActionName_('Format with ' + tagname)
    return context.applyTextRecipe_(insertions)
