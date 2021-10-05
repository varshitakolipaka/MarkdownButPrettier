import markdown


import re
from markdown.util import etree
from markdown import Extension
from markdown.blockprocessors import BlockProcessor


class DivStylesProcessor(BlockProcessor):
    # RE_FENCE = r"{: *((.|\n)*? *)}((\n|.)*)({ *?: *?})"

    # RE_FENCE_START = r"{: *((.|\n)*? *)}((\n|.)*)"
    # RE_FENCE_END = r"({ *?: *?})"

    RE_FENCE = r"{(: *(.|\n)*? *)}\n((.|\n)*){:}"

    RE_FENCE_START = r"{(: *(.|\n)*? *)}\n((.|\n)*)"
    RE_FENCE_END = r"{:}"

    def run(self, parent, blocks):
        original_block = blocks[0]

        pattern = re.compile(self.RE_FENCE_START)
        match = pattern.search(blocks[0])
        style = match.group(3)
        blocks[0] = re.sub(self.RE_FENCE_START, "", blocks[0])

        # Find block with ending fence
        for block_num, block in enumerate(blocks):
            if re.search(self.RE_FENCE_END, block):
                # remove fence
                blocks[block_num] = re.sub(self.RE_FENCE_END, "", block)
                # render fenced area inside a new div
                e = etree.SubElement(parent, "div")
                print("style found: ", style)
                e.set("style", style)
                self.parser.parseBlocks(e, blocks[0 : block_num + 1])
                # remove used blocks
                for i in range(0, block_num + 1):
                    blocks.pop(0)
                return True  # or could have had no return statement
        # No closing marker!  Restore and do nothing
        blocks[0] = original_block
        return False  # equivalent to our test() routine returning False


class BoxExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(DivStylesProcessor(md.parser), "box", 175)


with open("test.md", "r") as f:
    text = f.read()

    md = markdown.Markdown(extensions=[BoxExtension()])
    html = md.convert(text)

    with open("test.html", "w") as f:
        f.write(html)
