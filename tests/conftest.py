import sys
from pathlib import Path

# Add the repository root to sys.path so pytest can import src modules.
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))
