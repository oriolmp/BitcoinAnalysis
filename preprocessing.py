import os
import pandas as pd

from utils import *

DATA_PATH = r'data\raw_data'
PREPROCESS_DATA_PATH = r'data\preprocessed_data'
INDICATORS = [
    compute_variation,
    compute_rsi,
    compute_stochastic_oscillator,
    compute_obv,
    compute_atr,
    compute_ema,
    compute_macd,
    compute_signal,
    compute_chaikin
]

for file in os.listdir(DATA_PATH):
    csv_path = os.path.join(DATA_PATH, file)
    preprocessed_csv_path = os.path.join(PREPROCESS_DATA_PATH, file)

    print(f'Processing {file}')

    if not os.path.exists(PREPROCESS_DATA_PATH):
        os.makedirs(PREPROCESS_DATA_PATH)

    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%M-%d')

    for indicator in INDICATORS:
        df = indicator(df)
    df = df.drop('Adj Close', axis=1)    
    df.to_csv(preprocessed_csv_path, index=False)