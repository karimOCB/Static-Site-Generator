import re

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
        
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

        
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

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links_tuples = extract_markdown_links(old_node.text); # ("to boot dev", "https://www.boot.dev")
        if not links_tuples:
            new_nodes.append(old_node)
        else:
            text_to_process = old_node.text
            for link_tuple in links_tuples:
                link_text, link_url = link_tuple
                f_md_link = f"[{link_text}]({link_url})"
                sections = text_to_process.split(f_md_link, 1)
                before = sections[0]
                after = sections[1] if len(sections) > 1 else ""
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                text_to_process = after
            if text_to_process != "":
                new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images_tuples = extract_markdown_images(old_node.text);
        if not images_tuples:
            new_nodes.append(old_node)
        else:
            text_to_process = old_node.text
            for image_tuple in images_tuples:
                alt_text, image_url = image_tuple
                f_md_image = f"![{alt_text}]({image_url})"
                sections = text_to_process.split(f_md_image, 1)
                before = sections[0]
                after = sections[1] if len(sections) > 1 else ""
                if before != "":
                    new_nodes.append(TextNode(before, TextType.TEXT))
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, image_url))
                text_to_process = after
            if text_to_process != "":
                new_nodes.append(TextNode(text_to_process, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)