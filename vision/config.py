from pathlib import Path
import os
ROOT = Path(__file__).parents[1]

path_unlabled = os.path.join(ROOT, "images/unlabled")
path_labled = os.path.join(ROOT, "images/labled")
path_used = os.path.join(ROOT, "images/used")
path_skipped = os.path.join(ROOT, "images/skipped")