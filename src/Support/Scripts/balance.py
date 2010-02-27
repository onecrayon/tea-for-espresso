'''
Attempts to locate the balanced delimiters around the cursor and select
their contents.

If direction == 'in', balance will attempt to move inward (select first
balanced delimiters contained within the current delimiter) rather than
outward.

mode controls what type of balancing is used:
- auto (default): tries to detect if we're in HTML before using zen
- zen: always uses zen coding, even if we aren't in HTML or XML
- itemizer: always uses itemizer balancing, even in HTML
'''

from Foundation import NSValue

import tea_actions as tea

from zencoding import zen_core as zen_coding
from zen_editor import ZenEditor

def act(context, direction='out', mode='auto'):
    zen_target = 'html, html *, xml, xml *'
    if (mode.lower() == 'auto' and tea.cursor_in_zone(context, zen_target)) or \
       mode.lower() == 'zen':
        # HTML or XML, so use Zen-coding's excellent balancing commands
        
        editor = ZenEditor(context)
        action_name = 'match_pair_inward' if direction == 'in' else 'match_pair_outward'
        return zen_coding.run_action(action_name, editor)
    else:
        # No HTML or XML, so we'll rely on itemizers
        ranges = tea.get_ranges(context)
        targets = []
        for range in ranges:
            if direction.lower() == 'in':
                item = tea.get_item_for_range(context, range)
                if item is None:
                    # No item, so jump to next iteration
                    continue
                new_range = item.range()
                if new_range.location == range.location and \
                   new_range.length == range.length:
                    items = item.childItems()
                    if len(items) > 0:
                        new_range = items[0].range()
                targets.append(new_range)
            else:
                item = tea.get_item_parent_for_range(context, range)
                if item is None:
                    continue
                targets.append(item.range())
        
        # Set the selections, and return
        if len(targets) > 0:
            context.setSelectedRanges_([NSValue.valueWithRange_(range) for range in targets])
            return True
        else:
            return False
