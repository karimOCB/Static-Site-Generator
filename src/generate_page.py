import os
from blocks import markdown_to_html_node

def extract_title(md):
    i = 0
    md = md.lstrip()
    lines = md.split("\n")
    title = lines[0]
    while i < len(title) and title[i] == "#":
        i += 1
    
    if i == 0  or i > 1:
        raise Exception("There is no h1 header")

    return title[i:].lstrip() 

def generate_pages_recursive(from_path, template_path, dest_path, base_path):
    print(f"Generating pages from {from_path} to {dest_path} using {template_path}")
    for path in os.listdir(from_path):
        new_from_path = os.path.join(from_path, path)
        new_dest_path = os.path.join(dest_path, path)
        root, extension = os.path.splitext(path)
        if os.path.isdir(new_from_path):
            print(f"Generating folder from {new_from_path} from {from_path} to {dest_path}")
            if not os.path.exists(new_dest_path):
                os.mkdir(new_dest_path)
            generate_pages_recursive(new_from_path, template_path, new_dest_path, base_path)
        elif os.path.isfile(new_from_path) and  extension == ".md":
            print(f"Generating file from {new_from_path} to {new_dest_path} using {template_path}")
            new_dest_file = os.path.join(dest_path, (root + ".html"))
            generate_page(os.path.join(new_from_path), template_path, new_dest_file, base_path)
        
def generate_page(from_path, template_path, dest_path, base_path):
    with open(from_path, 'r') as f:
        md = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    html_node = markdown_to_html_node(md)
    html_string = html_node.to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{base_path}')
    template = template.replace('src="/', f'src="{base_path}')

    with open(dest_path, 'w') as f:
        f.write(template)