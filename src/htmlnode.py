class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children # children tags
        self.props = props # Dictionary of html att

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props: return "" 
        formatted_string_att = ""
        for key in self.props:
            formatted_string_att += f" {key}={self.props[key]}"
        return formatted_string_att
    
    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"