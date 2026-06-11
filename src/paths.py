from pathlib import Path

# Root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Folders
SUMO_DIR = BASE_DIR / "sumo"
DATA_DIR = BASE_DIR / "data"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
THOMPSON_SAMPLING_DIR = BASE_DIR / "figures" / "ThompsonSampling"
MONTECARLO_DIR = BASE_DIR / "figures" / "MonteCarlo"
POST_AVG_TT_DIR = THOMPSON_SAMPLING_DIR / "posterior_avg_tt"
CONVERGENCE_POST_MEANS = (
    THOMPSON_SAMPLING_DIR / "convergence_post_mean" / "convergence_post_mean.png"
)
TRAVEL_TIMES_MONTECARLO = PROCESSED_DATA_DIR / "MonteCarlo"

# Output files Thompson
SAMPLED_MEAN_TT_PARQUET = PROCESSED_DATA_DIR / "sampled_mean_tt.parquet"
POSTERIOR_STATE_PARQUET = PROCESSED_DATA_DIR / "posterior_state.parquet"
REGRET_PARQUET = PROCESSED_DATA_DIR / "regret.parquet"

# Files
SUMO_CONF = SUMO_DIR / "config" / "basic.cfg"
TRIPS_INFO = DATA_DIR / "raw" / "trips_info.xml"
ROUTES = SUMO_DIR / "routes" / "routes.rou.xml"
UNDESIRED_FILE = BASE_DIR / "routes.rou.xml"
METRICS_LINKS = DATA_DIR / "processed" / "metrics_links.parquet"
METRICS_ROUTES = DATA_DIR / "processed" / "metrics_routes.parquet"

# ============================================================
# MLFlow database
# ============================================================
BACKEND_DB = BASE_DIR / "mlflow_db" / "mlflow.db"
ARTIFACTS_STORAGE = BASE_DIR / "mlruns" / "mlruns"
