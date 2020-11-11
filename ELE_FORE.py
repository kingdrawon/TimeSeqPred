#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Drawon
# Time:2020/11/6 16:01
# Version:python 3.7.6


import logging
import datetime
import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import Holt
import warnings
warnings.filterwarnings('ignore')

def valueForecast(file):
    """
    电费预测
    :param data: 电量数据
    格式为：用户 日期 使用电量值
    :return: 预测电量值
    """
    logging.debug('开始运行')
    data = pd.read_excel(file)
    if data.shape[0] == 0:
        raise ValueError('相关性原始数据不存在')
    data.iloc[:, 0] = data.iloc[:,0].astype(str)
    users = set(data.iloc[:,0].values)

    # 用电量预测
    result_pre = pd.DataFrame(columns=['DATA_DATE', 'DATA_DATE1', 'DATA_DATE2', 'DATA_DATE3', 'DATA_DATE4', 'DATA_DATE5'])
    for user in users:
        subdata = data.loc[data.iloc[:,0]==user]
        df_index = pd.MultiIndex.from_frame(subdata.iloc[:, 1:2])
        df = pd.DataFrame(np.array(subdata.iloc[:,-1]).reshape(1,-1),columns=df_index)
        df.dropna(axis=1,inplace=True)
        df_values = df.values.flatten()
        model = Holt(endog=df_values, initialization_method='estimated', ).fit()
        pre = model.forecast(steps=5)
        print(f'数据的预测 {pre}')
        res2 = pd.DataFrame(pre).T
        res2.columns = ['DATA_DATE1', 'DATA_DATE2', 'DATA_DATE3', 'DATA_DATE4', 'DATA_DATE5']
        res2['DATA_DATE'] = datetime.date.today()
        res2['USRE'] = user
        print(f'RES2 {res2}')
        result_pre = result_pre.append(res2, ignore_index=True)
    print(result_pre)
    return result_pre


