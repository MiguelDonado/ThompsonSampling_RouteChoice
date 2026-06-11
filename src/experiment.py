from pathlib import Path

import pandas as pd

from config import config
from paths import POSTERIOR_STATE_PARQUET, SAMPLED_MEAN_TT_PARQUET


def rm_files_dir(dir):
    for file in dir.iterdir():
        if file.is_file():
            file.unlink()


def prepare_data(episode, sampled_mean_tt_routes, routes):
    sampled_mean_tt_result = prepare_sampled_mean_tt_routes(
        episode, sampled_mean_tt_routes
    )
    posterior_state_result = prepare_posterior_state(episode, routes)
    return {
        "sampled_tt_result": sampled_mean_tt_result,
        "posterior_state_result": posterior_state_result,
    }


def accumulate_results(results, result):
    mapping = {
        "sampled_tt": ("sampled_tt_result", "extend"),
        "posterior_state": ("posterior_state_result", "extend"),
    }

    """
    getattr: Returns the method dynamically

    Example:
    getattr([], "append") translates to list.append()

    Example:
    key = "Padre"
    my_fun = "append"
    data_dict = {"Padre": ["Miguel", "Donado"], "Madre": ["Mercedes", "Fernandez"]}
    getattr(data_dict[key], my_fun)("Campos")

    ### Output ###
    # {'Padre': ['Miguel', 'Donado', 'Campos'], 'Madre': ['Mercedes', 'Fernandez']}
    """

    for key, (res_key, method) in mapping.items():
        getattr(results[key], method)(result[res_key])


def save_processed_data(results):
    mapping = {
        "sampled_tt": SAMPLED_MEAN_TT_PARQUET,
        "posterior_state": POSTERIOR_STATE_PARQUET,
    }

    for key, path in mapping.items():
        df = pd.DataFrame(results[key])
        df.to_parquet(path, engine="pyarrow")


def prepare_sampled_mean_tt_routes(episode, sampled_mean_tt_routes):
    rows = []
    for idx, sampled_mean_tt_route in enumerate(sampled_mean_tt_routes, 1):
        rows.append(
            {"episode": episode, "route": idx, "sampled_mean_tt": sampled_mean_tt_route}
        )
    return rows


def prepare_posterior_state(episode, routes):
    rows = []
    for idx, route in enumerate(routes):
        post_mean_beta = route.post_a / route.post_b
        post_var_beta = route.post_a / route.post_b**2
        # 1/X is non linear so we cannos apply linearity of expectations
        post_mean_tt = config.MoM_alpha[idx] * route.post_b / (route.post_a - 1)
        rows.append(
            {
                "episode": episode,
                "route": idx + 1,
                "post_hyper_a": route.post_a,
                "post_hyper_b": route.post_b,
                "post_mean_beta": post_mean_beta,
                "post_var_beta": post_var_beta,
                "post_mean_tt": post_mean_tt,
            }
        )
    return rows
