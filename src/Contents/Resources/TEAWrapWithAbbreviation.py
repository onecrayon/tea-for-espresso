'''
@author: Sergey Chikuyonok (serge.che@gmail.com)
'''
'''Class for wrapping text with ZenCoding's abbreviations'''

import re

from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
import objc
from zencoding import settings_loader

from TEAforEspresso import TEAforEspresso
import tea_actions as tea

from zencoding import zen_core as zen
from zencoding import html_matcher as html_matcher

class TEAWrapWithAbbreviation(TEAforEspresso):
	'''Class for entabbing and detabbing current document or selection'''
	customSheet = objc.IBOutlet()
	abbr = objc.IBOutlet()
	spinner = objc.IBOutlet()
	
	undo_name = 'Wrap with Abbreviation'
	
	@objc.signature('B@:@@')
	def performActionWithContext_error_(self, context, error):
		'''
		Gets the user's abbreviation
		'''
		# Load the sheet
		if not self.customSheet:
			NSBundle.loadNibNamed_owner_('TEAEnterAbbreviation', self)
		
		# Set up the default number
#		prefs = tea.get_prefs(context)
#		num_spaces = prefs.numberOfSpacesForTab()
#		self.abbr.setStringValue_(num_spaces)
		
		NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
			self.customSheet,
			context.windowForSheet(),
			self,
			'didEndSheet:returnCode:contextInfo:',
			None
		)
		# Save the context for later reference (once the sheet is complete)
		self.context = context
		# Because this gets passed through to Obj-C, using int prevents beeping
		return True
	
	@objc.IBAction
	def doSubmitSheet_(self, sender):
		NSApp.endSheet_returnCode_(self.customSheet, 1)
	
	@objc.IBAction
	def cancel_(self, sender):
		NSApp.endSheet_returnCode_(self.customSheet, 0)
	
	@AppHelper.endSheetMethod
	def didEndSheet_returnCode_contextInfo_(self, sheet, code, info):
		def replacements(match):
			'''Utility function for replacing items'''
			return match.group(0).replace(self.search, self.replace)
		
		if code == 1:
			# Leave sheet open with "processing" spinner
			self.spinner.startAnimation_(self)
			wrap(self.context, self.abbr.stringValue(), self.undo_name)
			self.spinner.stopAnimation_(self)
		
		sheet.orderOut_(self)
		

def safe_str(text):
	"""
	Creates safe string representation to deal with Python's encoding issues
	"""
	return text.encode('utf-8')

def wrap(context, abbr, undo_name, profile_name='xhtml'):
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
	
	text, rng = tea.get_single_selection(context)
	if text == None:
		# no selection, find matching tag
		content = context.string()
		start, end = html_matcher.match(content, rng.location)
		if start is None:
			# nothing to wrap
			return False
		
		def is_space(char):
			return char.isspace() or char in r'\n\r'
		
		# narrow down selection untill first non-space character
		while start < end:
			if not is_space(content[start]):
				break
			start += 1
			
		while end > start:
			if not is_space(content[end]):
				break
			end -= 1
		
#		last = html_matcher.last_match
#		start = last['opening_tag'].start
#		end = last['closing_tag'] and last['closing_tag'].end or last['opening_tag'].end
		
		tea.set_selected_range(context, tea.new_range(start, end - start))
		text, rng = tea.get_single_selection(context)
		
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
	result = unicode(result, 'utf-8')
	
	result = tea.indent_snippet(context, result, rng)
	return tea.insert_snippet_over_range(context, result, rng, undo_name)

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