import pandas as pd


def upload_data(arg):
    data = pd.read_csv(f'DataSets/№{arg}.csv')
    data = data.drop(data.loc[data['VHI'] == -1.00].index)
    return data


def merge_indexes(params, DataSet):
    DataSet['Year/Week'] = DataSet[DataSet.columns[:2]].apply( lambda x: '/'.join(x.dropna().astype(str)), axis=1)
    arg = [DataSet['Year/Week'], DataSet[['SMN', 'SMT', f'{params["NOAA"]}']]]
    return pd.concat(arg, axis=1)