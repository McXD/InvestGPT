import numpy as np
import pandas as pd
import yfinance as yf

import warnings

warnings.filterwarnings("ignore")


def trade(code):
    df = yf.download(tickers=code,
                     start='2016-04-01',
                     end='2021-04-02',
                     progress=False)
    df = df[['Close']]
    df = df.sort_values(by='Date')
    df.reset_index(drop=False, inplace=True)
    return df


def performance(df):
    dai_ret = df['total_capital'][len(df) - 1] / df['total_capital'][0]
    ann_ret = pow(dai_ret, 250 / len(df)) - 1
    df['return'] = df['total_capital'].pct_change()
    ann_vol = df['return'].std() * np.sqrt(250)
    sr = ann_ret / ann_vol
    return sr, ann_ret


def performance1(df):
    dai_ret = df['Close'][len(df) - 1] / df['Close'][0]
    ann_ret = pow(dai_ret, 250 / len(df)) - 1
    df['return'] = df['Close'].pct_change()
    ann_vol = df['return'].std() * np.sqrt(250)
    sr = ann_ret / ann_vol
    return sr, ann_ret


def MA(df, var):
    df['MA' + str(var)] = df['Close'].rolling(window=var).mean()
    return df


def REF(df, X, N):
    df['REF' + str(N)] = df[X].shift(N)
    return df


def DPO(df, N):
    df = MA(df, N)
    df = REF(df, str('MA' + str(N)), int(N / 2 + 1))
    df['DPO' + str(N)] = df['Close'] - df['REF' + str(int(N / 2 + 1))]
    return df


def EMA(df, N):
    df['EMA' + str(N)] = pd.DataFrame.ewm(df['Close'], span=N).mean()
    return df


def PO(df):
    df = EMA(df, 9)
    df = EMA(df, 26)
    df['PO'] = df['EMA9'] - df['EMA26']
    return df


def DEMA(df, N):
    df = EMA(df, N)
    df['EEMA' + str(N)] = pd.DataFrame.ewm(df['EMA' + str(N)], span=N).mean()
    df['DEMA' + str(N)] = df['EMA' + str(N)] * 2 - df['EEMA' + str(N)]
    return df


def MACD(df):
    df = EMA(df, 20)
    df = EMA(df, 40)
    df['MACD'] = df['EMA20'] - df['EMA40']
    df['MACD_SIGNAL'] = pd.DataFrame.ewm(df['MACD'], span=5).mean()
    df['MACD_HISTOGRAM'] = df['MACD'] - df['MACD_SIGNAL']
    return df


def TSI(df):
    df = REF(df, 'Close', 1)
    df['T'] = df['Close'] - df['REF1']
    df['S'] = df['T'].abs()
    df['TSI1'] = pd.DataFrame.ewm(df['T'], span=25).mean()
    df['TSI2'] = pd.DataFrame.ewm(df['TSI1'], span=13).mean()
    df['TSI3'] = pd.DataFrame.ewm(df['S'], span=25).mean()
    df['TSI4'] = pd.DataFrame.ewm(df['TSI3'], span=13).mean()
    df['TSI'] = df['TSI2'] / df['TSI4'] * 100
    return df


def profit(df):
    df['strat'] = 0
    for i in range(len(df)):
        if (df['DPO20'].iloc[i] > 0):
            df.loc[i, 'strat'] = df.loc[i, 'strat'] + 1
        if (df['TSI'].iloc[i] > 10):
            df.loc[i, 'strat'] = df.loc[i, 'strat'] + 1
        if (df['PO'].iloc[i] > 0):
            df.loc[i, 'strat'] = df.loc[i, 'strat'] + 1
        if (df['DEMA5'].iloc[i] > df['DEMA10'].iloc[i]):
            df.loc[i, 'strat'] = df.loc[i, 'strat'] + 1
        if (df['MACD_HISTOGRAM'].iloc[i] > 0):
            df.loc[i, 'strat'] = df.loc[i, 'strat'] + 1
    return df


def MA_strategy(df):
    df['cash'] = 0
    df['shares'] = 0
    df['outstanding'] = 0
    df['total_capital'] = 0
    df['cash'].iloc[0] = 1000000
    df['total_capital'].iloc[0] = 1000000
    for i in range(1, len(df)):
        df['total_capital'].iloc[i] = df['cash'].iloc[i - 1] + df['shares'].iloc[i - 1] * df['Close'].iloc[i]
        df['outstanding'].iloc[i] = df['total_capital'].iloc[i] * df['strat'].iloc[i] / 5
        df['cash'].iloc[i] = df['total_capital'].iloc[i] - df['outstanding'].iloc[i]
        df['shares'].iloc[i] = df['outstanding'].iloc[i] / df['Close'].iloc[i]
    return df


def srrisk(code):
    df = trade(code)
    df = DPO(df, 20)
    df = PO(df)
    df = DEMA(df, 5)
    df = DEMA(df, 10)
    df = MACD(df)
    df = TSI(df)
    df = profit(df)
    df = MA_strategy(df)
    sr, ann_ret = performance(df)
    if sr < 0:
        sr, ann_ret = 'NA'
    risk = [code, sr, ann_ret]
    return risk


symbol_list = ['EQIX', 'SBAC', 'GLPI', 'HST', 'REG', 'LAMR', 'AGNCN', 'AGNCM', 'AGNC', 'PCH', 'SBRA', 'SVC', 'ROIC',
               'NYMTN', 'UNIT', 'RTL', 'NYMT', 'OPI', 'INDT', 'LAND', 'GOOD', 'LANDM', 'DHC', 'AFCG', 'ILPT',
               'SEVN', 'SOHOO', 'SOHOB', 'SOHON', 'CMCT', 'SOHO', 'LOAN', 'SELF', 'MDRR', 'WHLR', 'SQFT', 'WHLRD',
               'WHLRP', 'LANDO', 'RTLPO', 'RTLPP', 'AGNCO', 'HTIA', 'NYMTM', 'GOODN', 'AGNCP', 'PLD', 'PSA', 'EXR',
               'LSI', 'REXR', 'CUBE', 'COLD', 'EGP', 'FR', 'STAG', 'NSA', 'IIPR', 'PLYM', 'TRNO', 'LXP', 'WELL', 'VTR']
A = []
for i in symbol_list:
    A.append(srrisk(i))

df = pd.DataFrame(A, columns=['Company', 'SR', 'return'])
df = df[df['SR'] != 'N']
df.reset_index()
df.to_csv('data.csv')
