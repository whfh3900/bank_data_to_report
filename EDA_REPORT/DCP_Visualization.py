# -*- coding: utf-8 -*-

# 저작권       닉컴퍼니
# title     시각화 분석 : 데이터 분석에 대한 시각적 정보 전달
# filename  DCP_Visualization.py
# author    최승언
# version   0.12
# note      1. dcp_distribution_graph
#			 - 목적 : 범주형 필드항목은 데이터 불군형 및 희귀 변수값이 있는지 조사하고, 연속형 변수는 밀도가 한쪽으로 치우쳐 있는지 관찰.
#			 - 기능 : 각 필드항목의 밀도 분포 plot을 return
#			 - 사용 라이브러리 : seaborn에 있는 다양한 플롯 메소드
#			 - input : 범주형 항목 list, 엑셀시트
			 
#			 2. dcp_scale_comparison
#			 - 목적 : 연속형 필드항목의 원 데이터와 다양한 스케일 처리한 후의 밀도 분포 플롯을 비교
#			 - 기능 : 연속형 필드항목과 적용할 Scale의 밀도 분포 plot return
#			 - 사용 라이브러리 : seaborn에 있는 다양한 플롯 메소드
#			 - input : 수치형 항목 list, 엑셀시트
			 
#			 3. dcp_heatmap
#			 - 목적 : 변수간의 선형관계를 통해 피쳐선정, 파생변수 생성 등을 결정 
#			 - 기능 : 연속형 및 이진분류 필드항목의 상관관계 heatmap return
#			 - 사용 라이브러리 : seaborn의 heatmap 메소드 사용
#			 - input : 수치형 항목 list, 엑셀시트
#=========================================================

import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from openpyxl.drawing.image import Image
from DCP_Utils import *
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd


#### v0.12 버젼
class SetGraph():
    def __init__(self, df, bank, stat, pltpath):
        self.df = df
        self.bank = bank
        self.stat = stat
        self.pltpath = pltpath
        
        # self.df['ci_age'] = self.df['ci_age'].astype(int)
        
        # v0.13
        #plt.rc('font', family='Malgun Gothic')
        plt.rcParams["font.family"] = "NanumGothic"
        plt.rc('axes', unicode_minus=False)

    #### 1. Drawing a distribution graph
    # 범주형 필드항목의 분포도 그래프 생성
    def dcp_distribution_graph(self, sheet):
        cat = self.stat[(self.stat['TYPE'].isin(['VARCHAR','BINARY'])) & (self.stat['BANK'] == self.bank)]['COLUMN'].unique().tolist()
        excel_col = ['A','J','S','AB']
        excel_row = [i for i in range(1,1048553) if i%24==0]
        excel_row.insert(0,1)
        c = 0
        r = 0
        sheet['A{}'.format(excel_row[r])] = '전체'
        sheet['A{}'.format(excel_row[r])].border = border_styles()
        sheet['A{}'.format(excel_row[r])].font = font_styles()
        sheet['A{}'.format(excel_row[r])].fill = patternfill_styles(23)
        sheet['A{}'.format(excel_row[r])].alignment = alignment_styles()
        
        sheet.merge_cells('A{}:AJ{}'.format(excel_row[r],excel_row[r]))
        for i in cat:
            if c == 4:
                r+=1
                c=0
            imagefile = self.pltpath + "all_{}_{}_distribution_graph.png".format(self.bank, i)
            plt.clf() 
            sns.countplot(x=i, data=self.df)
            plt.savefig(imagefile)

            img = Image(imagefile)
            sheet.add_image(img, "{}{}".format(excel_col[c],excel_row[r]+1))
            c+=1
    
    
    
    #### 2. Drawing a scale comparison graph
    # 연속형 필드항목의 스케일 비교 describe 출력
    def dcp_scale_comparison(self, sheet):
        num = self.stat[(self.stat['TYPE'].isin(['INT','FLOAT'])) & (self.stat['BANK'] == self.bank)]['COLUMN'].unique().tolist()
        for i in num:
            self.df[i] = self.df[i].replace("", np.nan)
            self.df[i] = self.df[i].astype('float64')  
            scaler = StandardScaler()
            scaler.fit(self.df[i].to_numpy().reshape(-1,1))
            self.df[i+'_standard'] = scaler.transform(self.df[i].to_numpy().reshape(-1,1))
            scaler = MinMaxScaler()
            scaler.fit(self.df[i].to_numpy().reshape(-1,1))
            self.df[i+'_minmax'] = scaler.transform(self.df[i].to_numpy().reshape(-1,1))    
            scaler = RobustScaler()
            scaler.fit(self.df[i].to_numpy().reshape(-1,1))
            self.df[i+'_robust'] = scaler.transform(self.df[i].to_numpy().reshape(-1,1))        
            self.df[i+'_log'] = np.log1p(self.df[i])    
            self.df[i+'_log2'] = np.log2(self.df[i])   
            self.df[i+'_log10'] = np.log10(self.df[i])    

            describe = self.df[[j for j in self.df.columns if j.startswith(i)]].describe().reset_index()
            empty_list = ['']*len(self.df.columns)
            empty_list[0] = i+' 스케일 비교'
            sheet.append(empty_list)
            sheet.append(['요약','원본','StandardScale','MinMaxScale','RodustScale','LogScale','Log2Scale','Log10Scale'])
            for r in dataframe_to_rows(describe, index=False, header=False):
                sheet.append(r)    
            sheet.append(['']*len(self.df.columns))
            sheet.append(['']*len(self.df.columns))    


    #### 3. Drawing a heatmap graph
    # 연속형 필드항목의 히트맵 그래프 생성
    def dcp_heatmap(self, num, sheet):

        col_name = "_".join(num)
        imagefile = self.pltpath + "{}_{}_heatmap.png".format(col_name, self.bank)

        plt.clf()
        sns.heatmap(self.df[num].corr(),\
                    cmap = 'RdYlBu_r',\
                    annot = True)
        plt.savefig(imagefile)

        img = Image(imagefile)
        sheet.add_image(img, "A1")


# if __name__=="__main__":
#     df = pd.read_csv("../data/v2/ATS.csv", encoding="cp949")
#     bank = "URI"
#     stat = pd.read_csv("../data/v2/stat.csv", encoding="cp949")
#     pltpath = "../data/v2/graph"
#     sg = SetGraph(df, bank, stat, pltpath)