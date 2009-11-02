'''
Zen settings loader that can read user-defined snippets from Espresso
@author: Sergey Chikuyonok (serge.che@gmail.com)
'''
import stparser
import os
import plistlib
import pickle
import re
from subprocess import Popen, PIPE

plist_path = os.path.expanduser('~/Library/Preferences/com.macrabbit.Espresso.plist')
cache_file = os.path.join(os.path.dirname(__file__), '_user_snippets.cache')

re_full_tag = re.compile(r'^<([\w\-]+(?:\:\w+)?)((?:\s+[\w\-]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*)\s*(\/?)>(?:</\1>)?')

_prev_settings = None

def _read_settings_from_app():
	plist_xml = Popen("plutil -convert xml1 -o - %s" % plist_path, stdout=PIPE, shell=True).communicate()[0]
	plist_key = 'UserSnippets1.0'
	
	data = plistlib.readPlistFromString(plist_xml)
	
	if plist_key in data:
		snippetes = {}
		abbrs = {}
		for item in data[plist_key]:
			if 'snippetString' in item and 'title' in item:
				abbr_name = 'triggerString' in item and item['triggerString'] or item['title']
				if re_full_tag.match(item['snippetString']):
					abbrs[abbr_name] = item['snippetString']
				else:
					snippetes[abbr_name] = item['snippetString']
			
		return {'common': {
			'snippets': snippetes,
			'abbreviations': abbrs
		}}
	
	return None

def load_settings():
	"""
	Load zen coding's settings, combined with user-defined snippets
	"""
	orig_date = os.path.getmtime(plist_path)
	
	need_reload = globals()['_prev_settings'] is None
	
	# check if cached file exists and up-to-date
	if not os.path.exists(cache_file) or os.path.getmtime(cache_file) < orig_date:
		# need to reparse and cache data
		_data = _read_settings_from_app()
		fp = open(cache_file, 'wb')
		pickle.dump(_data, fp)
		fp.close()
		need_reload = True
		
	if need_reload:
		fp = open(cache_file, 'rb')
		user_settings = pickle.load(fp)
		fp.close()
		globals()['_prev_settings'] = stparser.get_settings(user_settings)
		
	return globals()['_prev_settings']
