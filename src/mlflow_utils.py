import json
import os
from dataclasses import asdict
from tempfile import NamedTemporaryFile

import mlflow

from config import config
from paths import (
    ARTIFACTS_STORAGE,
    BACKEND_DB,
    REWARD_DISTRIBUTIONS_DIR,
    THOMPSON_SAMPLING_DIR,
)


def set_up_mlflow():
    """
    We should explicitly control the location for both:
    1. backend database (mlflow.db) (metadata)
    2. artifact storage (mlruns/) (files)

    This function handles the setup for MLflow experiment tracking
    1. Set location for storage stuff
    2. Specify which experiment this run belongs to
    """
    experiment_name = f"Bayesian_{config.mode.value}"

    # 1. Set location backend db
    mlflow.set_tracking_uri(f"sqlite:///{BACKEND_DB}")

    # 2. Check if experiment is already created.
    # If its not, create it
    if mlflow.get_experiment_by_name(experiment_name) is None:
        mlflow.create_experiment(
            experiment_name, artifact_location=f"file://{ARTIFACTS_STORAGE}"
        )

    # 3. Specify which experiment this run belongs to
    mlflow.set_experiment(experiment_name)


def log_simulation_mlflow():

    # 1. Log RELEVANT hyperparameters
    mlflow.log_params(extract_mlflow_hyperparams(config))

    # 2. Log ALL hyperparameters as artifact
    log_config_artifact()

    # 3. Log artifacts
    log_mlflow_artifacts()


##########
# HELPERS
##########
def extract_mlflow_hyperparams(config):
    """
    Log only hyperparameters that may vary across runs
    """
    my_dict = {
        "network": config.network,
        "duration": config.duration,
        "n_veh": config.n_veh,
    }

    if config.mode.value == "montecarlo":
        my_dict["n_episodes_MC"] = config.n_episodes_MC
    elif config.mode.value == "thompson":
        my_dict["n_episodes_TS"] = config.n_episodes_TS

    return my_dict


def log_config_artifact():
    config_dict = asdict(config)
    config_dict["mode"] = config.mode.value
    with NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(config_dict, f, indent=4)

        temp_path = f.name

    mlflow.log_artifact(temp_path)

    os.remove(temp_path)


def log_mlflow_artifacts():
    if config.mode.value == "montecarlo":
        mlflow.log_artifact(REWARD_DISTRIBUTIONS_DIR)
    elif config.mode.value == "thompson":
        mlflow.log_artifact(THOMPSON_SAMPLING_DIR)
