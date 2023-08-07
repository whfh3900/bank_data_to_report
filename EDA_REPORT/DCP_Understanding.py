# -*- coding: utf-8 -*-

# 저작권       닉컴퍼니
# title     데이터 이해 : 데이터에 대한 정보확인
# filename  DCP_Understanding.py
# author    최승언
# version   0.15
# note      1. dcp_shape
#			 - 목적 : 데이터 이해, 보고서 작성
#			 - 기능 : 데이터의 행,열 크기를 tuple 형식으로 return
#			 - 사용 라이브러리 : pandas의 shape 메소드
#			 - input : 데이터(dataframe)
#			 - output : 데이터의 크기(tuple)

#			2. dcp_types
#			 - 목적 : 데이터 이해, 보고서 작성
#			 - 기능 : 필드항목 별 데이터 타입을 keys: 필드명, values:타입 으로 하여 json 형식으로 return
#			 - 사용 라이브러리 : pandas의 dtypes 메소드
#			 - input : 금융데이터 명세서
#			 - output : 필드항목별 데이터 타입(json)

#			3. dcp_missing
#			 - 목적 : 데이터 이해, 보고서 작성, 학습 파이프라인 전처리 단계에서 결측값 처리에 사용
#			 - 기능 : 필드항목 별 결측값을 keys: 필드명, values: 결측치 index list 으로 하여 json 형식으로 return
#			 - 사용 라이브러리 : pandas의 isnull 메소드
#			 - input : 데이터(dataframe)
#			 - output : 필드항목별 결측값 index(json)

#			4. dcp_unique
#			 - 목적 : 데이터 이해, 보고서 작성, 데이터 검증에 사용
#			 - 기능 : 범주형 필드항목 별 고유값 개수 파악
#			 - 사용 라이브러리 : pandas의 unique 메소드
#			 - input : 데이터(dataframe)
#			 - output : 필드항목별 고유값 index(json)

#           5. dcp_outliers
#			 - 목적 : 필드항목의 이상치 확인
#			 - 기능 : 범주형은 명세서에 없는 데이터를 이상치는 IQR을 이용하여 이상치를 확인하고 keys: 필드명, values: index로 하여 json 형식으로 return
#			 - 사용 라이브러리 : pandas
#			 - input : 데이터(dataframe), 금융데이터 명세서
#			 - output : 필드항목별 이상치 index(json)
#=========================================================


import pandas as pd
import numpy as np
import sys

class SetDataFrame():
    def __init__(self, df, bank, stat, code):
        self.df = df
        self.bank = bank
        self.stat = stat
        self.code = code
        self.df = self.df.replace('',np.nan)

    def dcp_shape(self):
        return self.df.shape

    def dcp_types(self):
        types_dict = dict()
        for col in self.df.columns:
            try:
                types_dict[col] = self.stat[self.stat['COLUMN']==col]['TYPE'].iloc[0]
            except Exception as e:
                print("Error: 데이터 타입을 읽는 중 해당 에러가 발생했습니다. %s:%s"%(e, col))
        return types_dict



    def dcp_missing(self):
        missing = dict()
        for col in self.df.columns:
            missing[col] = self.df[self.df[col].isnull()].index.tolist()
        return missing


    def dcp_unique(self):
        unique = dict()
        for col in self.df.columns:
            ##### 페이관련 테이블 마지막 컬럼에 이상한 컬럼이 계속생기는데 원인을 모르겠음
            types = self.dcp_types().values()
            if (types in ['VARCHAR', 'BINARY']):
                code_value = str(self.stat[self.stat['COLUMN']==col]['CODE'].iloc[0])
                code_list = list(map(str, self.code[(self.code['CODE']==self.bank) & (self.code['CODE']==code_value)]['VALUE']))
                try:
                    self.df[col] = self.df[col].astype('float64')
                    self.df[col] = self.df[col].astype('int32')
                    self.df[col] = self.df[col].astype('string')
                except Exception as e:
                    print("Error: 데이터 unique 값을 읽는 중 해당 에러가 발생했습니다. %s:%s"%(e, col))
                unique[col] = [i for i in self.df[col].unique() if i in code_list]
            elif (types in ['VARCHAR', 'BINARY']):
                unique[col] = list(self.df[col].unique())
            else:
                unique[col] = list()
        return unique
        

    def dcp_outliers(self):
        
        outliers = dict()
        for col in self.df.columns:
            types = self.dcp_types().values()
            if (types not in ['BINARY','VARCHAR']):
                outliers[col] = list()
            elif types in ['INT','FLOAT']:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                outliers[col] = self.df[self.df[col].isnull()].index.tolist()
            else:
                code_value = str(self.stat[self.stat['COLUMN']==col]['CODE'].iloc[0])
                ##### 만약 컬럼에 null이 들어갔을경우 해당컬럼은 저절로 float 형식으로 바뀐다
                ##### 여기선 code_values가 int 형식이므로 float 형식으로 바꿔서 진행한다.
                if (self.df[col].isnull().sum()) > 0:
                    code_values = list(map(str, list(map(float, self.code[self.code['CODE']==code_value]['VALUE']))))
                else:
                    try:
                        self.df[col] = self.df[col].astype('float64')
                        self.df[col] = self.df[col].astype('int32')
                        self.df[col] = self.df[col].astype('string')
                    except Exception as e:
                        print("Error: 데이터 이상치를 찾는 중 해당 에러가 발생했습니다. %s:%s"%(e, col))
                    code_values = list(map(str, self.code[self.code['CODE']==code_value]['VALUE']))
                outliers[col] = self.df[(~self.df[col].isin(code_values))&(self.df[col].notnull())].index.tolist()
        return outliers