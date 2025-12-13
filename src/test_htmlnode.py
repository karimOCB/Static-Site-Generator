import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is text", "span")
        node2 = HTMLNode("h1", "This is title")
        self.assertNotEqual(node, node2)

    def test_props_to_html_none():
        node = HTMLNode(tag="a", value="link", props=None)
        assert node.props_to_html() == ""

    def test_props_to_html_empty_dict():
        node = HTMLNode(tag="a", value="link", props={})
        assert node.props_to_html() == ""

    def test_props_to_html_multiple_props():
        node = HTMLNode(
            tag="a",
            value="link",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        result = node.props_to_html()
        assert ' href="https://www.google.com"' in result
        assert ' target="_blank"' in result

if __name__ == "__main__":
    unittest.main()