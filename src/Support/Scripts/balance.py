'''
Attempts to locate the balanced delimiters around the cursor and select
their contents.

If direction == 'in', balance will attempt to move inward (select first
balanced delimiters contained within the current delimiter) rather than
outward.
'''

import tea_actions as tea

from zencoding import html_matcher as html_matcher

def act(context, direction='out'):
    if tea.cursor_in_zone(context, "html, html *, xml, xml *"):
        # HTML or XML, so use Zen-coding's excellent balancing commands
        
        # Using this method rather than tea.get_single_range() is better
        # because it won't cause the action to fail if there's more than
        # one selection
        ranges = tea.get_ranges(context)
        rng = ranges[0]
        cursor = rng.location + rng.length
        range_start, range_end = rng.location, rng.location + rng.length
        content = context.string()
        
        old_open_tag = html_matcher.last_match['opening_tag']
        old_close_tag = html_matcher.last_match['closing_tag']
        
        if direction.lower() == 'in' and old_open_tag and range_start != range_end:
            # user has previously selected tag and wants to move inward
            if not old_close_tag:
                # unary tag was selected, can't move inward
                return False
            elif old_open_tag.start == range_start:
                if content[old_open_tag.end] == '<':
                    # test if the first inward tag matches the entire parent tag's content
                    _start, _end = html_matcher.find(content, old_open_tag.end + 1)
                    if _start == old_open_tag.end and _end == old_close_tag.start:
                        start, end = html_matcher.match(content, old_open_tag.end + 1)
                    else:
                        start, end = old_open_tag.end, old_close_tag.start
                else:
                    start, end = old_open_tag.end, old_close_tag.start
            else:
                new_cursor = content.find('<', old_open_tag.end, old_close_tag.start)
                search_pos = new_cursor != -1 and new_cursor + 1 or old_open_tag.end
                start, end = html_matcher.match(content, search_pos)
                
        else:
            start, end = html_matcher.match(content, cursor)
        
        if start is not None:
            new_range = tea.new_range(start, end - start)
            tea.set_selected_range(context, new_range)
            return True
        else:
            return False
    else:
        # No HTML or XML, so we'll rely on itemizers
        ranges = tea.get_ranges(context)
        targets = []
        for range in ranges:
            if direction.lower() == 'in':
                targets[] = tea.get_item_for_range(context, range).range()
            else:
                targets[] = tea.get_item_parent_for_range(context, range).range()
        
        # Set the selections, and return
        context.setSelectedRanges_([NSValue.valueWithRange_(range) for range in targets])
        return True
