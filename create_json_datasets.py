import json
import os
import pandas as pd

DEFAULT_JSON_LINE = {
    "start": "2009-11-01 00:00:00",
    "target": [4.3, "NaN", 5.1, ...],
    # "cat": [0, 1],
    "dynamic_feat": [[1.1, 1.2, 0.5, ...]]
}

PREPROCESS_DATA_PATH = r'data\preprocessed_data'

for file in os.listdir(PREPROCESS_DATA_PATH):
    csv_path = os.path.join(PREPROCESS_DATA_PATH, file)

    df = pd.read_csv(csv_path)

    json_str = ''
    for idx, row in df.iterrows():
        if idx != 0:
            json_row = '{' + f'"start": {row["Date"]}, "target": {row.pop(0)}, "dynamic_feat": {df.iloc[idx-1].pop(0)}' + '}'
            json_str += json_row + '\n'

    # TODO: create jsonl files
    # https://jsonlines.org/
