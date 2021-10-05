from markdown.preprocessors import Preprocessor
import markdown
import re
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from collections import OrderedDict


class SubstitutionPreprocessor(Preprocessor):

    def __init__(self, substitutions):
        super().__init__()
        self.substitutions = substitutions

    def run(self, lines):
        new_lines = []
        for line in lines:
            for pattern, subn in self.substitutions.items():
                line = line.replace(pattern, subn)
            new_lines.append(line)
        return new_lines


class SubstitutionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('subn', SubstitutionPreprocessor(md), '_begin')


substitutions = OrderedDict([
    ('hi', 'sup lil turd'),
    ('hello', 'bello'),
    ('Python 2', 'Python&nbsp;2'),
    ('Python 3', 'Python&nbsp;3'),
    ('JK Rowling', 'JK&nbsp;Rowling'),

    ('LATEX', '<span class="latex">L<sup>a</sup>T<sub>e</sub>X</span>'),
])

text = """
hi hello Python 2 Python 3 JK Rowling
"""

subn_extension = SubstitutionExtension(substitutions)
    
        
print(markdown.markdown(text))
# print(markdown.markdown('# hi _hello_ hihi', extensions=[BoxExtension(), 'test-thingy', 'BoxExtension']))