import json
import os
import pandas as pd


# https://jsonlines.org/
DEFAULT_JSON_LINE = {
    "start": "2009-11-01 00:00:00",
    "target": [4.3, "NaN", 5.1, ...],
    # "cat": [0, 1],
    "dynamic_feat": [[1.1, 1.2, 0.5, ...]]
}

PREPROCESS_DATA_PATH = 'data/preprocessed_data'
JSON_DATA_PATH = 'data/json'
PREDICTION_LENGTH = 30
DISCARD_FIRST_ROWS = 30

for file in os.listdir(PREPROCESS_DATA_PATH):
    csv_path = os.path.join(PREPROCESS_DATA_PATH, file)

    df = pd.read_csv(csv_path)

    train_str = ''
    test_str = ''
    for idx, row in df.iterrows():
        if idx > DISCARD_FIRST_ROWS:
            # d = {
            #     "start": str(row["Date"]),
            #     "target": list(row)[1:],
            #     "dynamic_feat": list(df.iloc[idx-1])[1:]
            # }
            json_row = '{' + f'"start": "{str(row["Date"])}", "target": {list(row)[1:]}, "dynamic_feat": {list(df.iloc[idx-1])[1:]}' + '}'
            if idx < df.shape[0] - PREDICTION_LENGTH:
                train_str += json_row + '\n' 
                test_str += json_row + '\n' 
            else:
                test_str += json_row + '\n' 
        else:
            pass

# train_path = f'/train/train_{file.split(".")[0]}.json'
# test_path = f'/test/test_{file.split(".")[0]}.json'
        
train_path = '/train/train.json'
test_path = '/test/test.json'


with open(JSON_DATA_PATH + train_path, 'w') as f:
    f.write(train_str)


with open(JSON_DATA_PATH + test_path, 'w') as f:
    f.write(test_str)

# for line in train_str.split('\n'):
#     with open(JSON_DATA_PATH + train_path, 'wb') as f:
#         f.write(json.loads(line).encode("utf-8"))

# for line in test_str.split('\n'):
#     with open(JSON_DATA_PATH + test_path, 'wb') as f:
#         f.write(json.loads(line).encode("utf-8"))
