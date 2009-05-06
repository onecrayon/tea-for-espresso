'''Sorts selected lines ascending or descending'''

import random

import tea_actions as tea

def act(context, direction=None, remove_duplicates=False, undo_name=None):
	'''
	Required action method
	
	This only allows a single selection (enforced through the utility
	functions) then sorts the lines, either ascending or descending.
	
	Theoretically we could allow discontiguous selections; might be useful?
	'''
	# Check if there is a selection, otherwise take all lines
	ranges = tea.get_ranges(context)
	if len(ranges) == 1 and ranges[0].length == 0:
		range = tea.new_range(0, context.string().length())
		text = tea.get_selection(context, range)
	else:
		text, range = tea.get_single_selection(context, True)
	
	if text == None:
		return False

	# Split the text into lines, not maintaining the linebreaks
	lines = text.splitlines(False)
	
	# Remove duplicates if set
	if remove_duplicates:
		if direction is None:
			seen = {}
			result = []
			for x in lines:
				if x in seen: continue
				seen[x] = 1
				result.append(x)
			lines = result
		else:
			lines = list(set(lines))
	
	# Sort lines ascending or descending
	if direction == 'asc' or direction == 'desc':
		lines.sort()
		if direction == 'desc':
			lines.reverse()
	
	# If direction is random, shuffle lines
	if direction == 'random':
		random.shuffle(lines)

	# Join lines to one string
	linebreak = tea.get_line_ending(context)
	sortedText = unicode.join(linebreak, lines)
	
	# Add final linebreak if selected text has one
	if text.endswith(linebreak):
		sortedText += linebreak

	# Paste the text
	return tea.insert_text_over_range(context, sortedText, range, undo_name)
