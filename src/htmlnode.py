class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children # children tags
        self.props = props # Dictionary of html att

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props: return "" 
        formatted_string_att = ""
        for key in self.props:
            formatted_string_att += f' {key}="{self.props[key]}"'
        return formatted_string_att
    
    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
       super().__init__(tag, value, None, props) 

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag: return self.value
        formatted_att = super().props_to_html()
        result = f"<{self.tag}{formatted_att}>{self.value}</{self.tag}>"
        return result
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"