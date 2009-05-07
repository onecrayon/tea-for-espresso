#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 17, 2009

@author: Sergey Chikuyonok (http://chikuyonok.ru)
'''
from zencoding.settings import zen_settings
import re


newline = '\n'
"Character line"

insertion_point = '|'
"The symbol indicating where you want to place your cursor"

sub_insertion_point = ''
"The symbol indicating where you want to place the cursor (for the editors, which allows you to specify a few characters)"

re_tag = re.compile(r'<\/?[\w:\-]+(?:\s+[\w\-:]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*\s*(\/?)>$')

def is_allowed_char(ch):
	"""
	Checks whether a valid character in the abbreviation 
    @ param ch: The character you want to check 
    @ Type ch: str 
    @ Return: bool
	"""
	return ch.isalnum() or ch in "#.>+*:$-_!@"

def make_map(prop):
	"""
	Auxiliary function that converts a string property settings in the dictionary 
    @ param prop: the key names in the dictionary <code> zen_settings [ 'html'] </ code> 
    @ Type prop: str
	"""
	obj = {}
	for a in zen_settings['html'][prop].split(','):
		obj[a] = True
		
	zen_settings['html'][prop] = obj
	
def get_newline():
	"""
	Returns the character line that is used in the editor
	@return: str
	"""
	return newline

def pad_string(text, pad):
	"""
	Discouraging the text, indented 
    @ param text: text that you want to discourage 
    @ Type text: str 
    @ param pad: The number of indents or the indentation 
    @ Type pad: int, str 
    @ Return: str
	"""
	pad_str = ''
	result = ''
	if (type(pad) is int):
		pad_str = zen_settings['indentation'] * pad
	else:
		pad_str = pad
		
	nl = get_newline()
	lines = text.split(nl)
	result = result + lines[0]
	for line in lines[1:]:
		result += nl + pad_str + line
		
	return result

def is_snippet(abbr, doc_type = 'html'):
	"""
	Checks whether the abbreviation snippet
	@return bool
	"""
	res = zen_settings[doc_type]
	return res.has_key('snippets') and abbr in res['snippets']

def is_ends_with_tag(text):
	"""
	Checks, if a string is pumped full tag. Basically 
    used to verify the ownership character '>' abbreviation 
    Or tag 
    @ param text: text that you want to check 
    @ Type text: str 
    @ Return: bool
	"""
	return re_tag.search(text) != None

def parse_into_tree(abbr, doc_type = 'html'):
	"""
	Converts an abbreviation of the tree elements 
    @ Param abbr: Abbreviation 
    @ Type abbr: str 
    @ param doc_type: Type of document (xsl, html) 
    @ Type doc_type: str 
    @ Return: Tag
	"""
	root = Tag('', 1, doc_type)
	parent = root
	last = None
	token = re.compile(r'([\+>])?([a-z][a-z0-9:\!\-]*)(#[\w\-\$]+)?((?:\.[\w\-\$]+)*)(?:\*(\d+))?', re.IGNORECASE)
	
	def expando_replace(m):
		ex = m.group(1)
		if 'expandos' in zen_settings[doc_type] and ex in zen_settings[doc_type]['expandos']:
			return zen_settings[doc_type]['expandos'][ex]
		else:
			return ex
		
	# replace deployed elements
	abbr = re.sub(r'([a-z][a-z0-9]*)\+$', expando_replace, abbr)
	
	def token_expander(operator, tag_name, id_attr, class_name, multiplier):
		multiplier = multiplier and int(multiplier) or 1
		current = is_snippet(tag_name, doc_type) and Snippet(tag_name, multiplier, doc_type) or Tag(tag_name, multiplier, doc_type)
		
		if id_attr:
			current.add_attribute('id', id_attr[1:])
		if class_name:
			current.add_attribute('class', class_name[1:].replace('.', ' '))
			
		# moving deep into the wood
		if operator == '>' and token_expander.last:
			token_expander.parent = token_expander.last;
			
		token_expander.parent.add_child(current)
		token_expander.last = current;
		return '';
	
	token_expander.parent = root
	token_expander.last = None
	
	
	abbr = re.sub(token, lambda m: token_expander(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)), abbr)
	# If abbr blank line - this means that all the abbreviation without problems 
    # Has been transformed into a tree, if not, the acronym was not valid
	return not abbr and root or None;

def find_abbr_in_line(line, index = 0):
	"""
	Look for an abbreviation in a row and returns it 
    @ param line: The string in which you want to go 
    @ Type line: str 
    @ param index: The position of the carriage in a row 
    @ Type index: int 
    @ Return: str
	"""
	start_index = 0
	cur_index = index - 1
	while cur_index >= 0:
		ch = line[cur_index]
		if not is_allowed_char(ch) or (ch == '>' and is_ends_with_tag(line[0:cur_index + 1])):
			start_index = cur_index + 1
			break
		cur_index = cur_index - 1
		
	return line[start_index:index], start_index

def expand_abbr(abbr, doc_type = 'html'):
	"""
    Deploys abbreviation 
    @ Param abbr: Abbreviation 
    @ Type abbr: str 
    @ Return: str
	"""
	tree = parse_into_tree(abbr, doc_type)
	if tree:
		result = tree.to_string(True)
		if result:
			result = re.sub('\|', insertion_point, result, 1)
			return re.sub('\|', sub_insertion_point, result)
		
	return ''

class Tag(object):
	def __init__(self, name, count = 1, doc_type = 'html'):
		"""
		@ param name: name tag 
        @ Type name: str 
        @ param count: How many times put a tag 
        @ Type count: int 
        @ param doc_type: Type of document (xsl, html) 
        @ Type doc_type: str
		"""
		name = name.lower()
		self.name = Tag.get_real_name(name, doc_type)
		self.count = count
		self.children = []
		self.attributes = []
		self.__res = zen_settings[doc_type]
		
		if self.__res.has_key('default_attributes'):
			if name in self.__res['default_attributes']:
				def_attrs = self.__res['default_attributes'][name]
				if not isinstance(def_attrs, list):
					def_attrs = [def_attrs]
					
				for attr in def_attrs:
					for k,v in attr.items():
						self.add_attribute(k, v)
				
	@staticmethod
	def get_real_name(name, doc_type = 'html'):
		"""
		Returns the name tag 
        @ param name: The name you want to check 
        @ Type name: str 
        @ param doc_type: Type of document (xsl, html) 
        @ Type doc_type: str 
        @ Return: str
		"""
		real_name = name
		if zen_settings[doc_type].has_key('aliases'):
			aliases = zen_settings[doc_type]['aliases']
			
			if name in aliases: # abbreviation: bq -> blockquote
				real_name = aliases[name]
			elif ':' in name:
				# check whether there is a bunching selector
				group_name = name.split(':', 1)[0] + ':*'
				if group_name in aliases:
					real_name = aliases[group_name]
		
		return real_name
			
	def add_attribute(self, name, value):
		"""
		Adds an attribute 
        @ Param name: The name attribute 
        @ Type name: str 
        @ Param value: Value of attribute 
        @ Type value: str
		"""
		self.attributes.append({'name': name, 'value': value})
		
	def add_child(self, tag):
		"""
		Adds a new descendant 
        @ Param tag: descendant 
        @ Type tag: Tag
		"""
		self.children.append(tag)
	
	def __has_element(self, collection_name, def_value = False):
		if collection_name in self.__res:
			return self.name in self.__res[collection_name]
		else:
			return def_value
		
	
	def is_empty(self):
		"""
		Checks whether the current element is empty
		@return: bool
		"""
		return self.__has_element('empty_elements')
	
	def is_inline(self):
		"""
		Checks whether the current element inline
		@return: bool
		"""
		return self.__has_element('inline_elements')
	
	def is_block(self):
		"""
		Checks whether the current element block
		@return: bool
		"""
		return self.__has_element('block_elements', True)
	
	def has_block_children(self):
		"""
		Checks whether there are descendants of the current block tag. 
        Used for formatting
		@return: bool
		"""
		for tag in self.children:
			if tag.is_block():
				return True
		return False
	
	def output_children(self, format = False):
		"""
		Prints of all the descendants of the line 
        @ param format: Should I format the conclusion 
        @ Return: str
		"""
		content = ''
		for tag in self.children:
				content += tag.to_string(format, True)
				if format and tag.is_block() and self.children.index(tag) != len(self.children) - 1:
					content += get_newline()
		return content
		
	
	def to_string(self, format = False, indent = False):
		"""
		Converts the tag to a string. If there is any argument 
        <code> format </ code> - output is formatted according to the settings 
        In <code> zen_settings </ code>. Also in this case will be put 
        symbol Ç|È, meaning the insertion cursor. The cursor will be put 
        in empty attributes and elements without descendants 
        @ param format: formatted output 
        @ Type format: bool 
        @ Param indent: Add indentation 
        @ Type indent: bool 
        @ Return: str
		"""
		cursor = format and '|' or ''
		content = ''
		start_tag = ''
		end_tag = ''
		
		# doing a string of attributes
		attrs = ''.join([' %s="%s"' % (p['name'], p['value'] and p['value'] or cursor) for p in self.attributes])
		
		# display descendants
		if not self.is_empty():
			content = self.output_children(format)
			
		if self.name:
			if self.is_empty():
				start_tag = '<%s />' % (self.name + attrs,)
			else:
				start_tag, end_tag = '<%s>' % (self.name + attrs,), '</%s>' % self.name
				
		# format conclusion
		if format:
			if self.name and self.has_block_children():
				start_tag += get_newline() + zen_settings['indentation']
				end_tag = get_newline() + end_tag;
			
			if content:
				content = pad_string(content, indent and 1 or 0)
			else:
				start_tag += cursor
		
		glue = ''
		if format and self.is_block():
			glue = get_newline()
		
		result = [start_tag.replace('$', str(i + 1)) + content + end_tag for i in range(self.count)]
		return glue.join(result)
	
class Snippet(Tag):
	def __init__(self, name, count = 1, doc_type = 'html'):
		self.name = name
		self.count = count
		self.children = []
		self.__res = zen_settings[doc_type]
		
	def add_attribute(self, name = '', value = ''):
		pass
	
	def is_block(self):
		return True
	
	def to_string(self, format = False, indent = False):
		data = self.__res['snippets'][self.name]
		begin = ''
		end = ''
		content = ''
		child_padding = ''
		child_token = '${child}'
		child_indent = re.compile(r'(^\s+)')
		
		if data:
			if format:
				data = data.replace(r'\n', get_newline())
				# you need to know what a space should be available to descendants
				for line in data.split(get_newline()):
					if child_token in line:
						m = child_indent.match(line)
						child_padding = m and m.group(1) or ''
						break
			
			if child_token in data:
				begin, end = data.split(child_token, 1)
			else:
				begin = data
				
			content = self.output_children(format)
			
			if child_padding:
				content = pad_string(content, child_padding)
		
		glue = format and get_newline() or ''	
		return glue.join([begin.replace(r'\$', str(i + 1)) + content + end for i in range(self.count)])
	
		
make_map('block_elements')
make_map('inline_elements')
make_map('empty_elements')

			
if __name__ == '__main__':
	print(parse_into_tree('ul+').to_string(True))
	print(parse_into_tree('span+em').to_string(True))
	print(parse_into_tree('tmatch', 'xml').to_string(True))
	print(parse_into_tree('d', 'css').to_string(True))
	print(parse_into_tree('cc:ie6>p+blockquote#sample$.so.many.classes*2').to_string(True))

