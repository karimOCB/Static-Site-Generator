import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter, split_nodes_link, split_nodes_image, text_to_textnodes
from blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMd(unittest.TestCase):
    def test_delimiter_one_node(self):
        node = TextNode("Hello **world**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Hello ", TextType.TEXT), TextNode("world", TextType.BOLD), TextNode(".", TextType.TEXT)])
    
    def test_delimiter_more_nodes(self):
        node = TextNode("Hello **world**.", TextType.TEXT)
        node2 = TextNode("Good **bye**.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Hello ", TextType.TEXT), TextNode("world", TextType.BOLD), TextNode(".", TextType.TEXT), TextNode("Good ", TextType.TEXT), TextNode("bye", TextType.BOLD), TextNode(".", TextType.TEXT)])

    def test_delimiter_more_nodes_no_txt(self):
        node = TextNode("Hello **world**.", TextType.TEXT)
        node2 = TextNode("www.url.com", TextType.LINK)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("Hello ", TextType.TEXT), TextNode("world", TextType.BOLD), TextNode(".", TextType.TEXT), TextNode("www.url.com", TextType.LINK)])
            
    def test_delimiter_invalid_syntax(self):
        node = TextNode("Hello **world.", TextType.TEXT)     
        self.assertRaises(Exception, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_delimiter_good_and_invalid_syntax(self):
        node = TextNode("Hello **world**.", TextType.TEXT)     
        node2 = TextNode("Good **bye.", TextType.TEXT)     
        self.assertRaises(Exception, split_nodes_delimiter, [node, node2], "**", TextType.BOLD)

    def test_link_delimiter(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)     
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("This is text with a link ", TextType.TEXT),TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),])
  
    def test_links_delimiter(self):
            node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)     
            node2 = TextNode("This is text with a link [to youtube](https://www.youtube.com)", TextType.TEXT)     
            new_nodes = split_nodes_link([node, node2])
            self.assertListEqual(new_nodes, [TextNode("This is text with a link ", TextType.TEXT),TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),TextNode(" and ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"), TextNode("This is text with a link ", TextType.TEXT),TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),])

    def test_img_delimiter(self):
        node = TextNode("This is some text with an ![first image](https://example.com/first.png) and another ![second image](https://example.com/second.png) in it.", TextType.TEXT)     
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("This is some text with an ", TextType.TEXT),TextNode("first image", TextType.IMAGE, "https://example.com/first.png"),TextNode(" and another ", TextType.TEXT),TextNode("second image", TextType.IMAGE, "https://example.com/second.png"),TextNode(" in it.", TextType.TEXT),])

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes, [
                                        TextNode("This is ", TextType.TEXT),
                                        TextNode("text", TextType.BOLD),
                                        TextNode(" with an ", TextType.TEXT),
                                        TextNode("italic", TextType.ITALIC),
                                        TextNode(" word and a ", TextType.TEXT),
                                        TextNode("code block", TextType.CODE),
                                        TextNode(" and an ", TextType.TEXT),
                                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                                        TextNode(" and a ", TextType.TEXT),
                                        TextNode("link", TextType.LINK, "https://boot.dev"),
                                    ])
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_p_block_to_block(self):
        md_block = "This is a simple paragraph"
        md_block_type = block_to_block_type(md_block)
        self.assertEqual(md_block_type, BlockType.PARAGRAPH)

    def test_heading_block_to_block(self):
        md_block = "### This is a simple heading"
        md_block_type = block_to_block_type(md_block)
        self.assertEqual(md_block_type, BlockType.HEADING)

    def test_md_to_html_node(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_and_inline(self):
        md = """
# Heading **one**
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading <b>one</b></h1></div>",
        )

    def test_a_lot_of_blocks(self):
        md = """
# Heading **one**

This is **bolded** paragraph
text in a p
tag here

> This is a **quote**
> over _two_ lines

- first **item**
- second _item_
- third `code`

1. first **item**
2. second _item_
3. third `code`
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading <b>one</b></h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><blockquote>This is a <b>quote</b> over <i>two</i> lines</blockquote><ul><li>first <b>item</b></li><li>second <i>item</i></li><li>third <code>code</code></li></ul><ol><li>first <b>item</b></li><li>second <i>item</i></li><li>third <code>code</code></li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()


