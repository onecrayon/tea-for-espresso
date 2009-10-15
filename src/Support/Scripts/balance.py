import tea_actions as tea

from zencoding import html_matcher as html_matcher

def act(context, direction='out'):
    range = tea.get_single_range(context)
    cursor = range.location + range.length
    start, end = html_matcher.match(context.string(), cursor)
    
    if start is not None:
        # BALANCING INWARD IS CURRENTLY BROKEN
        if direction.lower() == 'in':
            open = html_matcher.last_match['opening_tag']
            close = html_matcher.last_match['closing_tag']
            if open is not None and close is not None:
                text = tea.get_selection(
                    context,
                    tea.new_range(open.end, close.start - open.end)
                )
                cursor = text.find('<')
                if cursor != -1:
                    cursor += open.end + 1
                    start_1, end_1 = html_matcher.match(context.string(), cursor)
                    if start_1 is not None:
                        start = start_1
                        end = end_1
        
        new_range = tea.new_range(start, end - start)
        tea.set_selected_range(context, new_range)
        return True
    else:
        return False
