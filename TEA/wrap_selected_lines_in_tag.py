'''
Wraps currently selected lines in a text snippet
'''

import re

import tea_actions as tea

def act(context):
    '''
    Required action method
    
    Much like Wrap Selection in Tag, this only allows a single selection
    (enforced through the utility functions) then parses over the
    lines and inserts a snippet to allow the user to define the tag
    '''
    text, range = tea.get_single_selection(context)
    if text == None:
        return False
    # Split the text into lines, maintaining the linebreaks
    lines = text.splitlines(True)
    # Compile the regex for quicker action on lots of lines
    parser = re.compile(r'(\s*)(.*?)(\s*(\r?\n)|$)')
    # Loop over lines and construct the snippet
    snippet = ''
    # This is the number of snippets processed, not lines
    count = 1
    for line in lines:
        content = parser.search(line)
        # Only wrap the line if there's some content
        if content.group(2) != '':
            segment = tea.construct_tag_snippet(content.group(2), count, 'li')
            snippet += content.group(1) + segment + content.group(3)
            count += 1
        else:
            snippet += line
    return tea.insert_snippet_over_selection(context, snippet, range,
                                             'Wrap Selected Lines in Tag')
