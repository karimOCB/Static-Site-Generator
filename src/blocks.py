import re
from enum import Enum
from utils import text_to_textnodes, text_node_to_html_node
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "text"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(md_block):
    heading_pattern = r'^#{1,6}\s+(.+)$'
    lines = md_block.split("\n")
    quote_pattern = r'^(>.*(\n|$))+$'
    ul_pattern = r'^(- .+(\n|$))+$'
    ol_pattern = r'^\d+\.\s+.+$'
    if re.match(heading_pattern, md_block):
        return BlockType.HEADING
    elif lines[0].strip() == "```" and lines[-1].strip() == "```":
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
        case BlockType.HEADING:
            i = 0
            while i < len(block) and block[i] == "#":
                i += 1
            text = block[i:].lstrip()
            text_nodes = text_to_textnodes(text)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return ParentNode(f"h{i}", html_nodes)
        case BlockType.CODE:
            lines = block.split("\n")
            inner_lines = lines[1:-1]
            text = "\n".join(inner_lines)
            text += "\n"
            text_node = TextNode(text, TextType.CODE)
            html_node = text_node_to_html_node(text_node)
            pre_node = ParentNode("pre", [html_node])
            return pre_node
        case BlockType.QUOTE:
            lines = block.split("\n")
            fmt_lines = [line.removeprefix("> ") for line in lines]
            text = "\n".join(fmt_lines)
            text_nodes = text_to_textnodes(text)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return ParentNode("blockquote", html_nodes)
        case BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                text = line.removeprefix("- ")
                text = text.strip(" ")
                text_nodes = text_to_textnodes(text)
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                li_nodes.append(ParentNode("li", html_nodes))
            return ParentNode("ul", li_nodes)
        case BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for i, line in enumerate(lines):
                text = line.removeprefix(f"{i}. ")
                text = text.strip(" ")
                text_nodes = text_to_textnodes(text)
                html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
                li_nodes.append(ParentNode("li", html_nodes))
            return ParentNode("ol", li_nodes)
        case BlockType.PARAGRAPH:
            lines = block.split("\n")
            lines_stripped = [line.strip(" ") for line in lines]
            text = (" ").join(lines_stripped)
            text_nodes = text_to_textnodes(text)
            html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
            return ParentNode("p", html_nodes)
        case _:
            raise Exception("Not a valid type")

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    if "" in blocks: blocks.remove("")
    return blocks