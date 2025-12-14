from textnode import (TextType, TextNode)
from htmlnode import (LeafNode)

def text_node_to_html_node(text_node):     
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a valid type")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        parts = old_node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        
        parts_nodes = []
        for i in range(0, len(parts)):
            if i % 2 != 0:
                parts_nodes.append(TextNode(parts[i], text_type))
            else:
                parts_nodes.append(TextNode(parts[i], TextType.TEXT))

        new_nodes.extend(parts_nodes)
    return new_nodes

