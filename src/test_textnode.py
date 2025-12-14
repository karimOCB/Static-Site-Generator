import unittest

from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node with url", TextType.BOLD, "www.url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_same_different_url(self):
        node = TextNode("This is a text node with url", TextType.BOLD, "www.url")
        node2 = TextNode("This is a text node with url", TextType.BOLD, "www.differenturl")
        self.assertNotEqual(node, node2)
    
    def test_explicit_none_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_url(self):
        node = TextNode("", TextType.LINK, "www.differenturl")
        html_node = text_node_to_html_node(node)
        self.assertEqual(repr(html_node), "LeafNode(a, , {'href': 'www.differenturl'})")

    def test_img(self):
        node = TextNode("Alt Text", TextType.IMAGE, "www.imgurl")
        html_node = text_node_to_html_node(node)
        self.assertEqual(repr(html_node), "LeafNode(img, , {'src': 'www.imgurl', 'alt': 'Alt Text'})")

    def test_invalid_type_raises(self):
        node = TextNode("x", None)
        self.assertRaises(Exception, text_node_to_html_node, node)

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


if __name__ == "__main__":
    unittest.main()