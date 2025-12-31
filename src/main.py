import os, shutil

def main():
    copy_static_to_public()

def copy_static_to_public():
    current_dir = os.path.dirname(__file__) #.../src
    project_root = os.path.dirname(current_dir) # static_site_generator
    public_dir = os.path.join(project_root, 'public')
    static_dir = os.path.join(project_root, 'static')

    if not os.path.exists(static_dir):
        raise FileNotFoundError(f"Static directory not found: {static_dir}")

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
   
    os.mkdir(public_dir)

    check_files(static_dir, public_dir)

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