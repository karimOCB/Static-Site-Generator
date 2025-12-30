import re
from enum import Enum
from utils import text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "text"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(md_block):
    heading_pattern = r'^#{1,6}\s+(.+)$'
    code_pattern = r'^```[\s\S]*?^```$'
    quote_pattern = r'^(>.*(\n|$))+$'
    ul_pattern = r'^(- .+(\n|$))+$'
    ol_pattern = r'^\d+\.\s+.+$'
    if re.match(heading_pattern, md_block):
        return BlockType.HEADING
    elif re.match(code_pattern, md_block):
        return BlockType.CODE
    elif re.match(quote_pattern, md_block):
        return BlockType.QUOTE
    elif re.match(ul_pattern, md_block):
        return BlockType.UNORDERED_LIST
    elif re.match(ol_pattern, md_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def block_to_html_node(block, block_type):
    match block_type:
        case BlockType.HEADING
            i = 0
            while i < len(block) and block[i] == "#":
                i += 1
            text = block[i:].lstrip()
            text_nodes = text_to_textnodes(text)
            html_nodes = [text_node_to_html_node(node) for text_node in text_nodes]
            return HTMLNode(f"h{i}", text, html_nodes)
        case BlockType.CODE
            return HTMLNode("", text_node.text)
        case BlockType.QUOTE
            return LeafNode("i", text_node.text)
        case BlockType.UNORDERED_LIST
            return LeafNode("code", text_node.text)
        case BlockType.ORDERED_LIST
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.PARAGRAPH
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a valid type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    if "" in blocks: blocks.remove("")
    return blocks