from pathlib import Path

# Root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folders
SUMO_DIR = BASE_DIR / "sumo"
DATA_DIR = BASE_DIR / "data"
REWARD_DISTRIBUTIONS_DIR = BASE_DIR / "figures" / "reward_distributions"
POST_AVG_TT_DIR = BASE_DIR / "figures" / "posterior_avg_tt"
TRAVEL_TIMES_MONTECARLO = DATA_DIR / "processed"

# Files
SUMO_CONF = SUMO_DIR / "config" / "basic.cfg"
TRIPS_INFO = DATA_DIR / "raw" / "trips_info.xml"
ROUTES = SUMO_DIR / "routes" / "routes.rou.xml"
UNDESIRED_FILE = BASE_DIR / "routes.rou.xml"
FREE_FLOW_TRAVEL_TIMES_LINKS = DATA_DIR / "processed" / "free_flow_tt_links.parquet"
FREE_FLOW_TRAVEL_TIMES_ROUTES = DATA_DIR / "processed" / "free_flow_tt_routes.parquet"
