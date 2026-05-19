from pathlib import Path

# Root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folders
SUMO_DIR = BASE_DIR / "sumo"
DATA_DIR = BASE_DIR / "data"

# Files
SUMO_CONF = SUMO_DIR / "config" / "basic.cfg"
TRIPS_INFO = DATA_DIR / "raw" / "trips_info.xml"
ROUTES = SUMO_DIR / "routes" / "routes.rou.xml"
UNDESIRED_FILE = BASE_DIR / "routes.rou.xml"
