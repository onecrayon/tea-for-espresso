'''
@author: Sergey Chikuyonok (serge.che@gmail.com)
'''
'''Class for wrapping text with ZenCoding's abbreviations'''

import re

from zencoding import settings_loader

import tea_actions as tea

from zencoding import zen_core as zen
from zencoding import html_matcher

# This is a special variable; if it exists in a module, the module will be
# passed the actionObject as the second parameter
req_action_object = True

def act(context, actionObject, profile_name='xhtml', undo_name=None):
    abbr = actionObject.userInput().stringValue()
    # Set up the config variables
    zen_settings = settings_loader.load_settings()
    zen.update_settings(zen_settings)
    zen.newline = safe_str(tea.get_line_ending(context))
    zen_settings['variables']['indentation'] = safe_str(tea.get_indentation_string(context))
    
    # This allows us to use smart incrementing tab stops in zen snippets
    point_ix = [0]
    def place_ins_point(text):
        point_ix[0] += 1
        return '$%s' % point_ix[0]
    zen.insertion_point = place_ins_point
    
    rng = tea.get_first_range(context)
    
    # Until Serge figures out what is wrong with html_matcher, only fire for HTML
    zen_target = 'html, html *, xml, xml *'
    if rng.length == 0 and tea.cursor_in_zone(context, zen_target):
        # no selection, find matching tag
        content = context.string()
        start, end = html_matcher.match(content, rng.location)
        if start is None:
            # nothing to wrap
            return False
        
        def is_space(char):
            return char.isspace() or char in r'\n\r'
        
        # narrow down selection until first non-space character
        while start < end:
            if not is_space(content[start]):
                break
            start += 1
        
        while end > start:
            end -= 1
            if not is_space(content[end]):
                end += 1
                break
        
        rng = tea.new_range(start, end - start)
    elif rng.length == 0:
        text, rng = tea.get_word(context, rng)
    
    text = tea.get_selection(context, rng)
    
    # Detect the type of document we're working with
    zones = {
        'css, css *': 'css',
        'xsl, xsl *': 'xsl',
        'xml, xml *': 'xml'
    }
    doc_type = tea.select_from_zones(context, rng, 'html', **zones)
    
    text = unindent(context, text)
    
    # Damn Python's encodings! Have to convert string to ascii before wrapping 
    # and then back to utf-8
    result = zen.wrap_with_abbreviation(safe_str(abbr), safe_str(text), doc_type, profile_name)
    # Exit with error if no results
    if result is None:
        tea.log('Zen Wrap With Abbreviation failed: check abbreviation syntax.')
        return False
    
    result = unicode(result, 'utf-8')
    
    tea.insert_snippet_over_range(context, result, rng, undo_name)
    
    return True

def get_current_line_padding(context):
    """
    Returns padding of current editor's line
    @return str
    """
    line, r = tea.get_line(context, tea.get_ranges(context)[0])
    m = re.match(r'^(\s+)', safe_str(line))
    return m and m.group(0) or ''

def unindent(context, text):
    """
    Unindent content, thus preparing text for tag wrapping
    @param text: str
    @return str
    """
    pad = get_current_line_padding(context)
    lines = zen.split_by_lines(text)
    
    for i,line in enumerate(lines):
        if line.find(pad) == 0:
            lines[i] = line[len(pad):]
    
    return zen.get_newline().join(lines)

def safe_str(text):
    """
    Creates safe string representation to deal with Python's encoding issues
    """
    return text.encode('utf-8')
