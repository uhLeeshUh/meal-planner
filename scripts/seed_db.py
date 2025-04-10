from utils import add_project_root_to_path

add_project_root_to_path()

from app.seeds import run_seeds

if __name__ == "__main__":
    run_seeds() 