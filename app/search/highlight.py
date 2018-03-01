from haystack.utils import Highlighter
from django.utils.html import strip_tags


class GluuHighlighter(Highlighter):

    def highlight(self, text_block):
        self.text_block = strip_tags(text_block)
        highlight_locations = self.find_highlightable_words()
        start_offset, end_offset = self.find_window(highlight_locations)
        text_len = len(self.text_block)

        if text_len <= self.max_length:
            start_offset = 0
        elif (text_len - 1 - start_offset) <= self.max_length:
            end_offset = text_len
            start_offset = end_offset - self.max_length

        if start_offset < 0:
            start_offset = 0
        return self.render_html(highlight_locations, start_offset, end_offset)
