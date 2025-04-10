import sys
from pathlib import Path

def add_project_root_to_path() -> None:
    # Add the project root directory to Python path
    project_root = Path(__file__).parent.parent
    sys.path.append(str(project_root))