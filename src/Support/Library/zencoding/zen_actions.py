#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Middleware layer that communicates between editor and Zen Coding.
This layer describes all available Zen Coding actions, like 
"Expand Abbreviation".
@author Sergey Chikuyonok (serge.che@gmail.com)
@link http://chikuyonok.ru
"""
import zen_core as zen
import re
import html_matcher

def find_abbreviation(editor):
	"""
	Search for abbreviation in editor from current caret position
	@param editor: Editor instance
	@type editor: ZenEditor
	@return: str
	"""
	start, end = editor.get_selection_range()
	if start != end:
		# abbreviation is selected by user
		return editor.get_content()[start, end];
	
	# search for new abbreviation from current caret position
	cur_line_start, cur_line_end = editor.get_current_line_range()
	return zen.extract_abbreviation(editor.get_content()[cur_line_start, start])

def expand_abbreviation(editor, syntax, profile_name='xhtml'):
	"""
	Find from current caret position and expand abbreviation in editor
	@param editor: Editor instance
	@type editor: ZenEditor
	@param syntax: Syntax type (html, css, etc.)
	@type syntax: str
	@param profile_name: Output profile name (html, xml, xhtml)
	@type profile_name: str
	@return: True if abbreviation was expanded successfully
	"""
	range_start, caret_pos = editor.get_selection_range()
	abbr = find_abbreviation(editor)
	content = ''
		
	if abbr:
		content = zen.expand_abbreviation(abbr, syntax, profile_name)
		if content:
			editor.replace_content(content, caret_pos - len(abbr), caret_pos)
			return True
	
	return False

def expand_abbreviation_with_tab(editor, syntax, profile_name='xhtml'):
	"""
	A special version of <code>expandAbbreviation</code> function: if it can't
	find abbreviation, it will place Tab character at caret position
	@param editor: Editor instance
	@type editor: ZenEditor
	@param syntax: Syntax type (html, css, etc.)
	@type syntax: str
	@param profile_name: Output profile name (html, xml, xhtml)
	@type profile_name: str
	"""
	if not expand_abbreviation(editor, syntax, profile_name):
		editor.replace_content('\t', editor.get_caret_pos())

def match_pair(editor, direction='out'):
	"""
	Find and select HTML tag pair
	@param editor: Editor instance
	@type editor: ZenEditor
	@param direction: Direction of pair matching: 'in' or 'out'. 
	@type direction: str 
	"""
	direction = direction.lower()
	
	range_start, range_end = editor.get_selection_range()
	cursor = range_end
	content = editor.get_content()
	range = None
	
	
	old_open_tag = html_matcher.last_match['opening_tag']
	old_close_tag = html_matcher.last_match['closing_tag']
	
	if direction == 'in' and old_open_tag and range_start != range_end:
#		user has previously selected tag and wants to move inward
		if not old_close_tag:
#			unary tag was selected, can't move inward
			return False
		elif old_open_tag['start'] == range_start:
			raise Exception, 'search inward'
			if content[old_open_tag['end']] == '<':
#				test if the first inward tag matches the entire parent tag's content
				_r = html_matcher.find(content, old_open_tag['end'] + 1)
				if _r[0] == old_open_tag['end'] and _r[1] == old_close_tag['start']:
					range = html_matcher.match(content, old_open_tag['end'] + 1)
				else:
					range = (old_open_tag['end'], old_close_tag['start'])
			else:
				range = (old_open_tag['end'], old_close_tag['start'])
		else:
			new_cursor = content[0, old_close_tag['start']].find('<', old_open_tag['end'])
			search_pos = new_cursor + 1 if new_cursor != -1 else old_open_tag['end']
			range = html_matcher.match(content, search_pos)
	else:
		range = html_matcher.match(content, cursor)
	
	
	if range[0] is not None:
		editor.create_selection(range[0], range[1])
		return True
	else:
		return False

def wrap_with_abbreviation(editor, abbr, syntax, profile_name='xhtml'):
	"""
	Wraps content with abbreviation
	@param editor: Editor instance
	@type editor: ZenEditor
	@param syntax: Syntax type (html, css, etc.)
	@type syntax: str
	@param profile_name: Output profile name (html, xml, xhtml)
	@type profile_name: str
	"""
	start_offset, end_offset = editor.get_selection_range()
	content = editor.get_content()
	
	if not abbr: return None 
	
	if start_offset == end_offset:
		# no selection, find tag pair
		range = html_matcher.match(content, start_offset)
		
		if range[0] is None: # nothing to wrap
			return None
			
		start_offset = range[0]
		end_offset = range[1]
			
		# narrow down selection until first non-space character
		while start_offset < end_offset:
			if not content[start_offset].isspace(): break
			start_offset += 1
		
		while end_offset > start_offset:
			end_offset -= 1
			if not content[end_offset].isspace():
				end_offset += 1
				break
	
	new_content = content[start_offset:end_offset]
	result = zen.wrap_with_abbreviation(abbr, unindent(editor, new_content), syntax, profile_name)
	
	if result:
		editor.replace_content(result, start_offset, end_offset)

def unindent(editor, text):
	"""
	Unindent content, thus preparing text for tag wrapping
	@param editor: Editor instance
	@type editor: ZenEditor
	@param text: str
	@return str
	"""
	pad = get_current_line_padding(editor)
	lines = zen.split_by_lines(text)
	
	for i,line in enumerate(lines):
		if line.find(pad) == 0:
			lines[i] = line[len(pad):]
	
	return zen.get_newline().join(lines)

def get_current_line_padding(editor):
	"""
	Returns padding of current editor's line
	@return str
	"""
	line = editor.get_current_line()
	m = re.match(r'^(\s+)', line)
	return m and m.group(0) or ''

def find_new_edit_point(editor, inc=1, offset=0):
	"""
	Search for new caret insertion point
	@param editor: Editor instance
	@type editor: ZenEditor
	@param inc: Search increment: -1 — search left, 1 — search right
	@param offset: Initial offset relative to current caret position
	@return: -1 if insertion point wasn't found
	"""
	cur_point = editor.get_caret_pos() + offset
	content = editor.get_content()
	max_len = len(content)
	next_point = -1
	re_empty_line = r'^\s+$'
	
	def get_line(ix):
		start = ix
		while start >= 0:
			c = content[start]
			if c == '\n' or c == '\r': break
			start -= 1
		
		return content[start:ix]
		
	while cur_point < max_len and cur_point > 0:
		cur_point += inc
		cur_char = content[cur_point]
		next_char = content[cur_point + 1]
		prev_char = content[cur_point - 1]
		
		if cur_char in '"\'':
			if next_char == cur_char and prev_char == '=':
				# empty attribute
				next_point = cur_point + 1
		elif cur_char == '>' and next_char == '<':
			# between tags
			next_point = cur_point + 1
		elif cur_char in '\r\n':
			# empty line
			if re.search(re_empty_line, get_line(cur_point - 1)):
				next_point = cur_point
		
		if next_point != -1: break
	
	return next_point

def prev_edit_point(editor):
	"""
	Move caret to previous edit point
	@param editor: Editor instance
	@type editor: ZenEditor
	"""
	cur_pos = editor.get_caret_pos()
	new_point = find_new_edit_point(editor, -1)
		
	if new_point == cur_pos:
		# we're still in the same point, try searching from the other place
		new_point = find_new_edit_point(editor, -1, -2)
	
	if new_point != -1:
		editor.set_caret_pos(new_point)

def next_edit_point(editor):
	"""
	Move caret to next edit point
	@param editor: Editor instance
	@type editor: ZenEditor
	""" 
	new_point = find_new_edit_point(editor, 1)
	if new_point != -1:
		editor.set_caret_pos(new_point)

def insert_formatted_newline(editor, mode='html'):
	"""
	Inserts newline character with proper indentation
	@param editor: Editor instance
	@type editor: ZenEditor
	@param mode: Syntax mode (only 'html' is implemented)
	@type mode: str
	"""
	caret_pos = editor.get_caret_pos()
		
	def insert_nl():
		editor.replace_content('\n', caret_pos)
		
	if mode == 'html':
		# let's see if we're breaking newly created tag
		pair = html_matcher.get_tags(editor.get_content(), editor.get_caret_pos())
		
		if pair[0] and pair[1] and pair[0]['type'] == 'tag' and pair[0]['end'] == caret_pos and pair[1]['start'] == caret_pos:
			editor.replace_content('\n\t|\n', caret_pos)
		else:
			insert_nl()
	else:
		insert_nl()

def select_line(editor):
	"""
	Select line under cursor
	@param editor: Editor instance
	@type editor: ZenEditor
	"""
	start, end = editor.get_current_line_range();
	editor.create_selection(start, end)

def go_to_matching_pair(editor):
	"""
	Moves caret to matching opening or closing tag
	@param editor: Editor instance
	@type editor: ZenEditor
	"""
	content = editor.get_content()
	caret_pos = editor.get_caret_pos()
	
	if content[caret_pos] == '<': 
		# looks like caret is outside of tag pair  
		caret_pos += 1
		
	range = html_matcher.match(content, caret_pos)
		
	if range[0] is not None:
		# match found
		open_tag = html_matcher.last_match['opening_tag']
		close_tag = html_matcher.last_match['closing_tag']
			
		if close_tag: # exclude unary tags
			if open_tag['start'] <= caret_pos and open_tag['end'] >= caret_pos:
				editor.set_caret_pos(close_tag['start'])
			elif close_tag['start'] <= caret_pos and close_tag['end'] >= caret_pos:
				editor.set_caret_pos(open_tag['start'])
				

def merge_lines(editor):
	"""
	Merge lines spanned by user selection. If there's no selection, tries to find
	matching tags and use them as selection
	@param editor: Editor instance
	@type editor: ZenEditor
	"""
	start, end = editor.get_selection_range()
	if start == end:
		# find matching tag
		pair = html_matcher.match(editor.get_content(), editor.get_caret_pos())
		if pair and pair[0] is not None:
			start, end = pair
	
	if start != end:
		# got range, merge lines
		text = editor.get_content()[start, end]
		lines = map(lambda s: re.sub(r'^\s+', '', s), zen.split_by_lines(text))
		text = re.sub(r'\s{2,}', ' ', ''.join(lines))
		editor.replace_content(text, start, end)
		editor.create_selection(start, start + len(text))
