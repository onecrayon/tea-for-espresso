import tea_actions as tea

from zencoding import zen_core as zen

def act(context):
    range = tea.get_single_range(context)
    start, end = zen.get_pair_range(context.string(), range.location)
    
    if start != -1:
        new_range = tea.new_range(start, end - start)
        tea.set_selected_range(context, new_range)
        return True
    else:
        return False
