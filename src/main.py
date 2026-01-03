import os, shutil, sys
from generate_page import generate_pages_recursive

current_dir = os.path.dirname(__file__) #.../src
project_root = os.path.dirname(current_dir) # static_site_generator
docs_dir = os.path.join(project_root, 'docs')
static_dir = os.path.join(project_root, 'static')
base_path = sys.argv[1] if len(sys.argv) > 0 else "/"

def main():
    if not os.path.exists(static_dir):
        raise FileNotFoundError(f"Static directory not found: {static_dir}")

    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
   
    os.mkdir(docs_dir)

    check_files(static_dir, docs_dir)

    generate_pages_recursive(os.path.join(project_root, 'content'), os.path.join(project_root, 'template.html'), os.path.join(docs_dir), base_path)


def check_files(src, dest):
    for path in os.listdir(src):
        new_path = os.path.join(src, path)
        if os.path.isdir(new_path):
            new_dest = os.path.join(dest, path)
            os.mkdir(new_dest)
            print(f"{new_dest}") 
            check_files(new_path, new_dest)
        else:
           shutil.copy(new_path, dest)
           print(f"{new_path} into {dest}")

if __name__ == "__main__":
    main()