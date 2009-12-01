#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Jul 1, 2009

@author: sergey
'''

import re

# Regular Expressions for parsing tags and attributes
start_tag = r'^<([\w\:]+)((?:\s+[\w\-:]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*)\s*(\/?)>'
end_tag = r'^<\/([\w\:]+)[^>]*>'
attr = r'([\w\-:]+)\s*=\s*([\'"]?)(.+?)\2'

def make_map(elems):
	"""
	Create dictionary of elements for faster searching
	@param elems: Elements, separated by comma
	@type elems: str
	"""
	obj = {}
	for elem in elems.split(','):
		obj[elem] = True
	
	return obj

# Empty Elements - HTML 4.01
empty = make_map("area,base,basefont,br,col,frame,hr,img,input,isindex,link,meta,param,embed");

# Block Elements - HTML 4.01
block = make_map("address,applet,blockquote,button,center,dd,dir,div,dl,dt,fieldset,form,frameset,hr,iframe,isindex,li,map,menu,noframes,noscript,object,ol,p,pre,script,table,tbody,td,tfoot,th,thead,tr,ul");

# Inline Elements - HTML 4.01
inline = make_map("a,abbr,acronym,applet,b,basefont,bdo,big,br,button,cite,code,del,dfn,em,font,i,iframe,img,input,ins,kbd,label,map,object,q,s,samp,select,small,span,strike,strong,sub,sup,textarea,tt,u,var");

# Elements that you can, intentionally, leave open
# (and which close themselves)
close_self = make_map("colgroup,dd,dt,li,options,p,td,tfoot,th,thead,tr");

# Attributes that have their values filled in disabled="disabled"
fill_attrs = make_map("checked,compact,declare,defer,disabled,ismap,multiple,nohref,noresize,noshade,nowrap,readonly,selected");

#Special Elements (can contain anything)
# serge.che: parsing data inside <scipt> elements is a "feature" 
special = make_map("style");

def parse(html, handler):
	index = None
	chars = None
	match = None
	stack = []
	last = html
	ix = 0
	
	
	def parse_start_tag(tag, tag_name, rest='', unary=False):
		if tag_name in block:
			while len(stack) and stack[-1] in inline:
				parse_end_tag('', stack[-1])
				
		if tag_name in close_self and stack[-1] == tag_name:
			parse_end_tag('', tag_name)
			
		unary = tag_name in empty or bool(unary)
		
		if not unary:
			stack.append(tag_name)
			
		if 'start' in handler:
			attrs = []
			for m in re.findall(attr, rest):
				name = m.group(1)
				value = m.group(3) or  ''
				if not value and name in fill_attrs:
					value = name
					 
				attrs.append({
					'name': name,
					'value': value,
					'escaped': re.sub(r'(^|[^\\])', '\1\\\"', value)
				})
				
			handler['start'](tag_name, attrs, unary, ix, ix + len(tag))
			
	def parse_end_tag(tag, tag_name):
#		If no tag name is provided, clean shop
		pos = 0
		
		if tag_name:
#			Find the closest opened tag of the same type
			for pos in range(len(stack) - 1, -1, -1):
				if stack[pos] == tag_name:
					break
		
		if pos >= 0:
#			Close all the open elements, up the stack
			for i in range(len(stack) - 1, pos - 1, -1):
				if 'end' in handler:
					handler['end'](stack[i], ix, ix + len(tag))
					
#			Remove the open elements from the stack
			del stack[pos:]
	
	if 'stop' not in handler:
		handler['stop'] = False
	
	while html and not handler['stop']:
		chars = True
		
#		Make sure we're not in a script or style element
		if not len(stack) or stack[-1] not in special:
#			comment
			if html.find('<!--') == 0:
				index = html.find('-->')
				
				if index >= 0:
					if 'comment' in handler:
						handler['comment'](html[4:index], ix, ix + index + 3)
					html = html[index + 3:]
					ix += index + 3
					chars = False
			
#			doctype declaration
			elif html.find('<!DOCTYPE') == 0:
				index = html.find('>')
				
				if index >= 0:
					html = html[index + 1:]
					ix += index + 1
					chars = False
			
#			end tag
			elif html.find('</') == 0:
				match = re.match(end_tag, html)
				if match:
					html = html[len(match.group(0)):]
					re.sub(end_tag, lambda m: parse_end_tag(m.group(0), m.group(1)), match.group(0))
					ix += len(match.group(0))
					chars = False
				
#			start tag	
			elif html.find('<') == 0:
				match = re.match(start_tag, html)
				
				if match:
					html = html[len(match.group(0)):]
					re.sub(start_tag, lambda m: parse_start_tag(m.group(0), m.group(1)), match.group(0))
					ix += len(match.group(0))
					chars = False
					
			if chars:
				index = html.find('<')
				text = index < 0 and html or html[0:index]
				html = index < 0 and '' or html[index:]
				
				if index > -1:
					ix += index
				
				if 'chars' in handler:
					handler['chars'](text)
					
		else:
			def __repl(m):
				"""
				@type m: MatchObject
				"""
				text = m.group(1)
				text = re.sub(r'<!--(.*?)-->', '\1', text)
				text = re.sub(r'<!\[CDATA\[(.*?)]]>', '\1', text)
				
				if 'chars' in handler:
					handler['chars'](text)
					
				return ''
				
			html = re.sub("^(.*)<\\/" + stack[-1] + "[^>]*>", __repl, html)
			
			parse_end_tag('', stack[-1])
			
		if html == last:
			raise RuntimeError('Parse Error: ' + html)
		
		last = html
	
#	Clean up any remaining tags
	parse_end_tag('', '')
	
	
if __name__ == '__main__':
	def start_h(tag_name, attrs, unary, start_ix, end_ix):
		print('found <%s> at %d:%d' % (tag_name, start_ix, end_ix))
		
	def end_h(tag_name, start_ix, end_ix):
		print('found </%s> at %d:%d' % (tag_name, start_ix, end_ix))
		
	def chars_h(chars):
		print('found %s' % (chars,))
		
	parse('<div>Hello <br/> <some:ns xx:df="sd" d="sds">sdfsdf</some:ns> <strong class="demo">world</strong></div>', {'start': start_h, 'end': end_h, 'chars': chars_h})
	
