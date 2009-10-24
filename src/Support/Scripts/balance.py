#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tea_actions as tea

from zencoding import html_matcher as html_matcher

def act(context, direction='out'):
	rng = tea.get_single_range(context)
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