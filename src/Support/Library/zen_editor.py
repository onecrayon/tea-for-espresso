'''
High-level editor interface that communicates with underlying editor (like
Espresso, Coda, etc.) or browser.
Basically, you should call <code>set_context(obj)</code> method to
set up undelying editor context before using any other method.

This interface is used by <i>zen_actions.py</i> for performing different
actions like <b>Expand abbreviation</b>

@example
import zen_editor
zen_editor.set_context(obj);
//now you are ready to use editor object
zen_editor.get_selection_range();

@author Sergey Chikuyonok (serge.che@gmail.com)
@link http://chikuyonok.ru
'''
import tea_actions as tea
import zen_settings_loader
from zencoding import zen_core as zen
import re

class ZenEditor():
    def __init__(self, context):
        self._context = None
        self.zen_settings = zen_settings_loader.load_settings()
        zen.update_settings(self.zen_settings)
        
        if context:
            self.set_context(context)
        
    def set_context(self, context):
        """
        Setup underlying editor context. You should call this method
        <code>before</code> using any Zen Coding action.
        @param context: context object
        """
        self._context = context
        zen.newline = self.safe_str(tea.get_line_ending(context))
        self.zen_settings['variables']['indentation'] = self.safe_str(tea.get_indentation_string(context))
        
    def get_selection_range(self):
        """
        Returns character indexes of selected text
        @return: list of start and end indexes
        @example
        start, end = zen_editor.get_selection_range();
        print('%s, %s' % (start, end))
        """
        rng = tea.get_first_range(self._context)
        return rng.location, rng.location + rng.length
        
    def create_selection(self, start, end=None):
        """
        Creates selection from <code>start</code> to <code>end</code> character
        indexes. If <code>end</code> is ommited, this method should place caret
        and <code>start</code> index
        @type start: int
        @type end: int
        @example
        zen_editor.create_selection(10, 40)
        # move caret to 15th character
        zen_editor.create_selection(15)
        """
        if end is None: end = start
        new_range = tea.new_range(start, end - start)
        tea.set_selected_range(self._context, new_range)
        
    def get_current_line_range(self):
        """
        Returns current line's start and end indexes
        @return: list of start and end indexes
        @example
        start, end = zen_editor.get_current_line_range();
        print('%s, %s' % (start, end))
        """
        rng = tea.get_ranges(self._context)[0]
        text, rng = tea.get_line(self._context, rng)
        return rng.location, rng.location + rng.length
        
    def get_caret_pos(self):
        """ Returns current caret position """
        range = tea.get_ranges(self._context)[0]
        return range.location
        
    def set_caret_pos(self, pos):
        """
        Set new caret position
        @type pos: int
        """
        self.create_selection(pos)
        
    def get_current_line(self):
        """
        Returns content of current line
        @return: str
        """
        rng = tea.get_ranges(self._context)[0]
        text, rng = tea.get_line(self._context, rng)
        return text
            
    def replace_content(self, value, start=None, end=None, undo_name = 'Replace content'):
        """
        Replace editor's content or it's part (from <code>start</code> to
        <code>end</code> index). If <code>value</code> contains
        <code>caret_placeholder</code>, the editor will put caret into
        this position. If you skip <code>start</code> and <code>end</code>
        arguments, the whole target's content will be replaced with
        <code>value</code>.
        
        If you pass <code>start</code> argument only,
        the <code>value</code> will be placed at <code>start</code> string
        index of current content.
        
        If you pass <code>start</code> and <code>end</code> arguments,
        the corresponding substring of current target's content will be
        replaced with <code>value</code>
        @param value: Content you want to paste
        @type value: str
        @param start: Start index of editor's content
        @type start: int
        @param end: End index of editor's content
        @type end: int
        """
        if start is None: start = 0
        if end is None: end = len(self.get_content())
        rng = tea.new_range(start, end - start)
        value = self.add_placeholders(value)
        tea.insert_snippet_over_range(self._context, value, rng, undo_name)
        
    def get_content(self):
        """
        Returns editor's content
        @return: str
        """
        return self._context.string()
        
    def get_syntax(self):
        """
        Returns current editor's syntax mode
        @return: str
        """
        zones = {
            'css, css *': 'css',
            'xsl, xsl *': 'xsl',
            'xml, xml *': 'xml',
            'haml, haml *': 'haml'
        }
        rng = tea.get_first_range(self._context)
        return tea.select_from_zones(self._context, rng, 'html', **zones)
        
    def get_profile_name(self):
        """
        Returns current output profile name (@see zen_coding#setup_profile)
        @return {String}
        """
        close_string = tea.get_tag_closestring(self._context)
        if close_string == '/':
            return 'xml'
        elif close_string != ' /':
            return 'html'
        else:
            return 'xhtml'
        
    def safe_str(self, text):
        """
        Creates safe string representation to deal with Python's encoding issues
        """
        return text.encode('utf-8')
        
    def add_placeholders(self, text):
        _ix = [0]
        
        def get_ix(m):
            _ix[0] += 1
            return '$%s' % _ix[0]
        
        text = re.sub(r'\$', '\\$', text)
        return re.sub(zen.get_caret_placeholder(), get_ix, text)
