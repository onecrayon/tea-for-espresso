import tea_actions as tea

from zencoding import html_matcher as html_matcher

def act(context):
    range = tea.get_single_range(context)
    cursor = range.location + range.length
    start, end = html_matcher.match(context.string(), cursor)
    
    if start is not None:
        new_range = tea.new_range(start, end - start)
        tea.set_selected_range(context, new_range)
        return True
    else:
        return False
