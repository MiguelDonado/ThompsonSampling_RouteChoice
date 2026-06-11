from pathlib import Path


def rm_files_dir(dir):
    for file in dir.iterdir():
        if file.is_file():
            file.unlink()


# def prepare_data(sampled_tt_routes):
#     sampled_tt_result = prepare_sampled_tt_routes()
#     return {"sampled_tt_result": sampled_tt_result}


# def accumulate_results(results, result):
#     mapping = {
#         "sampled_tt": ("sampled_tt_result", "extend"),
#     }
#     """
#     getattr: Returns the method dynamically

#     Example:
#     getattr([], "append") translates to list.append()

#     Example:
#     key = "Padre"
#     my_fun = "append"
#     data_dict = {"Padre": ["Miguel", "Donado"], "Madre": ["Mercedes", "Fernandez"]}
#     getattr(data_dict[key], my_fun)("Campos")

#     ### Output ###
#     # {'Padre': ['Miguel', 'Donado', 'Campos'], 'Madre': ['Mercedes', 'Fernandez']}
#     """

#     for key, (res_key, method) in mapping.items():
#         getattr(results[key], method)(result[res_key])

# def save_processed_data(results):
#     mapping = {
#         "sampled_tt":


#         "aggregated": STATISTICS_PARQUET,
#         "vehroute": VEHROUTE_PARQUET,
#         "trips_info": TRIPS_INFO_PARQUET,
#         "fcd": FCD_PARQUET,
#         "edgedata": EDGEDATA_PARQUET,
#         "actions": ACTIONS,
#         "rewards": REWARDS,
#         "BM_results": BM_RESULTS,
#     }

#     for key, path in mapping.items():
#         df = pd.DataFrame(results[key])
#         # Extra code to make fcd smaller
#         if key == "fcd":
#             categorical_cols = ["vehicle_id"]
#             for col in categorical_cols:
#                 df[col] = df[col].astype("category")
#             df.to_parquet(path, compression="zstd", compression_level=9)
#         else:
#             df.to_parquet(path, engine="pyarrow")

# def prepare_sampled_tt_routes(episode, sampled_tt_routes):
#     rows = []
#     for idx, sampled_tt_route in enumerate(sampled_tt_routes, 1):
#         rows.append({"episode": episode, "route": idx, "sampled_tt": sampled_tt_route})
#     return rows
