'''Wraps currently selected lines in a text snippet'''

import re

import tea_actions as tea

def act(context, first_snippet='', following_snippet='',
        final_append='', undo_name=None):
    '''
    Required action method
    
    This only allows a single selection (enforced through the utility
    functions) then parses over the lines and inserts a snippet
    
    Theoretically we could allow discontiguous selections; have to consider
    it if recipes get snippet capabilities
    '''
    text, range = tea.get_single_selection(context, True)
    if text == None:
        return False
    # Split the text into lines, maintaining the linebreaks
    lines = text.splitlines(True)
    # Compile the regex for quicker action on lots of lines
    parser = re.compile(r'(\s*)(.*?)(\s*(\r|\r\n|\n)|$)')
    # Loop over lines and construct the snippet
    snippet = ''
    # This is the number of snippets processed, not lines
    count = 1
    for line in lines:
        content = parser.search(line)
        # Only wrap the line if there's some content
        if content.group(2) != '':
            if count == 1:
                segment = tea.construct_snippet(content.group(2), first)
            else:
                segment = tea.construct_snippet(content.group(2), following)
            snippet += content.group(1) + segment + content.group(3)
            count += 1
        else:
            snippet += line
    snippet += final_append
    return tea.insert_snippet_over_range(context, snippet, range, undo_name)
