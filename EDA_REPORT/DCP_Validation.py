# 저작권       닉컴퍼니
# title     데이터 검증 : 각 필드항목에 대한 이상치 확인
# filename  DCP_Validation.py
# author    최승언
# version   0.12
# note      1. dcp_outliers
#			 - 목적 : 필드항목의 이상치 확인
#			 - 기능 : 범주형은 명세서에 없는 데이터를 이상치는 IQR을 이용하여 이상치를 확인하고 keys: 필드명, values: index로 하여 json 형식으로 return
#			 - 사용 라이브러리 : pandas
#			 - input : 데이터(dataframe), 금융데이터 명세서
#			 - output : 필드항목별 이상치 index(json)
#=========================================================
# V0.11
# 2022.01.18
# 1. 명세서 불러오는 코드 추가
# 2. categorical stat 부분 수정
# 3. discrete 알고리즘 표준편차 방법에서 IQR로 수정(threshold 사용여부)
#=========================================================
# V0.12
# 2022.02.15
# 1. dcp_outliers에 범주형, 수치형 이상치 탐지 알고리즘 통합
#=========================================================
# V0.13
# 2022.02.24
# 1. dcp_outliers에 수치형 이상치 탐지 방법 수정
#=========================================================
# V0.14
# 2022.03.11
# 1. dcp_outliers : DB설계 수정에 의한 수정
#=========================================================
import pandas as pd
import scipy.stats as ss
import numpy as np
import os
import datetime

#### v0.1 버젼
"""
def categorical(df, stat):
    stat = {i:stat.at[i,'uni'].split(',') for i in stat.index}
    outliers = {i:[len(df[~df[i].isin(list(map(str,stat[i])))].index)] for i in stat.keys()}
    return outliers

def discrete(df, threshold):
    outliers = dict()
    for cal in df.columns:
        if df[cal].dtype == ('int64' or 'float64'):            
            median = np.median(df[cal])
            mad = np.median(df[cal].map(lambda x: np.abs(x - median)))
            modified_z_score = pd.DataFrame(list(df[cal].map(lambda x: 0.6745*(x-median)/mad)))
            outliers[cal] = [len(df[abs(modified_z_score[0]) > abs(threshold)].index)]
    return outliers
"""


    

#### v0.11 버젼
"""
# DB로 부터 금융데이터 명세서 Load 
def dcp_loadstat(dbid, passwd, database, host, port, table):
    # 현재 임시로 만들어놓은 명세서를 사용하여 테스트
    db = pymysql.connect(
        user=dbid,
        passwd=passwd,
        database=database,
        host=host,
        port=port)                                              
    cursor = db.cursor(pymysql.cursors.DictCursor)              
    cursor.execute("SELECT * FROM {};".format(table+'_stat'))   
    stat = pd.DataFrame(cursor.fetchall()) 
    return stat



# 범주형 필드항목 이상치 개수 반환
def dcp_categorical(df, stat):
    # 금융데이터 명세서의 고유값 가져오기
    
    
    outliers = dict()
    cat_name = stat[stat['types']=='cat']['name'].unique().tolist()
    for cat in cat_name:
        unique = stat[stat['name']==cat]['class'].unique().tolist()
        outliers[cat] = df[~df[cat].isin(unique)].index.tolist()
        
        
    ########### v0.11 #######################################    
    #stat = {n:list(filter(None, stat[col].iloc[i].tolist())) for i,n in enumerate(stat['필드명'])}
    # 필드항목별 이상치 개수
    #outliers = {i:df[~df[i].isin(list(map(str,stat[i])))].index.tolist() for i in stat.keys()}
    #########################################################    
    
    
    return outliers



# 연속형 필드항목 이상치 개수 반환
def dcp_numerical(df, stat):
    stat = stat[stat['타입'].isin(['int','float'])]
    
    # IQR 방법으로 이상치 탐지 사용
    def iqr_outlier(df=None, column=None):
        quantile_25 = np.percentile(df[column].values, 25)
        quantile_75 = np.percentile(df[column].values, 75)

        IQR = quantile_75 - quantile_25
        IQR_weight = IQR*1.5

        lowest = quantile_25 - IQR_weight
        highest = quantile_75 + IQR_weight

        outlier_len = df[column][ (df[column] < lowest) | (df[column] > highest) ].index.tolist()
        return outlier_len
        
    outliers = {i:iqr_outlier(df,i) for i in stat['필드명']}
    return outliers
""" 
#### v0.12 버젼   
"""
def dcp_outliers(df, stat):

    outliers = dict()
    
    def iqr_outlier(df=None, column=None):
        quantile_25 = np.percentile(df[column].values, 25)
        quantile_75 = np.percentile(df[column].values, 75)

        IQR = quantile_75 - quantile_25
        IQR_weight = IQR*1.5

        lowest = quantile_25 - IQR_weight
        highest = quantile_75 + IQR_weight

        outlier_len = df[column][ (df[column] < lowest) | (df[column] > highest) ].index.tolist()
        return outlier_len
    for col in df.columns:
    
        types = stat[stat['name']==col]['types'].iloc[0]
    
        if types in ['uni', 'dtime']:
            outliers[col] = list()
            
            
        elif types == 'cat':
            df[col] = df[col].astype(str)
            unique = stat[stat['name']==col]['class_field'].unique().tolist()
            outliers[col] = df[~df[col].isin(unique)].index.tolist()  
        elif types == 'num':
            outliers[col] = iqr_outlier(df, col)
        else:
            raise('명세서 오류')
    return outliers
"""
"""
#### v0.13 버젼
def dcp_outliers(df, stat):
    outliers = dict()
    for col in df.columns:
        types = stat[stat['name']==col]['types'].iloc[0]
        if types in ['uni', 'dtime']:
            outliers[col] = list()
        elif types == 'cat':
            df[col] = df[col].astype(str)
            unique = stat[stat['name']==col]['class_field'].unique().tolist()
            outliers[col] = df[~df[col].isin(unique)].index.tolist()  
        elif types == 'num':
            pass
        else:
            raise('명세서 오류')
    return outliers
"""    

#### v0.14 버젼
def dcp_outliers(df, stat, code):
    outliers = dict()
    for col in df.columns:
        types = stat[stat['col_name']==col]['col_types'].iloc[0]
        if (col == 'ci_num') or ('org_code' in col) or (types != 'VARCHAR'):
            outliers[col] = list()
        else:
            df_col = df[col].astype(str).copy()
            code_value = str(stat[stat['col_name']==col]['code'].iloc[0])
            code_values = list(map(str, code[code['code']==code_value]['code_values']))
            outliers[col] = df[~df_col.isin(code_values)].index.tolist()
    return outliers