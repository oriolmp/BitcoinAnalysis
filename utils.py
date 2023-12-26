import pandas as pd
import numpy as np


def compute_variation(df: pd.DataFrame):
    """
    Given a df with columns 'Close' and 'Open', computes the price daily variation, absolute and percentual.
    """
    df['Variation'] = (df['Close'] - df['Open'])
    df['Percentual Variation'] = (df['Variation'] / df['Open']) * 100
    
    return df


def calculate_change(df: pd.DataFrame):
    """
    Given a df with column "variation", computes the change between prior and current price
    """
    change_lst = []
    change = 0
    for idx, row in df.iterrows():
        if idx == 0:
            pass
        else:
            change = df.iloc[idx]['Variation'] - df.iloc[idx-1]['Variation']
        change_lst.append(change)

    changes = pd.Series(change_lst, name='Variation')
    df = pd.concat([df, changes], axis=1)
    return df


def compute_rsi(df: pd.DataFrame, n: int=14):
    """
    Computes RSI
    """
    rsi_lst = []
    for idx, row in df.iterrows():
        if idx < n:
            m = idx
        else:
            m = n

        up = []
        down = []
        for i in range(idx - m, idx):
            if df.iloc[i]['Percentual Variation'] > 0:
                up.append(df.iloc[i]['Percentual Variation'])
            else:
                down.append(df.iloc[i]['Percentual Variation'])
        
        if up:
            up_mean = np.mean(up) / m
        else:
            up_mean = 0

        if down:
            down_mean = np.mean(down) / m
        else:
            down_mean = 1

        rs = np.abs(up_mean / down_mean)
        rsi = 100 - (100/(1 + rs))
            
        rsi_lst.append(rsi)
    
    rsi = pd.Series(rsi_lst, name='RSI')
    df = pd.concat([df, rsi], axis=1)    

    return df


def compute_sma(df: pd.DataFrame, n: int=12):
    """
    Computes simple moving average
    """
    sma_lst = []
    for idx, row in df.iterrows():
        if idx < n:
            sma = df[0:idx]['Close'].mean()
        else:
            sma = df[idx-n:idx]['Close'].mean()
        sma_lst.append(sma)
    
    sma_column = f'SMA_{n}'
    sma = pd.Series(sma_lst, name=sma_column)
    df = pd.concat([df, sma], axis=1)

    return df

def compute_ema(df: pd.DataFrame, n: int=14):
    """
    Computes exponential moving average
    """

    sma = df.iloc[:n]['Close'].mean()
    w = 2 / (n + 1)
    ema_lst = []

    for idx, row in df.iterrows():
        if idx < n:
            ema = sma
        else:
            ema = (row['Close'] - ema_lst[idx-1]) * w + ema_lst[idx-1]
        ema_lst.append(ema)
    
    ema_column = f'EMA_{n}'
    ema = pd.Series(ema_lst, name=ema_column)
    df = pd.concat([df, ema], axis=1)

    return df


def compute_macd(df: pd.DataFrame):
    """
    Computes MACD.
    Computes ema of 12 and 26 and add them inside df
    https://www.investopedia.com/ask/answers/122414/what-moving-average-convergence-divergence-macd-formula-and-how-it-calculated.asp
    """

    df = compute_ema(df, n=12)
    df = compute_ema(df, n=26)
    
    macd_lst = []

    for idx, row in df.iterrows():
        macd = row['EMA_26'] - row['EMA_12']
        macd_lst.append(macd)

    macd = pd.Series(macd_lst, name='MACD')
    df = pd.concat([df, macd], axis=1)

    return df


def compute_signal(df: pd.DataFrame, n: int=9):
    """
    Computes signal line from MACD method
    """

    sma = df.iloc[:n]['MACD'].mean()
    w = 2 / (n + 1)
    ema_lst = []

    for idx, row in df.iterrows():
        if idx < n:
            ema = sma
        else:
            ema = (row['MACD'] - ema_lst[idx-1]) * w + ema_lst[idx-1]
        ema_lst.append(ema)

    ema = pd.Series(ema_lst, name='Signal_MACD')
    df = pd.concat([df, ema], axis=1)

    return df


def compute_stochastic_oscillator(df: pd.DataFrame, n: int=14):
    """
    Computes Stochastic Oscillator
    """

    stochastic_lst = []

    for idx, row in df.iterrows():
        if idx < n:
            lowest = df.iloc[0:idx]['Low'].min()
            highest = df.iloc[0:idx]['High'].max()
        else:
            lowest = df.iloc[idx-n:idx]['Low'].min()
            highest = df.iloc[idx-n:idx]['High'].max()
        current = row['Close']

        stochastic = (current - lowest) / (highest - lowest)
        stochastic_lst.append(stochastic)

    stochastic = pd.Series(stochastic_lst, name='Stochastic_oscillator')
    df = pd.concat([df, stochastic], axis=1)

    return df

def compute_atr(df: pd.DataFrame, n: int=14):
    """
    Computes average true range
    """

    atr_lst = []

    for idx, row in df.iterrows():
        if idx < n:
            sum = 0
            for i in range(idx):
                sum += df.iloc[i]['High'] - df.iloc[i]['Low']
            atr = (1 / n) * sum
        else:
            atr = (atr_lst[idx-1] + (row['High'] - row['Low'])) / n
        atr_lst.append(atr)

    atr = pd.Series(atr_lst, name='ATR')
    df = pd.concat([df, atr], axis=1)

    return df


def compute_obv(df: pd.DataFrame):
    """
    Computes On-Balance Volume
    """

    obv_lst = []

    for idx, row in df.iterrows():
        if idx == 0:
            obv = row['Volume']
        else:
            previous_close = df.iloc[idx-1]['Close']
            current_close = row['Close']

            if current_close > previous_close:
                obv = obv_lst[idx-1] + row['Volume']
            elif current_close < previous_close:
                obv = obv_lst[idx-1] - row['Volume']
            else:
                obv = obv_lst[idx-1]
        obv_lst.append(obv)

    obv = pd.Series(obv_lst, name='OBV')
    df = pd.concat([df, obv], axis=1)

    return df


def compute_chaikin(df:pd.DataFrame, n: int=21):
    """
    Computes Chaikin Money Flow. Also it computes and adds Money Flow volume
    """

    money_flow_lst = []
    chaikin_lst = []

    for idx, row in df.iterrows():
        m = ((row['Close'] - row['Low']) - (row['High'] - row['Close'])) / (row['High'] - row['Low'])
        money_flow = m * row['Volume']
        money_flow_lst.append(money_flow)

        if idx < n:
            chaikin = np.mean(money_flow_lst[:n]) - df.iloc[:n]['Volume'].mean()
        else:
            chaikin = np.mean(money_flow_lst[idx-n:idx]) - df.iloc[idx-n:idx]['Volume'].mean()
        chaikin_lst.append(chaikin)
    
    money_flow = pd.Series(money_flow_lst, name='Money_flow')
    chaikin = pd.Series(chaikin_lst, name='Chaikin')
    df = pd.concat([df, money_flow, chaikin], axis=1)

    return df


def set_target(df: pd.DataFrame):
    """
    Creates target column.
    It is the next daily close price
    """

    target_lst = []
    for idx, row in df.iterrows():
        if idx+1 == df.shape[0]:
            target = row.pop(0)
        else:
            target = df.iloc[idx+1]['Close'].pop(1)
        target_lst.append(target)
    
    targets = pd.Series(target_lst)
    df = pd.concat([df, targets], axis=1)

    return df