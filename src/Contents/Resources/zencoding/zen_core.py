#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Apr 17, 2009

@author: Sergey Chikuyonok (http://chikuyonok.ru)
'''
from zencoding.zen_settings import zen_settings
import re
import stparser

newline = '\n'
"Символ перевода строки"

insertion_point = '|'
"Символ, указывающий, куда нужно поставить курсор"

sub_insertion_point = ''
"Символ, указывающий, куда нужно поставить курсор (для редакторов, которые позволяют указать несколько символов)"

re_tag = re.compile(r'<\/?[\w:\-]+(?:\s+[\w\-:]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*\s*(\/?)>$')

profiles = {}

default_profile = {
	'tag_case': 'lower',         # values are 'lower', 'upper'
	'attr_case': 'lower',        # values are 'lower', 'upper'
	'attr_quotes': 'double',     # values are 'single', 'double'
	
	'tag_nl': 'decide',          # each tag on new line, values are True, False, 'decide'
	
	'place_cursor': True,        # place cursor char — | (pipe) — in output
	
	'indent': True,              # indent tags
	
	'self_closing_tag': 'xhtml'  # use self-closing style for writing empty elements, e.g. <br /> or <br>. 
                                 # values are True, False, 'xhtml'
}

def has_deep_key(obj, key):
	"""
	Check if <code>obj</code> dictionary contains deep key. For example,
	example, it will allow you to test existance of my_dict[key1][key2][key3],
	testing existance of my_dict[key1] first, then my_dict[key1][key2], 
	and finally my_dict[key1][key2][key3]
	@param obj: Dictionary to test
	@param obj: dict
	@param key: Deep key to test. Can be list (like ['key1', 'key2', 'key3']) or
	string (like 'key1.key2.key3')
	@type key: list, tuple, str
	@return: bool
	"""
	if isinstance(key, str):
		key = key.split('.')
		
	last_obj = obj
	for v in key:
		if not last_obj.has_key(v):
			return False
		last_obj = last_obj[v]
	
	return True
		

def is_allowed_char(ch):
	"""
	Проверяет, является ли символ допустимым в аббревиатуре
	@param ch: Символ, который нужно проверить
	@type ch: str
	@return: bool
	"""
	return ch.isalnum() or ch in "#.>+*:$-_!@"

def make_map(prop):
	"""
	Вспомогательная функция, которая преобразовывает строковое свойство настроек в словарь
	@param prop: Названия ключа в словаре <code>zen_settings['html']</code>
	@type prop: str
	"""
	obj = {}
	for a in zen_settings['html'][prop].split(','):
		obj[a] = True
		
	zen_settings['html'][prop] = obj

def create_profile(options):
	"""
	Create profile by adding default values for passed optoin set
	@param options: Profile options
	@type options: dict
	"""
	for k, v in default_profile.items():
		options.setdefault(k, v)
	
	return options

def setup_profile(name, options = {}):
	"""
	@param name: Profile name
	@type name: str
	@param options: Profile options
	@type options: dict
	"""
	profiles[name.lower()] = create_profile(options);

def get_newline():
	"""
	Возвращает символ перевода строки, используемый в редакторе
	@return: str
	"""
	return newline

def pad_string(text, pad):
	"""
	Отбивает текст отступами
	@param text: Текст, который нужно отбить
	@type text: str
	@param pad: Количество отступов или сам отступ
	@type pad: int, str
	@return: str
	"""
	pad_str = ''
	result = ''
	if (type(pad) is int):
		pad_str = zen_settings['variables']['indentation'] * pad
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
	Check is passed abbreviation is snippet
	Проверяет, является ли аббревиатура сниппетом
	@return bool
	"""
	return get_snippet(doc_type, abbr) and True or False

def is_ends_with_tag(text):
	"""
	Проверяет, закачивается ли строка полноценным тэгом. В основном 
	используется для проверки принадлежности символа '>' аббревиатуре 
	или тэгу
	@param text: Текст, который нужно проверить
	@type text: str
	@return: bool
	"""
	return re_tag.search(text) != None

def get_elements_collection(resource, type):
	"""
	Returns specified elements collection (like 'empty', 'block_level') from
	<code>resource</code>. If collections wasn't found, returns empty object
	@type resource: dict
	@type type: str
	@return: dict
	"""
	if 'element_types' in resource and type in resource['element_types']:
		return resource['element_types'][type]
	else:
		return {}
	
def replace_variables(text):
	"""
	Replace variables like ${var} in string
	@param text: str
	@return: str
	"""
	return re.sub(r'\$\{([\w\-]+)\}', lambda s, p1: p1 in zen_settings['variables'] and zen_settings['variables'][p1] or s, text)

def get_abbreviation(res_type, abbr):
	"""
	Returns abbreviation value from data set
	@param res_type: Resource type (html, css, ...)
	@type res_type: str
	@param abbr: Abbreviation name
	@type abbr: str
	@return dict, None
	"""
	return get_settings_resource(res_type, abbr, 'abbreviations')

def get_snippet(res_type, snippet_name):
	"""
	Returns snippet value from data set
	@param res_type: Resource type (html, css, ...)
	@type res_type: str
	@param snippet_name: Snippet name
	@type snippet_name: str
	@return dict, None
	"""
	return get_settings_resource(res_type, snippet_name, 'snippets');

def get_settings_resource(res_type, abbr, res_name):
	"""
	Returns resurce value from data set with respect of inheritance
	@param res_type: Resource type (html, css, ...)
	@type res_type: str
	@param abbr: Abbreviation name
	@type abbr: str
	@param res_name: Resource name ('snippets' or 'abbreviation')
	@type res_name: str
	@return dict, None
	"""
	
	if zen_settings.has_key(res_type):
		resource = zen_settings[res_type];
		if (has_deep_key(resource, [res_name, abbr])):
			return resource[res_name][abbr]
		elif 'extends' in resource:
	#		find abbreviation in ancestors
			for v in resource['extends']:
				if has_deep_key(zen_settings, [v, res_name, abbr]):
					return zen_settings[v][res_name][abbr]
	return None;


def parse_into_tree(abbr, doc_type = 'html'):
	"""
	Преобразует аббревиатуру в дерево элементов
	@param abbr: Аббревиатура
	@type abbr: str
	@param doc_type: Тип документа (xsl, html)
	@type doc_type: str
	@return: Tag
	"""
	root = Tag('', 1, doc_type)
	parent = root
	last = None
	res = zen_settings.has_key(doc_type) and zen_settings[doc_type] or {}
	token = re.compile(r'([\+>])?([a-z@\!][a-z0-9:\-]*)(#[\w\-\$]+)?((?:\.[\w\-\$]+)*)(?:\*(\d+))?', re.IGNORECASE)
	
	def expando_replace(m):
		ex = m.group(0)
		a = get_abbreviation(doc_type, ex)
		return a and a.value or ex
		
	def token_expander(operator, tag_name, id_attr, class_name, multiplier):
		
		multiplier = multiplier and int(multiplier) or 1
		current = is_snippet(tag_name, doc_type) and Snippet(tag_name, multiplier, doc_type) or Tag(tag_name, multiplier, doc_type)
		
		if id_attr:
			current.add_attribute('id', id_attr[1:])
		if class_name:
			current.add_attribute('class', class_name[1:].replace('.', ' '))
			
		# двигаемся вглубь дерева
		if operator == '>' and token_expander.last:
			token_expander.parent = token_expander.last;
			
		token_expander.parent.add_child(current)
		token_expander.last = current;
		return '';
		
	# заменяем разворачиваемые элементы
	abbr = re.sub(r'([a-z][a-z0-9]*)\+$', expando_replace, abbr)
	
	token_expander.parent = root
	token_expander.last = None
	
	
	abbr = re.sub(token, lambda m: token_expander(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)), abbr)
	# если в abbr пустая строка — значит, вся аббревиатура без проблем 
	# была преобразована в дерево, если нет, то аббревиатура была не валидной
	return not abbr and root or None;

def find_abbr_in_line(line, index = 0):
	"""
	Ищет аббревиатуру в строке и возвращает ее
	@param line: Строка, в которой нужно искать
	@type line: str
	@param index: Позиция каретки в строке
	@type index: int
	@return: str
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

def expand_abbreviation(abbr, doc_type = 'html', profile_name = 'plain'):
	"""
	Разворачивает аббревиатуру
	@param abbr: Аббревиатура
	@type abbr: str
	@return: str
	"""
	tree = parse_into_tree(abbr, doc_type)
	if tree:
		result = tree.to_string(profile_name)
		if result:
			result = re.sub('\|', insertion_point, result, 1)
			return  replace_variables(re.sub('\|', sub_insertion_point, result))
		
	return ''

def get_pair_range(text, cursor_pos):
	"""
	Returns range that indicates starting and ending pair tags nearest 
	to cursor position.
	@param text: Full document
	@type text: str
	@param cursor_pos: Caret position inside document
	@type cursor_pos: int
	@return: list of start and end indices. If pair wasn't found, returns (-1, -1)
	"""
	
	import htmlparser
	
	tags = {}
	ranges = []
	result = [-1, -1]
	
	handler = {'stop': False}
	
	def in_range(start, end):
		return cursor_pos > start and cursor_pos <= end
	
	def start_h(name, attrs, unary, ix_start, ix_end):
		if unary and in_range(ix_start, ix_end):
			result[0] = ix_start
			result[1] = ix_end
			handler['stop'] = True
		else:
			if name not in tags:
				tags[name] = []
			
			tags[name].append(ix_start)
			
	def end_h(name, ix_start, ix_end):
		if name in tags:
			start = tags[name].pop()
			if in_range(start, ix_end):
				ranges.append([start, ix_end])
	
	def comment_h(data, ix_start, ix_end):
		if in_range(ix_start, ix_end):
			result[0] = ix_start
			result[1] = ix_end
			handler['stop'] = True
			
	handler['start'] = start_h
	handler['end'] = end_h
	handler['comment'] = comment_h
	
	try:
		htmlparser.parse(text, handler)
	except RuntimeError:
		pass
	
	if result[0] == -1 and len(ranges):
#		because we have overlaped ranges only, we have to sort array by 
#		length: the shorter range length, the most probable match
		ranges.sort(lambda a, b: (a[1] - a[0]) - (b[1] - b[0]))
		result = ranges[0]
		
	return result


class Tag(object):
	def __init__(self, name, count = 1, doc_type = 'html'):
		"""
		@param name: Имя тэга
		@type name: str
		@param count:  Сколько раз вывести тэг
		@type count: int
		@param doc_type: Тип документа (xsl, html)
		@type doc_type: str
		"""
		name = name.lower()
		
		abbr = get_abbreviation(doc_type, name)
		if abbr and abbr.type == stparser.TYPE_REFERENCE:
			abbr = get_abbreviation(doc_type, abbr.value)
		
		self.name = abbr and abbr.value['name'] or name
		self.count = count
		self.children = []
		self.attributes = []
		self.__attr_hash = {}
		self.__abbr = abbr
		self.__res = zen_settings.has_key(doc_type) and zen_settings[doc_type] or {}
		
		if self.__abbr and 'attributes' in self.__abbr.value:
			for a in self.__abbr.value['attributes']:
				self.add_attribute(a['name'], a['value'])
		
	def add_attribute(self, name, value):
		"""
		Add attribute to tag. If the attribute with the same name already exists,
		it will be overwritten, but if it's name is 'class', it will be merged
		with the existed one
		@param name: Attribute nama
		@type name: str
		@param value: Attribute value
		@type value: str
		"""
		if name in self.__attr_hash:
#			attribue already exists
			a = self.__attr_hash[name]
			if name == 'class':
#				'class' is a magic attribute
				if a['value']:
					value = ' ' + value
				a['value'] += value
			else:
				a['value'] = value
		else:
			a = {'name': name, 'value': value}
			self.__attr_hash[name] = a
			self.attributes.append(a)
		
	def add_child(self, tag):
		"""
		Добавляет нового потомка
		@param tag: Потомок
		@type tag: Tag
		"""
		self.children.append(tag)
	
	def __has_element(self, collection_name, def_value = False):
		if collection_name in self.__res:
			return self.name in self.__res[collection_name]
		else:
			return def_value
		
	
	def is_empty(self):
		"""
		Проверяет, является ли текущий элемент пустым
		@return: bool
		"""
		
		return (self.__abbr and self.__abbr.value['is_empty']) or \
			self.name in get_elements_collection(self.__res, 'empty')
	
	def is_inline(self):
		"""
		Проверяет, является ли текущий элемент строчным
		@return: bool
		"""
		return self.name in get_elements_collection(self.__res, 'inline_level')
	
	def is_block(self):
		"""
		Проверяет, является ли текущий элемент блочным
		@return: bool
		"""
		return self.name in get_elements_collection(self.__res, 'block_level')
	
	def has_block_children(self):
		"""
		Проверяет, есть ли блочные потомки у текущего тэга. 
		Используется для форматирования
		@return: bool
		"""
		for tag in self.children:
			if tag.is_block():
				return True
		return False
	
	def output_children(self, profile_name):
		"""
		Выводит всех потомков в виде строки
		@type profile_name: str
		@return: str
		"""
		content = ''
		profile = profile_name in profiles and profiles[profile_name] or profiles['plain']
		for tag in self.children:
				content += tag.to_string(profile_name)
				
				if self.children.index(tag) != len(self.children) - 1 and \
					(profile['tag_nl'] == True or \
					(profile['tag_nl'] == 'decide' and tag.is_block())):
						content += get_newline()
		return content
		
	
	def to_string(self, profile_name):
		"""
		Преобразует тэг в строку. Если будет передан аргумент 
		<code>format</code> — вывод будет отформатирован согласно настройкам
		в <code>zen_settings</code>. Также в этом случае будет ставится 
		символ «|», означающий место вставки курсора. Курсор будет ставится
		в пустых атрибутах и элементах без потомков
		@type profile_name: string
		@return: str
		"""
		
		profile = profile = profile_name in profiles and profiles[profile_name] or profiles['plain']
		attrs = '' 
		content = '' 
		start_tag = '' 
		end_tag = ''
		attr_quote = profile['attr_quotes'] == 'single' and "'" or '"'
		cursor = profile['place_cursor'] and '|' or ''
		self_closing = ''
		
		if profile['self_closing_tag'] == 'xhtml':
			self_closing = ' /'
		elif profile['self_closing_tag'] == True:
			self_closing = '/'
			
		# делаем строку атрибутов
		for a in self.attributes:
			if profile['attr_case'] == 'upper':
				attr_name = a['name'].upper()
			else:
				attr_name = a['name'].lower()
				
			attrs += ' %s=%s%s%s' % (attr_name, attr_quote, a['value'] or cursor, attr_quote)
		
		# выводим потомков
		if not self.is_empty():
			content = self.output_children(profile_name)
			
		if self.name:
			tag_name = profile['tag_case'] == 'upper' and self.name.upper() or self.name.lower()
			if self.is_empty():
				start_tag = '<%s%s%s>' % (tag_name, attrs, self_closing)
			else:
				start_tag, end_tag = '<%s%s>' % (tag_name, attrs), '</%s>' % tag_name
				
		# форматируем вывод
		glue = ''
		if profile['tag_nl'] != False:
			if self.name and (profile['tag_nl'] == True or self.has_block_children()):
				if not self.is_empty():
					start_tag += get_newline() + zen_settings['variables']['indentation']
					end_tag = get_newline() + end_tag
				
		
			if self.name:
				if content:
					content = pad_string(content, profile['indent'] and 1 or 0)
				else:
					start_tag += cursor
		
			if profile['tag_nl'] == True or self.is_block():
				glue = get_newline()
		
		
		result = [start_tag.replace('$', str(i + 1)) + content + end_tag for i in range(self.count)]
		return glue.join(result)
	
class Snippet(Tag):
	def __init__(self, name, count = 1, doc_type = 'html'):
		self.name = name
		self.count = count
		self.children = []
		self.value = get_snippet(doc_type, name)
		self.__res = zen_settings[doc_type]
		
	def add_attribute(self, name = '', value = ''):
		pass
	
	def is_block(self):
		return True
	
	def to_string(self, profile_name):
		content = ''
		profile = profile_name in profiles and profiles[profile_name] or profiles['plain']
		result = []
		data = self.value
		begin = ''
		end = ''
		glue = ''
		child_padding = ''
		child_token = '${child}'
		child_indent = re.compile(r'(^\s+)')
		
		if data:
			if profile['tag_nl'] != False:
				data = data.replace(r'\n', get_newline())
				# нужно узнать, какой отступ должен быть у потомков
				for line in data.split(get_newline()):
					if child_token in line:
						m = child_indent.match(line)
						child_padding = m and m.group(1) or ''
						break
					
				glue = get_newline()
			
			if child_token in data:
				begin, end = data.split(child_token, 1)
			else:
				begin = data
				
			content = self.output_children(profile_name)
			
			if child_padding:
				content = pad_string(content, child_padding)
		
		return glue.join([begin.replace(r'\$', str(i + 1)) + content + end for i in range(self.count)])
	
		
# create default profiles
setup_profile('xhtml');
setup_profile('html', {'self_closing_tag': False});
setup_profile('xml', {'self_closing_tag': True, 'tag_nl': True});
setup_profile('plain', {'tag_nl': False, 'indent': False, 'place_cursor': False});

# init settings
# first we need to expand some strings into hashes
stparser.create_maps(zen_settings)
if hasattr(globals(), 'my_zen_settings'):
#	# we need to extend default settings with user's
	stparser.create_maps(my_zen_settings)
	stparser.extend(zen_settings, my_zen_settings)

# now we need to parse final set of settings
stparser.parse(zen_settings)

#if __name__ == '__main__':
#	print(parse_into_tree('ul+').to_string(True))
#	print(parse_into_tree('span+em').to_string(True))
#	print(parse_into_tree('tmatch', 'xml').to_string(True))
#	print(parse_into_tree('d', 'css').to_string(True))
#	print(parse_into_tree('cc:ie6>p+blockquote#sample$.so.many.classes*2').to_string(True))
