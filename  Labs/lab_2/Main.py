from spyre import server

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import Functions as Fn
from sklearn import preprocessing
server.include_df_index = True

class Second_Lab(server.App):
    title = "NOAA data visualization"

    inputs = [{    
        "type":'dropdown',
        "label": 'NOAA data visualization',
        "options" : [ 
            {"label": "VCI", "value":"VCI"},
            {"label": "TCI", "value":"TCI"},
            {"label": "VHI", "value":"VHI"}],
        "key": 'NOAA',
        "action_id": "update_data"},

        {"type":'dropdown',
        "label": 'Область',
        "options" : [ 
            {"label": "Вінницька", "value":"1"},
            {"label": "Волинська", "value":"2"},
            {"label": "Дніпропетровська", "value":"3"},
            {"label": "Донецька", "value":"4"},
            {"label": "Житомирська", "value":"5"},
            {"label": "Закарпатська", "value":"6"},
            {"label": "Запорізька", "value":"7"},
            {"label": "Івано-Франківська", "value":"8"},
            {"label": "Київська", "value":"9"},
            {"label": "Кіровоградська", "value":"10"},
            {"label": "Луганська", "value":"11"},
            {"label": "Львівська", "value":"12"},
            {"label": "Миколаївська", "value":"13"},
            {"label": "Одеська", "value":"14"},
            {"label": "Полтавська", "value":"15"},
            {"label": "Рівенська", "value":"16"},
            {"label": "Сумська", "value":"17"},
            {"label": "Тернопільська", "value":"18"},
            {"label": "Харківська", "value":"19"},
            {"label": "Херсонська", "value":"20"},
            {"label": "Хмельницька", "value":"21"},
            {"label": "Черкаська", "value":"22"},
            {"label": "Чернівецька", "value":"23"},
            {"label": "Чернігівська", "value":"24"},
            {"label": "Республіка Крим", "value":"25"},
            {"label": "м.Київ", "value":"26"},
            {"label": "Севастополь", "value":"27"}],
        "key": 'Region',
        "action_id": "update_data"},

        {"type": "text",
        "key": 'range_weeks',
        "label": "Range of weeks. (Min:1. Max:52)",
        "value": "1-52",
        "action_id": 'simple_html_output'},

        {"type": "text",
        "key": 'range_years',
        "label": "Range of years. (Min:1990. Max:2022)",
        "value": "1990-2022",
        "action_id": 'simple_html_output'},

        {"type":'dropdown',
        "label": 'Chart type',
        "options" : [ 
            {"label": "Lineplot", "value":"lineplot"},
            {"label": "Histplot", "value":"histplot"},
            {"label": "Heatmap", "value":"heatmap"},
            {"label": "Barplot", "value":"barplot"},
            {"label": "Scatterplot", "value":"scatterplot"}],
        "key": 'chart_type',
        "action_id": "update_data"}]

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Show result"
    }]

    tabs = ["Plot", "Table"]

    outputs = [{
            "type": "plot",
            "id": "__get_plot__",
            "control_id": "update_data",
            "tab": "Plot"},
            
            {"type": "table",
            "id": "__get_data__",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True}]

    def __get_html__(self, params):
        return params["range"]

    def __get_range__(self, rangeofdate):
        if len(rangeofdate.split('-')) == 1:
            return [int(rangeofdate) for _ in range(2)]
        else:
            return list(map(lambda x: int(x), rangeofdate.split('-')))

    def __get_data__(self, params):
        Data = Fn.upload_data(int(params['Region']))
        DataSet = Data.loc[Data['Year'].between(self.__get_range__(params['range_years'])[0], self.__get_range__(params['range_years'])[1]) &
         Data['Week'].between(self.__get_range__(params['range_weeks'])[0], self.__get_range__(params['range_weeks'])[1])]
        return DataSet[['Year', 'Week', 'SMN', 'SMT', f'{params["NOAA"]}']]
    
    def __get_plot__(self, params):
        Data = self.__get_data__(params)
        Data = Fn.merge_indexes(params, Data)
        Data.set_index('Year/Week', inplace=True)
        plt.figure(figsize=(15,9))
        match params['chart_type']:
            case 'lineplot':
                ax = sns.lineplot(data=Data[['SMN', 'SMT', f'{params["NOAA"]}']])
                plt.xticks(range(1, len(Data['SMN']), len(Data['SMN'])//13))
                return ax
            case 'histplot':
                ax = sns.histplot(data=Data[['SMN', 'SMT', f'{params["NOAA"]}']])
                return ax
            case 'scatterplot':
                ax = sns.scatterplot(data=Data[['SMN', 'SMT', f'{params["NOAA"]}']])
                plt.xticks(range(1, len(Data['SMN']), len(Data['SMN'])//13))
                return ax
            case 'heatmap':
                plt.figure(figsize=(20,40))
                data_normalized = Data.copy()
                scaler = preprocessing.MinMaxScaler()
                data_normalized = pd.DataFrame(scaler.fit_transform(Data), columns=Data.columns, index=Data.index)
                ax = sns.heatmap(data=data_normalized[['SMN', 'SMT', f'{params["NOAA"]}']][:50], annot=True)
                return ax
            case 'barplot':
                plt.figure(figsize=(13,9))
                ax = sns.barplot(x=Data.index, y=Data[f'{params["NOAA"]}'])
                plt.xticks(range(1, len(Data['SMN']), len(Data['SMN'])//13))
                return ax

app = Second_Lab()
app.launch(port=9093)