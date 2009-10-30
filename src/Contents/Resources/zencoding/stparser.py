'''
Zen Coding's settings parser
Created on Jun 14, 2009

@author: sergey
'''

import re
import types


TYPE_ABBREVIATION = 'zen-tag',
TYPE_EXPANDO = 'zen-expando',
TYPE_REFERENCE = 'zen-reference';
""" Reference to another abbreviation or tag """

re_tag = r'^<([\w\-]+(?:\:\w+)?)((?:\s+[\w\-]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*)\s*(\/?)>'
"Regular expression for XML tag matching"
	
re_attrs = r'([\w\-]+)\s*=\s*([\'"])(.*?)\2'
"Regular expression for matching XML attributes"

class Entry:
	"""
	Unified object for parsed data
	"""
	def __init__(self, entry_type, key, value):
		"""
		@type entry_type: str
		@type key: str
		@type value: dict
		"""
		self.type = entry_type
		self.key = key
		self.value = value

def _make_expando(key, value):
	"""
	Make expando from string
	@type key: str
	@type value: str
	@return: Entry
	"""
	return Entry(TYPE_EXPANDO, key, value)

def _make_abbreviation(key, tag_name, attrs, is_empty=False):
	"""
	Make abbreviation from string
	@param key: Abbreviation key
	@type key: str
	@param tag_name: Expanded element's tag name
	@type tag_name: str
	@param attrs: Expanded element's attributes
	@type attrs: str
	@param is_empty: Is expanded element empty or not
	@type is_empty: bool
	@return: dict
	"""
	result = {
		'name': tag_name,
		'is_empty': is_empty
	};
	
	if attrs:
		result['attributes'] = [];
		for m in re.findall(re_attrs, attrs):
			result['attributes'].append({
				'name': m[0],
				'value': m[2]
			})
			
	return Entry(TYPE_ABBREVIATION, key, result)

def _parse_abbreviations(obj):
	"""
	Parses all abbreviations inside dictionary
 	@param obj: dict
	"""
	for key, value in obj.items():
		key = key.strip()
		if key[-1] == '+':
#			this is expando, leave 'value' as is
			obj[key] = _make_expando(key, value)
		else:
			m = re.search(re_tag, value)
			if m:
				obj[key] = _make_abbreviation(key, m.group(1), m.group(2), (m.group(3) == '/'))
			else:
#				assume it's reference to another abbreviation
				obj[key] = Entry(TYPE_REFERENCE, key, value)

def parse(settings):
	"""
	Parse user's settings. This function must be called *before* any activity
	in zen coding (for example, expanding abbreviation)
 	@type settings: dict
	"""
	for p, value in settings.items():
		if p == 'abbreviations':
			_parse_abbreviations(value)
		elif p == 'extends':
			settings[p] = [v.strip() for v in value.split(',')]
		elif type(value) == types.DictType:
			parse(value)


def extend(parent, child):
	"""
	Recursevly extends parent dictionary with children's keys. Used for merging
	default settings with user's
	@type parent: dict
	@type child: dict
	"""
	for p, value in child.items():
		if type(value) == types.DictType:
			extend(parent[p], value)
		else:
			parent[p] = value


def create_maps(obj):
	"""
	Create hash maps on certain string properties of zen settings
	@type obj: dict
	"""
	for p, value in obj.items():
		if p == 'element_types':
			for k, v in value.items(): 
				value[k] = [el.strip() for el in v.split(',')]
		elif type(value) == types.DictType:
			create_maps(value)


if __name__ == '__main__':
	pass