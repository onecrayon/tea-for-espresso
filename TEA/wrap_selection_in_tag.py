'''
Wraps the currently selected text in a tag snippet
'''

import tea_utils as tea

def act(context):
    '''Required action method'''
    deletions = tea.new_recipe()
    ranges = context.selectedRanges()
    # Since there aren't good ways to deal with discontiguous selections
    # verify that we're only working with a single selection
    if len(ranges) != 1:
        tea.say(
            context, "Error: multiple selections detected",
            "You must have a single selection in order to use Wrap Selection in Tag."
        )
        return False
    count = 1
    for range in ranges:
        # For some reason, range is not an NSRange; it's an NSConcreteValue
        # This converts it to an NSRange which we can work with
        range = range.rangeValue()
        if range.length is 0:
            tea.say(
                context, "Error: selection required",
                "You must select some text in order to use Wrap Selection in Tag."
            )
            return False
        text = tea.get_selection(context, range)
        snippet = tea.construct_tag_snippet(text, count)
        deletions.addDeletedRange_(range)
        # We break because we can only currently handle the first
        break
        count = count + 1
    # Apply the deletions
    context.applyTextRecipe_(deletions)
    # Insert the snippet
    return tea.insert_snippet(context, snippet)
