<p>import re
import markdown
from markdown import Extension
from markdown.util import etree
from markdown.blockprocessors import BlockProcessor</p>
<p>import sys</p>
<p>class BoxBlockProcessor(BlockProcessor):
    RE_FENCE_START = r"{: <em>([\s\S]</em>?)}([\s\S]<em>?)"
    RE_FENCE_END = r"{ </em>: *}"</p>
<pre><code>def test(self, parent, block):
    return re.match(self.RE_FENCE_START, block)

def run(self, parent, blocks):
    original_block = blocks[0]
    blocks[0] = re.sub(self.RE_FENCE_START, "", blocks[0])
    match = re.match(self.RE_FENCE_START, original_block)
    style = match.group(1)
    print(style)
    content = match.group(0)
    print("&gt;", content)

    for block_num, block in enumerate(blocks):
        if re.search(self.RE_FENCE_END, block):
            blocks[block_num] = re.sub(self.RE_FENCE_END, "", block)
            e = etree.SubElement(parent, "div")
            e.set("style", style)
            self.parser.parseBlocks(e, blocks[0 : block_num + 1])
            for i in range(0, block_num + 1):
                blocks.pop(0)
            return True
    blocks[0] = original_block
    return False
</code></pre>
<p>class BoxExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), "box", 175)</p>
<p>input_md = sys.argv[0] or "test.md"
output_html = sys.argv[1] or (input_md.split(".")[0] + ".html")</p>
<p>with open(input_md, "r") as f:
    text = f.read()</p>
<pre><code>md = markdown.Markdown(extensions=[BoxExtension()])
html = md.convert(text)

with open(output_html, "w") as f:
    f.write(html)
</code></pre>