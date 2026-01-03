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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(md_block):
    lines = md_block.split("\n")
    lines = [line.strip() for line in lines if line.strip() != ""]
    ol_pattern = re.compile(r'^\d+\.\s+(.+)$')
    if re.match(r'^#{1,6}\s+(.+)$', md_block):
        return BlockType.HEADING
    elif lines[0].strip() == "```" and lines[-1].strip() == "```":
        return BlockType.CODE
    elif re.match(r'^(>.*(\n|$))+$', md_block):
        return BlockType.QUOTE
    elif re.match(r'^(- .+(\n|$))+$', md_block):
        return BlockType.UNORDERED_LIST
    elif all(ol_pattern.match(line) for line in lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        html_nodes.append(html_node)
    return ParentNode("div", html_nodes)


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
            stripped_lines = [fmt_line.strip() for fmt_line in fmt_lines if fmt_line.strip() != ""]
            text = " ".join(stripped_lines)
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
                text = line.removeprefix(f"{i+1}. ")
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


