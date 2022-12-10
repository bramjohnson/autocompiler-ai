import yaml, os
from pathlib import Path

def edit_config(key, value):
    OPTIONS_DICT[key] = value
    with open('config.yaml', 'w') as outfile:
        yaml.dump(OPTIONS_DICT, outfile, default_flow_style=False)
    # print(OPTIONS_DICT)

OPTIONS_DICT = {
    "import_m3u8_path": str(Path.home() / "Music"),
    "export_m3u8_path": str(Path.home() / "Music"),
    "save_session_path": "./backup/",
    "open_session_path": "./backup/",
    "auto_load_songs_on_open": False,
    "use_negative_weights": False,
    "random_noise": 0.07,
    "playlist_lookback": 10,
    "amount_similar_tracks": 10
}
if (not os.path.exists('config.yaml')):
    for key, value in OPTIONS_DICT.items():
        edit_config(key, value)

with open('config.yaml') as file:
    for key, value in yaml.load(file, Loader=yaml.Loader).items():
        OPTIONS_DICT[key] = value