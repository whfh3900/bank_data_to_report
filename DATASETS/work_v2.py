import pandas as pd
from glob import glob
from work import *
from tqdm import tqdm
import os
tqdm.pandas()
from utils import *


def case_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        # tokens = text_pre.split("-", "－")
        
        tokens = re.split(r'-|－', text_pre)
        token_1 = tokens[0]
        token_2 = tokens[-1]
        
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        token_2_mean = "이름" if token_2 != "월급여" else "급여"
        object_2 = "이름" if token_2 != "월급여" else "금융용어"
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_1_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
            
        token_2 = "청약"
        token_1 = text_pre.replace(token_2, "")
        token_1 = token_1.replace("~", "")
        token_1 = token_1.replace(" ", "")

        token_1_mean = "이름"
        object_1 = "이름"
        token_2_mean = "청약"
        object_2 = "금융용어"
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "청약 저축으로 입금된 내역의 적요이다." if tran_diff == "입금" else "청약 저축으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "청약 저축으로 입금된 내역의 적요이다." if tran_diff == "입금" else "청약 저축으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_2(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        for i in ["월급여", "급여"]:
            if text_pre[2:].endswith(i):
                token_3 = i
                token_3_mean = token_3
                object_3 = "금융용어"
                
                token_2 = text_pre[2:].replace(token_3, "")
                token_2 = del_sw(token_2)
                
                token_2_mean = token_2
                object_2 = "알수없음"
                break
                
        new_df = new_df.append({'확인용': num,
                        '적요': text,
                        '적요일련번호': text_num,
                        '입출금구분': tran_diff,
                        '데이터셋출처': data_sour,
                        '출처번호': sour_num,
                        '적요구조': text_stru,
                        '적요구조일련번호': text_stru_num,
                        '적요 설명': "%s 계좌에서 급여가 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 급여를 이체한 내역의 적요이다."%token_1_mean,
                        '거래코드': tran_code,
                        '분류': clas,
                        '분류번호': clas_num,
                        '최소금액': min_amou,
                        '최대금액': max_amou,
                        '단어': token_1,
                        '단어일련번호':0,
                        '단어의미':token_1_mean,
                        '개체명': object_1,
                        '완료여부':1,
                        }, ignore_index=True)
        
        word_num = 1
        if (token_2 != ""):
            new_df = new_df.append({'확인용': num,
                            '적요': text,
                            '적요일련번호': text_num,
                            '입출금구분': tran_diff,
                            '데이터셋출처': data_sour,
                            '출처번호': sour_num,
                            '적요구조': text_stru,
                            '적요구조일련번호': text_stru_num,
                            '적요 설명': "%s 계좌에서 급여가 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 급여를 이체한 내역의 적요이다."%token_1_mean,
                            '거래코드': tran_code,
                            '분류': clas,
                            '분류번호': clas_num,
                            '최소금액': min_amou,
                            '최대금액': max_amou,
                            '단어': token_2,
                            '단어일련번호':word_num,
                            '단어의미':token_2_mean,
                            '개체명': object_2,
                            '완료여부':1,
                            }, ignore_index=True)
            word_num+=1
        new_df = new_df.append({'확인용': num,
                    '적요': text,
                    '적요일련번호': text_num,
                    '입출금구분': tran_diff,
                    '데이터셋출처': data_sour,
                    '출처번호': sour_num,
                    '적요구조': text_stru,
                    '적요구조일련번호': text_stru_num,
                    '적요 설명': "%s 계좌에서 급여가 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 급여를 이체한 내역의 적요이다."%token_1_mean,
                    '거래코드': tran_code,
                    '분류': clas,
                    '분류번호': clas_num,
                    '최소금액': min_amou,
                    '최대금액': max_amou,
                    '단어': token_3,
                    '단어일련번호':word_num,
                    '단어의미':token_3_mean,
                    '개체명': object_3,
                    '완료여부':1,
                    }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_3(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        tokens = text_pre.split("월급여")
        token_1 = del_sw(tokens[0])
        token_2 = "월급여"
        token_3 = del_sw(tokens[-1])
        
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        token_2_mean = "급여"
        object_2 = "금융용어"
        token_3_mean = "이름"
        object_3 = "이름"
        
        word_num = 0
        if token_1.replace(" ", "") != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_4(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        token_1 = "신한"
        token_2 = "신한"
        
        token_1_mean = bank_dict.get(token_1, token_1)
        token_2_mean = bank_dict.get(token_1, token_1)
        
        object_1 = "은행명"
        object_2 = "은행명"
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 2
        tokens = del_sw(text_pre[5:])
        
        for i in tokens.split():
            if (i != ""):
                token_3 = i
                token_3_mean = token_3
                object_3 = "알수없음"
        
        
                new_df = new_df.append({'확인용': num,
                                        '적요': text,
                                        '적요일련번호': text_num,
                                        '입출금구분': tran_diff,
                                        '데이터셋출처': data_sour,
                                        '출처번호': sour_num,
                                        '적요구조': text_stru,
                                        '적요구조일련번호': text_stru_num,
                                        '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                        '거래코드': tran_code,
                                        '분류': clas,
                                        '분류번호': clas_num,
                                        '최소금액': min_amou,
                                        '최대금액': max_amou,
                                        '단어': token_3,
                                        '단어일련번호':word_num,
                                        '단어의미':token_3_mean,
                                        '개체명': object_3,
                                        '완료여부':1,
                                        }, ignore_index=True)
                word_num += 1
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_5(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        # tokens = re.split(r'-|－', text_pre)
        token_1 = text_pre[0:2]
        token_3 = "급여"
        
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"

        token_3_mean = "급여"
        object_3 = "금융용어"
        
        

        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        tokens = del_sw(text_pre[2:-2])
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 ="알수없음"
        
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 급여 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_6(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        
        for i in bank_dict.keys():
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = bank_dict.get(token_1, token_1) 
                object_1 = "은행명"
                tokens = del_sw(text_pre.replace(token_1, ""))
                
                for j in comp_word_for_contains.split("|"):
                     if j in tokens:
                         token_3 = j
                         token_3_mean = token_3
                         object_3 ="금융용어"
                         tokens = del_sw(tokens.replace(token_3, ""))
                         break
                break
                
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s 으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s 으로(로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = i
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 계좌에서 %s 으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s 으로(로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s 으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s 으로(로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_7(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        tokens = re.split(r'-|－', text_pre)
        token_1 = tokens[0]
        token_2 = "국민은행" if tokens[-1].startswith("국민은행") else "국민" 
        
        token_3 = tokens[-1][4:] if tokens[-1].startswith("국민은행") else tokens[-1][2:]
        token_3 = del_sw(token_3).replace(" ", "")

        token_1_mean = "KB국민은행"
        object_1 = "은행명"
        token_2_mean = "KB국민은행"
        object_2 ="은행명"
        token_3_mean = token_3
        object_3 = "금융용어"
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 %s으로(로) 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else token_1_mean+" 계좌로 %s 때문에 이체한 내역의 적요이다."%token_3_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 %s으로(로) 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else token_1_mean+" 계좌로 %s 때문에 이체한 내역의 적요이다."%token_3_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        if token_3.replace(" ","") != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 %s으로(로) 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else token_1_mean+" 계좌로 %s 때문에 이체한 내역의 적요이다."%token_3_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':2,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_8(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in bank_dict.keys():
            if text_pre.startswith(i):
                token_1 = text_pre[0:2]
                for j in save_word_for_contains.split("|"):
                     if j in text_pre[2:]:
                         token_3 = j
                         tokens = text_pre[2:].replace(token_3, " ")
                         tokens = del_sw(tokens)
                         break
                
        token_1_mean = bank_dict.get(token_1, token_1) 
        object_1 = "은행명"
        token_3_mean = token_3
        object_3 ="금융용어"
        
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s을(를) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = i
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 계좌에서 %s으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s을(를) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s을(를) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_9(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        tokens = re.split(r'-|－', text_pre)
        token_1 = tokens[0]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        for i in ede_word_for_contains.split("|"):
            index = tokens[-1].find(i)
            if index == -1:
                continue
            else:
                token_3 = tokens[-1][index:index+len(i)]
                
        tokens =  tokens[-1].replace(token_3, " ").split()

        if token_3 == "방과후":
            token_3_mean = "방과후교육비"
            object_3 ="교육비"
        else:
            token_3_mean = token_3
            object_3 ="교육비"
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 %s 로(으로) 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else token_1_mean+" 계좌로 %s 로(으로) 이체한 내역의 적요이다."%token_3_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for token_2 in tokens:
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 %s 로(으로) 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else token_1_mean+" 계좌로 %s 로(으로) 이체한 내역의 적요이다."%token_3_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1    
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 %s 로(으로) 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else token_1_mean+" 계좌로 %s 로(으로) 이체한 내역의 적요이다."%token_3_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_10(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"

        for i in insu_word_for_contains.split("|"):
            if i in text_pre[2:]:
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"
                
                tokens = del_sw(text_pre[2:].replace(token_2, " "))
                break
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_2_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_2_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 2
        for i in tokens.split():
            token_3 = i
            token_3_mean = i
            object_3 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_2_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_2_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':word_num,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num+=1
            
            
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_10_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"

        for i in resi_word_for_contains.split("|"):
            if i in text_pre[2:]:
                token_3 = i
                token_3_mean = token_3
                object_3 = "금융용어"
                
                tokens = del_sw(text_pre[2:].replace(token_3, " "))
                break
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = i
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num+=1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
            
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_10_2(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"

        for i in loan_word_for_contains.split("|"):
            if i in text_pre[2:]:
                token_3 = i
                token_3_mean = token_3
                object_3 = "금융용어"
                
                tokens = del_sw(text_pre[2:].replace(token_3, " "))
                break
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = i
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num+=1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 %s로(으로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s로(으로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)

            
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_11(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = del_sw(text_pre)
        token_1_mean = "이름"
        object_1 = "이름"

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "개인간거래로 입금된 내역의 적요이다." if tran_diff == "입금" else "개인간거래로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_12(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        
        token_1 = text_pre[:2]        
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        token_2 = del_sw(text_pre.replace(token_1, ""))
        token_2_mean = "이름"
        object_2 = "이름"
        
        text_mean = list()
        if any(word in tran_code for word in ["급여", "대량"]):
            # 0: 입금 # 1: 출금
            text_mean.append(token_1_mean+"에서 급여가 입금된 내역의 적요이다.")
            text_mean.append(token_1_mean+"에 급여 이체한 내역의 적요이다.")
        else:
            # 0: 입금 # 1: 출금
            text_mean.append(token_1_mean+"에서 입금된 내역의 적요이다.")
            text_mean.append(token_1_mean+"에 이체한 내역의 적요이다.")

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean[0] if tran_diff == "입금" else text_mean[1],
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        if token_2.replace(" ","") != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': text_mean[0] if tran_diff == "입금" else text_mean[1],
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':1,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_13(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = "1회"
        token_1_mean = "저축/투자횟수"
        object_1 = "저축/투자횟수"
        for i in ["0회","00회","000회"]:
            if text_pre.startswith(i):
                tokens = del_sw(text_pre.replace(i, ""))
                break
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "저축 및 투자로 입금된 내역의 적요이다." if tran_diff == "입금" else "저축 및 투자로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        
        if check_language(tokens):
            for i,n in enumerate(tokens.split()):
                token_2 = n
                token_2 = token_2.replace(" ", "")
                if i == 0:
                    token_2_mean = "이름"
                    object_2 = "이름"
                else:
                    token_2_mean = token_2
                    object_2 = "알수없음" 
                if token_2 != "":
                    new_df = new_df.append({'확인용': num,
                                            '적요': text,
                                            '적요일련번호': text_num,
                                            '입출금구분': tran_diff,
                                            '데이터셋출처': data_sour,
                                            '출처번호': sour_num,
                                            '적요구조': text_stru,
                                            '적요구조일련번호': text_stru_num,
                                            '적요 설명': "저축 및 투자로 입금된 내역의 적요이다." if tran_diff == "입금" else "저축 및 투자로 이체한 내역의 적요이다.",
                                            '거래코드': tran_code,
                                            '분류': clas,
                                            '분류번호': clas_num,
                                            '최소금액': min_amou,
                                            '최대금액': max_amou,
                                            '단어': token_2,
                                            '단어일련번호':word_num,
                                            '단어의미':token_2_mean,
                                            '개체명': object_2,
                                            '완료여부':1,
                                            }, ignore_index=True)
                    word_num += 1
        else:
            token_2 = tokens
            token_2 = token_2.replace(" ", "")
            token_2_mean = "이름"
            object_2 = "이름"
            if token_2 != "":
                new_df = new_df.append({'확인용': num,
                                        '적요': text,
                                        '적요일련번호': text_num,
                                        '입출금구분': tran_diff,
                                        '데이터셋출처': data_sour,
                                        '출처번호': sour_num,
                                        '적요구조': text_stru,
                                        '적요구조일련번호': text_stru_num,
                                        '적요 설명': "저축 및 투자로 입금된 내역의 적요이다." if tran_diff == "입금" else "저축 및 투자로 이체한 내역의 적요이다.",
                                        '거래코드': tran_code,
                                        '분류': clas,
                                        '분류번호': clas_num,
                                        '최소금액': min_amou,
                                        '최대금액': max_amou,
                                        '단어': token_2,
                                        '단어일련번호':word_num,
                                        '단어의미':token_2_mean,
                                        '개체명': object_2,
                                        '완료여부':1,
                                        }, ignore_index=True)
                word_num += 1
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df
        
        
def case_14(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        for i in goal_word_for_contains.split("|"):
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = i
            object_1 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_15(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        tokens = del_sw(text_pre.replace("세무법인", ""))
        
        token_2 = "세무법인"
        token_2_mean = "세무법인"
        object_2 = "금융용어"
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = i
            object_1 = "법인명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "세무법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무법인으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무법인으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_16(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        # tokens = text_pre.split("-", "－")
        text_pre = text_pre.replace("세무사", " 세무사 ")
        text_pre = text_pre.replace("사무", " 사무 ")
        text_pre = text_pre.replace("기장", " 기장 ")
        tokens = re.split(r'-|－| |_', text_pre)
        #token_1 = tokens[0]
        #token_2 = tokens[-1]
        
        if text_pre[2]=="-" or text_pre[2]=="－":
            for i in bank_dict_2.get(tokens[0], tokens[0]):
                if tokens[1].startswith(i):
                    tokens[1] = tokens[1].replace(i,"")
                    break
        else :
            if text_pre[0:2] in bank_dict.keys():
                text_pre = text_pre[0:2] + " "+ text_pre[2:]
                tokens = re.split(r'-|－| |_', text_pre)
            
        tokens = [re.sub(r'[^\w\s]', ' ', x) for x in tokens]    
        temp = re.split(r'-|－| |_', " ".join(tokens))
        tokens = [v for v in temp if v]

        tokens_mean=[]
        object_mean=[]
        for i in range(len(tokens)):
            if tokens[i] in bank_dict.keys():
                tokens_mean.append(bank_dict.get(tokens[i], tokens[i]))
                object_mean.append('은행명')
            elif tokens[i] in ["급여","월급여"]:
                tokens_mean.append("급여")
                object_mean.append("급여")
            elif tokens[i] in ["청약","적금","저축"]:
                tokens_mean.append(tokens[i])
                object_mean.append(tokens[i])
            elif tokens[i] in ["세무사"]:
                tokens_mean.append("세무사")
                object_mean.append("세무사")
            else:
                tokens_mean.append("이름/법인명")
                object_mean.append("이름/법인명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무사무소에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무사무소로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_17(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        if text_pre.startswith("세무회계"):
            token_1 = "세무회계"
            token_1_mean = "세무회계법인"
            object_1 = "금융용어"
            
            token_2 = text_pre.replace("세무회계", "")
            token_2_mean = token_2
            object_2 = "법인명"
        else:
            token_1 = text_pre.replace("세무회계", "")
            token_1_mean = token_1
            object_1 = "법인명"
            
            token_2 = "세무회계"
            token_2_mean = "세무회계법인"
            object_2 = "금융용어"
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무회계법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계법인으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무회계법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계법인으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_18(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        token_2 = "세무회계사"
        token_2_mean = "세무회계사"
        object_2 = "직업"
        
        tokens = del_sw(text_pre.replace(token_2, ""))

        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = "이름"
            object_1 = "이름"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "세무회계사 에게서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계사 에게서 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무회계사 에게서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계사 에게서 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_19(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = text_pre.replace("회계사", "")
        token_1_mean = "이름"
        object_1 = "이름"
        
        token_2 = "회계사"
        token_2_mean = "회계사"
        object_2 = "직업"
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "회계사에게서 입금된 내역의 적요이다." if tran_diff == "입금" else "회계사에게 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "회계사에게서 입금된 내역의 적요이다." if tran_diff == "입금" else "회계사에게 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_20(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        text_pre = text_pre.replace("회계법인", " 회계법인 ")
        text_pre = text_pre.replace("사무", " 사무 ")
        text_pre = text_pre.replace("기장", " 기장 ")
        tokens = re.split(r'-|－| |_', text_pre)
        
        if text_pre[2]=="-" or text_pre[2]=="－":
            for i in bank_dict_2.get(tokens[0], tokens[0]):
                if tokens[1].startswith(i):
                    tokens[1] = tokens[1].replace(i,"")
                    break
        else :
            if text_pre[0:2] in bank_dict.keys():
                text_pre = text_pre[0:2] + " "+ text_pre[2:]
                tokens = re.split(r'-|－| |_', text_pre)
            
        tokens = [re.sub(r'[^\w\s]', ' ', x) for x in tokens]    
        temp = re.split(r'-|－| |_', " ".join(tokens))
        tokens = [v for v in temp if v]

        tokens_mean=[]
        object_mean=[]
        for i in range(len(tokens)):
            if tokens[i] in bank_dict.keys():
                tokens_mean.append(bank_dict.get(tokens[i], tokens[i]))
                object_mean.append('은행명')
            elif tokens[i] in ["급여","월급여"]:
                tokens_mean.append("급여")
                object_mean.append("급여")
            elif tokens[i] in ["청약","적금","저축"]:
                tokens_mean.append(tokens[i])
                object_mean.append(tokens[i])
            elif tokens[i] in ["회계법인"]:
                tokens_mean.append("회계법인")
                object_mean.append("회계법인")
            else:
                tokens_mean.append("법인명")
                object_mean.append("법인명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "회계법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "회계법인으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_21(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["급여이체", "급여입금", "급여지급", "급여수당"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"      
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break  
            
        word_num = 0
        for i in tokens.split():
            token_1 = i
            if token_1.replace(" ", "") != "":
                token_1_mean = token_1
                object_1 = "알수없음"
                new_df = new_df.append({'확인용': num,
                                        '적요': text,
                                        '적요일련번호': text_num,
                                        '입출금구분': tran_diff,
                                        '데이터셋출처': data_sour,
                                        '출처번호': sour_num,
                                        '적요구조': text_stru,
                                        '적요구조일련번호': text_stru_num,
                                        '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                        '거래코드': tran_code,
                                        '분류': clas,
                                        '분류번호': clas_num,
                                        '최소금액': min_amou,
                                        '최대금액': max_amou,
                                        '단어': token_1,
                                        '단어일련번호':word_num,
                                        '단어의미':token_1_mean,
                                        '개체명': object_1,
                                        '완료여부':1,
                                        }, ignore_index=True)
                word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_21_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        token_2 = "급여"
        token_2_mean = token_2
        object_2 = "금융용어"   
        
        token_1 = del_sw(text_pre.replace("급여", ""))
        token_1 = token_1.replace(" ","")
        token_1_mean = token_1
        object_1 = "알수없음"

        word_num = 0
        if token_1 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_22(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        text_pre = text_pre.replace("세무그룹", " 세무그룹 ")
        tokens = re.split(r'-|－| |_', text_pre)
        
        if text_pre[2]=="-" or text_pre[2]=="－":
            for i in bank_dict_2.get(tokens[0], tokens[0]):
                if tokens[1].startswith(i):
                    tokens[1] = tokens[1].replace(i,"")
                    break
        else :
            if text_pre[0:2] in bank_dict.keys():
                text_pre = text_pre[0:2] + " "+ text_pre[2:]
                tokens = re.split(r'-|－| |_', text_pre)
            
        tokens = [re.sub(r'[^\w\s]', ' ', x) for x in tokens]    
        temp = re.split(r'-|－| |_', " ".join(tokens))
        tokens = [v for v in temp if v]

        tokens_mean=[]
        object_mean=[]
        for i in range(len(tokens)):
            if tokens[i] in bank_dict.keys():
                tokens_mean.append(bank_dict.get(tokens[i], tokens[i]))
                object_mean.append('은행명')
            elif tokens[i] in ["급여","월급여"]:
                tokens_mean.append("급여")
                object_mean.append("급여")
            elif tokens[i] in ["청약","적금","저축"]:
                tokens_mean.append(tokens[i])
                object_mean.append(tokens[i])
            elif tokens[i] in ["세무그룹"]:
                tokens_mean.append("세무그룹")
                object_mean.append("세무그룹")
            else:
                tokens_mean.append("법인명")
                object_mean.append("법인명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무그룹에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무그룹으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_23(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = text_pre.replace("세무회", "")
        token_1_mean = token_1
        object_1 = "법인명"
        
        token_2 = "세무회"
        token_2_mean = "세무회계법인"
        object_2 = "금융용어"
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무회계법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계법인에 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "세무회계법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계법인에 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_24(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        # tokens = text_pre.split("-", "－")
        text_pre = text_pre.replace("노무법인", " 노무법인 ")
        tokens = re.split(r'-|－| |_', text_pre)
        #token_1 = tokens[0]
        #token_2 = tokens[-1]
        
        if text_pre[2]=="-" or text_pre[2]=="－":
            for i in bank_dict_2.get(tokens[0], tokens[0]):
                if tokens[1].startswith(i):
                    tokens[1] = tokens[1].replace(i,"")
                    break
        else :
            if text_pre[0:2] in bank_dict.keys():
                text_pre = text_pre[0:2] + " "+ text_pre[2:]
                tokens = re.split(r'-|－| |_', text_pre)
            
        tokens = [re.sub(r'[^\w\s]', ' ', x) for x in tokens]    
        temp = re.split(r'-|－| |_', " ".join(tokens))
        tokens = [v for v in temp if v]

        tokens_mean=[]
        object_mean=[]
        for i in range(len(tokens)):
            if tokens[i] in bank_dict.keys():
                tokens_mean.append(bank_dict.get(tokens[i], tokens[i]))
                object_mean.append('은행명')
            elif tokens[i] in ["급여","월급여"]:
                tokens_mean.append("급여")
                object_mean.append("급여")
            elif tokens[i] in ["청약","적금","저축"]:
                tokens_mean.append(tokens[i])
                object_mean.append(tokens[i])
            elif tokens[i] in ["노무법인"]:
                tokens_mean.append("노무법인")
                object_mean.append("노무법인")
            else:
                tokens_mean.append("법인명")
                object_mean.append("법인명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "노무법인에서 입금된 내역의 적요이다." if tran_diff == "입금" else "노무법인으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_25(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        tokens = del_sw(text_pre.replace("SK쉴더스", ""))
        
        token_1 = "SK쉴더스"
        token_1_mean = "SK쉴더스"
        object_1 = "기업명"
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "SK쉴더스에서 입금된 내역의 적요이다." if tran_diff == "입금" else "SK쉴더스에 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i,n in enumerate(tokens.split()):
            token_2 = n
            token_2_mean = token_2
            if i == 0:
                object_2 = "지역명"
            else:
                object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "SK쉴더스에서 입금된 내역의 적요이다." if tran_diff == "입금" else "SK쉴더스에 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_26(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        for i in ["급여", "상여", "성과", "월급"]:
            if i in text_pre:
                token_2 = i
                if i in ["상여", "성과"]:
                    token_2_mean = token_2+"금"
                elif i in ["급여", "월급"]:
                    token_2_mean = token_2
                object_2 = "금융용어"
                break

        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i,n in enumerate(tokens.split()):
            token_1 = n
            token_1_mean = token_1
            if i == 0:
                object_1 = "회사명"
            else:
                object_1 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_27(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        tokens = del_sw(text_pre)
        
        
        text_mean = list()
        if any(word in tran_code for word in ["급여", "대량"]):
            # 0: 입금 # 1: 출금
            text_mean.append("급여가 입금된 내역의 적요이다.")
            text_mean.append("급여 이체한 내역의 적요이다.")
        else:
            # 0: 입금 # 1: 출금
            text_mean.append("회사에서 입금된 내역의 적요이다.")
            text_mean.append("회사에 이체한 내역의 적요이다.")
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            if token_1 == "주식회사":
                object_1 = "금융용어"
            elif "은행" in token_1_mean:
                object_1 = "은행명"
            else:
                object_1 = "회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': text_mean[0] if tran_diff == "입금" else text_mean[1],
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_27_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        tokens = del_sw(text_pre)

        text_mean = list()
        if any(word in tran_code for word in ["급여", "대량"]):
            # 0: 입금 # 1: 출금
            text_mean.append("급여가 입금된 내역의 적요이다.")
            text_mean.append("급여 이체한 내역의 적요이다.")
        else:
            # 0: 입금 # 1: 출금
            text_mean.append("회사에서 입금된 내역의 적요이다.")
            text_mean.append("회사에 이체한 내역의 적요이다.")

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "주식회사"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': text_mean[0] if tran_diff == "입금" else text_mean[1],
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
        
            word_num += 1
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_28(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        tokens = del_sw(text_pre.replace("", ""))

        
        token_2 = "세무서"
        token_2_mean = "세무서"
        object_2 = "기관명"
        
        token_1 = del_sw(text_pre.replace(token_2, ""))
        token_1_mean = token_1
        object_1 = "지역명"


        new_df = new_df.append({'확인용': num,
                        '적요': text,
                        '적요일련번호': text_num,
                        '입출금구분': tran_diff,
                        '데이터셋출처': data_sour,
                        '출처번호': sour_num,
                        '적요구조': text_stru,
                        '적요구조일련번호': text_stru_num,
                        '적요 설명': "세무서에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무서에 이체한 내역의 적요이다.",
                        '거래코드': tran_code,
                        '분류': clas,
                        '분류번호': clas_num,
                        '최소금액': min_amou,
                        '최대금액': max_amou,
                        '단어': token_1,
                        '단어일련번호':0,
                        '단어의미':token_1_mean,
                        '개체명': object_1,
                        '완료여부':1,
                        }, ignore_index=True)
        

        new_df = new_df.append({'확인용': num,
                        '적요': text,
                        '적요일련번호': text_num,
                        '입출금구분': tran_diff,
                        '데이터셋출처': data_sour,
                        '출처번호': sour_num,
                        '적요구조': text_stru,
                        '적요구조일련번호': text_stru_num,
                        '적요 설명': "세무서에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무서에 이체한 내역의 적요이다.",
                        '거래코드': tran_code,
                        '분류': clas,
                        '분류번호': clas_num,
                        '최소금액': min_amou,
                        '최대금액': max_amou,
                        '단어': token_2,
                        '단어일련번호':1,
                        '단어의미':token_2_mean,
                        '개체명': object_2,
                        '완료여부':1,
                        }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_29(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_3 = "요금"
        token_3_mean = "요금"
        object_3 = "금융용어"
        
        
        tokens = del_sw(text_pre.replace(token_3, ""))

        token_2 = ""
        token_2_mean = ""
        for i in ["전화", "핸드폰", "휴대폰", "통신", "도시가스", "가스", "청소", "수도", "전기", "분납"]:
            if tokens.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "요금명"
                tokens = del_sw(tokens.replace(token_2, ""))
                break
                
    
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if token_2 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_30(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "입금"
        token_2_mean = token_2
        object_2 = "금융용어"
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "입금된 내역의 적요이다." if tran_diff == "입금" else "알수없음",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "입금된 내역의 적요이다." if tran_diff == "입금" else "알수없음",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_31(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_2 = "상금"
        token_2_mean = "상금"
        object_2 = "금융용어"

        tokens = del_sw(text_pre.replace("상금", ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "상금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "상금으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "상금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "상금으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_32(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        pay = ["월급여","월급","급여"]
        pay_is = False
        
        for i in pay:
            if i in text_pre:
                text_pre = text_pre.replace(i, " "+i+" ")
                pay_is = True
                break;
        
        text_pre = text_pre.replace("세무", " 세무 ")
        tokens = re.split(r'-|－| |　|_', text_pre)

        
        if text_pre[2]=="-" or text_pre[2]=="－":
            for i in bank_dict_2.get(tokens[0], tokens[0]):
                if tokens[1].startswith(i):
                    tokens[1] = tokens[1].replace(i,"")
                    break
        else :
            if text_pre[0:2] in bank_dict.keys():
                text_pre = text_pre[0:2] + " "+ text_pre[2:]
                tokens = re.split(r'-|－| |_', text_pre)
            
        tokens = [re.sub(r'[^\w\s]', ' ', x) for x in tokens]    
        temp = re.split(r'-|－| |_', " ".join(tokens))
        tokens = [v for v in temp if v]
        if pay_is ==True:
            word_text = "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다."
        else:
            word_text = "세무회계사무소에서 입금된 내역의 적요이다." if tran_diff == "입금" else "세무회계사무소에 이체한 내역의 적요이다."
        tokens_mean=[]
        object_mean=[]
        for i in range(len(tokens)):
            if tokens[i] in bank_dict.keys():
                tokens_mean.append(bank_dict.get(tokens[i], tokens[i]))
                object_mean.append('은행명')
            elif tokens[i] in ["급여","월급여"]:
                tokens_mean.append("급여")
                object_mean.append("급여")
            elif tokens[i] in ["청약","적금","저축"]:
                tokens_mean.append(tokens[i])
                object_mean.append(tokens[i])
            elif tokens[i] in ["세무"]:
                tokens_mean.append("세무회계사무소")
                object_mean.append("세무회계사무소")
            elif tokens[i] in ["주"]:
                tokens_mean.append("주식회사")
                object_mean.append("주식회사")
            else:
                tokens_mean.append("이름/회사명")
                object_mean.append("이름/회사명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': word_text,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_33(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
                
        token_1 = "농협"
        token_2 = "농협"         
        token_3 = del_sw(text_pre[5:])
        token_3 = token_3.replace(" ", "")

        token_1_mean = "농협은행"
        object_1 = "은행명"
        token_2_mean = "농협은행"
        object_2 ="은행명"
        token_3_mean = token_3
        object_3 = "알수없음"
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "농협은행 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else "농협은행 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "농협은행 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else "농협은행 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        if token_3 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "농협은행 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else "농협은행 계좌로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':2,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_34(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        # tokens = text_pre.split("-", "－")

        allowance = ["용돈"]
        fee = ['월회비','회비','계돈','모임비','모임','곗돈']
        allowance_is = False
        fee_is = False
        
        for i in allowance:
            if i in text_pre:
                text_pre = text_pre.replace(i, " "+i+" ")
                allowance_is = True
                break;
        for i in fee:
            if i in text_pre:
                text_pre = text_pre.replace(i, " "+i+" ")
                fee_is = True
                break;
        
        
        
        tokens = re.split(r'-|－| |　|_', text_pre)

        bank_is = False
        if text_pre[2]=="-" or text_pre[2]=="－":
            bank_is = True
            for i in bank_dict_2.get(tokens[0], tokens[0]):
                if tokens[1].startswith(i):
                    tokens[1] = tokens[1].replace(i,"")                
                    break
        else :
            if text_pre[0:2] in bank_dict.keys():
                text_pre = text_pre[0:2] + " "+ text_pre[2:]
                tokens = re.split(r'-|－| |_', text_pre)
                bank_is = True
                
        
        tokens = [re.sub(r'[^\w\s]', ' ', x) for x in tokens]    
        temp = re.split(r'-|－| |_', " ".join(tokens))
        tokens = [v for v in temp if v]
        if allowance_is ==True and fee_is==False:
            word_text = "경조사/용돈이 입금된 내역의 적요이다." if tran_diff == "입금" else "경조사/용돈을 이체한 내역의 적요이다."
        elif allowance_is==False and fee_is ==True:
            word_text = "회비가 입금된 내역의 적요이다." if tran_diff == "입금" else "회비를 이체한 내역의 적요이다."
        else:
            word_text = "경조사/용돈이 입금된 내역의 적요이다." if tran_diff == "입금" else "경조사/용돈을 이체한 내역의 적요이다."
        
        if bank_is:
            word_text = bank_dict.get(tokens[0], tokens[0])+" 계좌에서 "+word_text if tran_diff =='입금' else bank_dict.get(tokens[0], tokens[0])+" 계좌로 "+word_text
        
            
        tokens_mean=[]
        object_mean=[]
        for i in range(len(tokens)):
            if tokens[i] in bank_dict.keys():
                tokens_mean.append(bank_dict.get(tokens[i], tokens[i]))
                object_mean.append('은행명')
            elif tokens[i] in ["급여","월급여"]:
                tokens_mean.append("급여")
                object_mean.append("급여")
            elif tokens[i] in ["청약","적금","저축"]:
                tokens_mean.append(tokens[i])
                object_mean.append(tokens[i])
            elif tokens[i] in allowance:
                tokens_mean.append("용돈")
                object_mean.append("용돈")
            elif tokens[i] in fee:
                tokens_mean.append("회비")
                object_mean.append("회비")
            else:
                tokens_mean.append("이름/회사명")
                object_mean.append("이름/회사명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': word_text,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_35(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        tokens = re.split(r'-|－', text_pre)
        token_1 = tokens[0]
        token_2 = tokens[-1]
        
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        token_2_mean = token_2
        object_2 = "알수없음"

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_36(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        tokens = re.split(r'-|－', text_pre)
        token_1 = tokens[0]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        names = find_name(tokens[-1])
        tokens = tokens[-1]
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in names:
            token_2 = i
            token_2_mean = "이름"
            object_2 = "이름"
            tokens = tokens.replace(token_2, "")
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num +=1
        tokens = re.sub(r'[^\w\s]', ' ', tokens)
        for i in tokens.split():
            token_3 = i
            token_3_mean = token_3
            object_3 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':word_num,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_37(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["복지기금", "발전기금", "행복기금", "보증기금", "교육기금", "형제기금", "기금"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "기금명"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
                
    
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
        word_num += 1
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)

        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_38(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        token_2 = text_pre.replace(token_1, "")
        token_2_mean = token_2
        object_2 = "이름"

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_39(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        for i in ["월급여", "급여"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"   
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_39_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["월급여", "급여"]:
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = token_1
                object_1 = "금융용어"   
                tokens = del_sw(text_pre.replace(token_1, ""))
                break
            
        tokens = del_sw(text_pre.replace(token_1, ""))
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여 입금된 내역의 적요이다." if tran_diff == "입금" else "급여 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            


        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_40(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "연말정산"
        token_2_mean = token_2
        object_2 = "금융용어"   
        
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"   
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_41(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = text_pre[-5:]
        token_2_mean = token_2
        object_2 = "금융용어"   
        
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"   
        
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "상여금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "상여금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_41_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "상여금"
        token_2_mean = token_2
        object_2 = "금융용어"   
        
        tokens = del_sw(text_pre.replace("상여금", ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"   
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "상여금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "상여금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_42(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["성과급", "성과금"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"   
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_43(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["인센티브", "인센티", "인센"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = "인센티브"
                object_2 = "금융용어"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break

        word_num = 0        
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"   

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_43_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = "인센티브"
        token_1_mean = token_1
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace("인센티브", ""))

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "인센티브로 입금된 내역의 적요이다." if tran_diff == "입금" else "인센티브로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1        
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "사유"   

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "인센티브로 입금된 내역의 적요이다." if tran_diff == "입금" else "인센티브로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_44(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["카드대금", "사업대금", "물품대금", "결제대금", "판매대금", "이용대금", "대금"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"   
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"   

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_45(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = "연말정산"
        token_1_mean = token_1
        object_1 = "금융용어"   
        
        tokens = del_sw(text_pre.replace("연말정산", ""))
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "연말정산으로 입금된 내역의 적요이다." if tran_diff == "입금" else "연말정산으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "사유"  
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "연말정산으로 입금된 내역의 적요이다." if tran_diff == "입금" else "연말정산으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_46(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        for i in ["대학교", "고등학교", "중학교", "초등학교", "학교"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "기관명"
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "학교명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s에서 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s에서 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



##  나중에
def case_47(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = ""
        token_1_mean = ""
        tokens = text_pre
        for i in stoc_dict.keys():
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = stoc_dict.get(token_1, token_1)
                object_1 = "증권/자산운용사명"
                tokens = del_sw(text_pre.replace(token_1, ""))
                break
        
        token_2 = ""
        token_2_mean = token_2
        object_2 = "금융용어" 
        token_3 = ""
        token_3_mean = token_3
        object_3 = "금융용어"

        for i in securities:
            if i in text_pre:
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"   
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                for j in securities:
                    if j in tokens:
                        token_3 = j
                        token_3_mean = token_3
                        object_3 = "금융용어"  
                        tokens = del_sw(text_pre.replace(token_3, ""))
                        break
                break
                
        word_num = 0
        if token_1 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "주식으로 입금된 내역의 적요이다." if tran_diff == "입금" else "주식으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if token_2 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "주식으로 입금된 내역의 적요이다." if tran_diff == "입금" else "주식으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if token_3 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "주식으로 입금된 내역의 적요이다." if tran_diff == "입금" else "주식으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':word_num,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if (token_1 != "") & (token_2 != "") & (token_3 != ""):
            for i in tokens.split():
                token_1 = i
                token_1_mean = token_1
                object_1 = "알수없음"
                new_df = new_df.append({'확인용': num,
                                        '적요': text,
                                        '적요일련번호': text_num,
                                        '입출금구분': tran_diff,
                                        '데이터셋출처': data_sour,
                                        '출처번호': sour_num,
                                        '적요구조': text_stru,
                                        '적요구조일련번호': text_stru_num,
                                        '적요 설명': "주식으로 입금된 내역의 적요이다." if tran_diff == "입금" else "주식으로 이체한 내역의 적요이다.",
                                        '거래코드': tran_code,
                                        '분류': clas,
                                        '분류번호': clas_num,
                                        '최소금액': min_amou,
                                        '최대금액': max_amou,
                                        '단어': token_1,
                                        '단어일련번호':word_num,
                                        '단어의미':token_1_mean,
                                        '개체명': object_1,
                                        '완료여부':1,
                                        }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_48(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = "DB손보"
        token_1_mean = "DB손해보험"
        object_1 = "보험명"   
        
        token_2 = del_sw(text_pre.replace(token_1, ""))
        token_2_mean = token_2
        object_2 = "이름"   

        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_49(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "증권"
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "증권사명"
        
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "증권사로 입금된 내역의 적요이다." if tran_diff == "입금" else "증권사로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "증권사로 입금된 내역의 적요이다." if tran_diff == "입금" else "증권사로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_50(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = "KB증"
        token_1_mean = "KB증권"
        object_1 = "증권사명"   
        
        token_2 = del_sw(text_pre.replace(token_1, ""))
        token_2_mean = token_2
        object_2 = "이름"   

        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_51(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        for i in ["ＹＷＣＡ", "ＹＭＣＡ"]:
            if text_pre.endswith(i):
                token_2 = i
                token_1 = del_sw(text_pre.replace(token_2, ""))
                token_1_mean = token_1
                object_1 = "지역명"
                token_2_mean = token_2
                object_2 = "비영리단체"
                break
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s에서 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s에서 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_52(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["개인연금", "국민연금", "퇴직연금", "노후연금", "연금"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"   
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"   

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_53(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = text_pre[:4]
        token_1_mean = token_1
        object_1 = "회사명"
        
        tokens = del_sw(text_pre.replace(token_1, ""))

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "지역명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1


    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_54(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_1 = text_pre[:2]
        tokens = del_sw(text_pre.replace(token_1, ""))
        token_3 = text_pre[-2:]

        
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        token_3_mean = bank_dict.get(token_3, token_3)
        object_3 = "은행명"
        
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌로 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 계좌로 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s에 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_55(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = text_pre[-5:]
        token_2_mean = token_2
        object_2 = "장학금종류"
        
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_55_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = text_pre[-3:]
        token_2_mean = token_2
        object_2 = "금융용어"
        
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        word_num = 0
        
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_56(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "연차수당"
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        word_num = 0
        
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "회사명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_57(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        tokens = del_sw(text_pre.replace(token_1, ""))
        for i in cost_word_for_contains.split("|"):
            if tokens.endswith(i):
                token_3 = i
                token_3_mean = token_3
                object_3 = "금융용어"
                
                tokens = del_sw(tokens.replace(token_3, ""))
                break
        
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_3_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_3_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로 입금된 내역의 적요이다."%token_3_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_3_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)

        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_58(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "특별수당"
        token_2_mean = "특별수당금"
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "회사명"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_59(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = text_pre[-3:]
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "후원기업"
        
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_60(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "설상여"
        token_2_mean = "설 상여금"
        object_2 = "금융용어"
                
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "회사명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_61(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "환불"
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_62(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in cost_word_for_contains.split("|"):
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = i
                object_2 = "금융용어"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_63(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "명절상여"
        token_2_mean = "명절상여금"
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "명절상여금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "명절상여금으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "명절상여금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "명절상여금으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_64(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["(사)", "（사）", "사단법인", "사）"]:
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = "사단법인"
                object_1 = "금융용어"
        
                tokens = del_sw(text_pre.replace(token_1, ""))
                break

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "법인명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_65(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_2 = "저축은행"
        token_2_mean = "저축은행"
        object_2 = "금융용어"
        
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "저축은행명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 저축은행 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 저축은행 계좌로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 저축은행 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 저축은행 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_66(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        tokens = del_sw(text_pre)

        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "단말기회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "카드결제를 이용한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_67(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        for i in ["통신비지원금", "통신비지원"]:
            if text_pre.endswith(i):
                token_2 = i
                token_1 = del_sw(text_pre.replace(token_2, ""))
                token_1 = token_1.replace(" ", "")
        
        token_1_mean = token_1
        object_1 = "회사명"
        token_2_mean = "통신비지원금"
        object_2 = "금융용어"

        word_num = 0
        if token_1 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "통신비지원금 으로 입금된 내역의 적요이다." if tran_diff == "입금" else "통신비지원금 으로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "통신비지원금 으로 입금된 내역의 적요이다." if tran_diff == "입금" else "통신비지원금 으로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_67_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        token_1 = "통신비"
        token_1_mean = "통신비"
        object_1 = "금융용어"
        tokens = del_sw(text_pre.replace(token_1, ""))
        
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "통신비를 입금한 내역의 적요이다." if tran_diff == "입금" else "통신비로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "통신비를 입금한 내역의 적요이다." if tran_diff == "입금" else "통신비로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num+=1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_68(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        token_2 = "명절수당"
        token_2_mean = "명절수당"
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_69(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        lists = ["추가상여", "정기상여", "성과상여", "급여상여"]
        for i in lists:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2+"금"
                object_2 = "금융용어"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "상여금이 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금을 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "상여금이 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금을 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_69_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_2 = "상여"
        token_2_mean = token_2+"금"
        object_2 = "금융용어"

        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "회사명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "상여금이 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금을 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "상여금이 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금을 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_69_2(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_2 = "상여"
        token_2_mean = token_2+"금"
        object_2 = "금융용어"

        token_1 = del_sw(text_pre.replace(token_2, ""))
        token_1 = token_1.replace(" ", "")
        token_1_mean = token_1
        object_1 = "사유"

        word_num = 0
        if token_1 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "상여금이 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금을 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "상여금이 입금된 내역의 적요이다." if tran_diff == "입금" else "상여금을 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_70(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        for i in fare_word_for_contains.split("|"):
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_71(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        tokens = del_sw(text_pre.replace(token_1, ""))
        
        for i in inco_comp_dict.keys():
            if i in tokens:
                
                token_2 = i
                token_2_mean = inco_comp_dict.get(token_2, token_2)
                object_2 = "법인명"
                
                tokens = del_sw(tokens.replace(token_2, ""))
                break


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 회사에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌에서 회사로 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 계좌에서 회사에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌에서 회사로 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 2
        for i in tokens.split():
            token_3 = i
            token_3_mean = token_3
            object_3 = "회사명"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 계좌에서 회사에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌에서 회사로 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':word_num,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df







def case_72(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        
        for i in comp_word_for_contains.split("|"):
            if i in text_pre:
                token_1 = i
                token_1_mean = token_1
                object_1 = "금융용어"
                
                tokens = del_sw(text_pre.replace(token_1, ""))
                
                for j in inco_comp_dict.keys():
                    if j in tokens:
                        token_2 = j
                        token_2_mean = token_2
                        object_2 = "법인명"
                        
                        tokens = del_sw(tokens.replace(token_2, ""))
                
                        break
                break


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "회사에서 %s 으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "회사에서 %s 으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "회사에서 %s 으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "회사에서 %s 으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':1,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 2
        for i in tokens.split():
            token_3 = i
            token_3_mean = token_3
            object_3 = "회사명"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "회사에서 %s 으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "회사에서 %s 으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':word_num,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_73(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        
        for i in ["상여금", "상여"]:
            if text_pre.startswith(i):
                token_1 = i
                if i == "상여":
                    token_1_mean = token_1+"금"
                object_1 = "금융용어"
            
                tokens = del_sw(text_pre.replace(token_1, ""))
                break
                
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_74(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        for i in ["근로수당", "근무수당"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"

                tokens = del_sw(text_pre.replace(token_2, ""))
                break
            
            
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_75(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        
        token_1 = "방과후"
        token_1_mean = token_1+"수업비"
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_1, ""))
        
        


        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            if token_2.endswith(("초", "고")):
                token_2_mean = token_2+"등학교"
                object_2 = "학교명"
            elif token_2.endswith(("초등", "중")):
                token_2_mean = token_2+"학교"
                object_2 = "학교명"
            elif token_2.endswith(("비", "료")):
                token_2_mean = token_2
                object_2 = "교육비"
            else:
                token_2_mean = token_2
                object_2 = "알수없음"    
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_76(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_2 = "유치원"
        token_2_mean = token_2
        object_2 = "기관명"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "건물명"

        
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_77(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        token_1 = text_pre[0:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        names = find_name(text_pre)
        tokens = text_pre.replace(token_1, "")

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in names:
            token_2 = i
            token_2_mean = "이름"
            object_2 = "이름"
            tokens = tokens.replace(token_2, "")
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        for i in del_sw(tokens).split():
            token_3 = i
            token_3_mean = token_3
            object_3 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_3,
                                    '단어일련번호':word_num,
                                    '단어의미':token_3_mean,
                                    '개체명': object_3,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_78(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        for i in ["정기예금", "일반예금", "적립예금"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"
        
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "은행명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)

            
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_79(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        for i in ede_word_for_contains.split("|"):
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "금융용어"
                break
        
        
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            if token_1.endswith(("초", "고")):
                token_1_mean = token_1+"등학교"
                object_1 = "학교명"
            elif token_1.endswith(("초등", "중")):
                token_1_mean = token_1+"학교"
                object_1 = "학교명"
            elif token_1.endswith(("비", "료")):
                token_1_mean = token_1
                object_1 = "교육비"
            else:
                token_1_mean = token_1
                object_1 = "알수없음"  
                
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s를(을) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s를(을) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s를(을) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s를(을) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_80(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        for i in ["명절급여", "정기급여", "정산급여", "직원급여", "개인급여"]:
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = token_1
                object_1 = "금융용어"
                
                tokens = del_sw(text_pre.replace(token_1, ""))

                break


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_80_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        for i in ["월급여", "월급"]:
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = token_1
                object_1 = "금융용어"
                
                tokens = del_sw(text_pre.replace(token_1, ""))
                break

            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_80_2(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_2 = "월급"
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))


        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_80_3(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "급여"
        token_1_mean = token_1
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_1, " "))
        
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = i
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "급여를 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_81(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        lists = ["시각복지관", "실버복지관", "노인복지관", "장애인복지관", \
                "노인종합복지관", "장애인복합복지관", "사회복지관", \
                "종합사회복지관", "종합복지관"]

        for i in lists:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "시설명"
                
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "지역명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_81_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_2 = "복지관"
        token_2_mean = token_2
        object_2 = "시설명"
        
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "지역명" 
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_82(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "성과급"
        token_1_mean = token_1
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_1, ""))



        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_83(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        for i in ["천주교회", "중앙교회", "교회"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "종교단체"
                
                tokens = del_sw(text_pre.replace(token_2, ""))

                break
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "단체/건물이름"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금받은 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금받은 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_84(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_3 = "협회"
        token_3_mean = "협회"
        object_3 = "협회"
        
        
        tokens = del_sw(text_pre.replace(token_3, ""))

        token_2 = ""
        token_2_mean = ""
        for i in ["평화", "문화", "보호", "복지", "장애인", \
                "교육", "미용", "외식업", "산업", "척수", \
                "주선", "개별화물", "봉사", "숙박"]:
            if tokens.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "협회명"
                tokens = del_sw(tokens.replace(token_2, ""))
                break
                
    
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "단체명"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if token_2 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_85(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "삼성금융"
        token_1_mean = token_1
        object_1 = "금융사명"
        
        tokens = del_sw(text_pre.replace(token_1, ""))


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "지역명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_86(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = text_pre[0:3]
        token_1_mean = inco_comp_dict.get(token_1, token_1)
        object_1 = "법인명"
        
        tokens = del_sw(text_pre[3:])


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "회사명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
        
            word_num += 1
            
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_87(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "대출소개"
        token_1_mean = "대출소개비"
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_1, ""))


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "이름"
        
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_88(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "중진공"
        token_1_mean = "중소벤처기업진흥공단"
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_1, ""))


        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_89(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        lists = ["야근수당", "연구수당", "업무수당", "직무수당", \
                "특별수당", "연수수당", "강의수당", "관리수당", \
                "직책수당", "참석수당", "교육수당", "복지수당"]
        for i in lists:
            if text_pre.endswith(i):
                
                token_2 = i    
                token_2_mean = token_2
                object_2 = "금융용어"
                                  
                tokens = del_sw(text_pre.replace(token_2, ""))
                break

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "기관및단체"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s을(를) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s을(를) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s을(를) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s을(를) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df

    
    
def case_89_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        tokens = del_sw(text_pre)


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "금융용어"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "특정수당 을(를) 입금된 내역의 적요이다." if tran_diff == "입금" else "특정수당 을(를) 이체한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_89_2(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        token_2 = "수당"
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s을(를) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s을(를) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s을(를) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s을(를) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_90(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "ＣＪ"
        token_1_mean = "CJ"
        object_1 = "회사명"
        
        tokens = del_sw(text_pre.replace(token_1, ""))


            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "지점명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_91(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "DLIVE"
        token_1_mean = token_1+" 구독료"
        object_1 = "플랫폼명"
        
        tokens = del_sw(text_pre.replace(token_1, ""))


            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "지역명"
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_92(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_2 = "청약"
        token_2_mean = "청약"
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_2, ""))
        
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"

                
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_93(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        for i in ["세액", "월세"]:
            if text_pre.endswith(i):
                token_2 = i
                if i == "세액":
                    token_2_mean = "세액공제"
                else:
                    token_2_mean = "월세"
                object_2 = "금융용어"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
            
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_94(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        for i in ["교통비", "교통"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = "교통비"
                object_2 = "금융용어"
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
            
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_94_1(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        token_1 = "교통비"
        token_1_mean = "교통비"
        object_1 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_1, ""))

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            object_2 = "알수없음"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_1_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_95(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        for i in ["연말정산환급금", "연말정산환급", "연말정산", "연말"]:
            if text_pre.endswith(i):
                token_2 = i
                if "환급" in i: 
                    token_2_mean = "연말정산환급금"
                else:
                    token_2_mean = "연말정산"
                object_2 = "금융용어"
                
                tokens = del_sw(text_pre.replace(token_2, ""))
                break

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_96(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        tokens = del_sw(text_pre)

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "카드결제회사"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "급여가 입금된 내역의 적요이다." if tran_diff == "입금" else "카드결제를 이용한 내역의 적요이다.",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_97(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        token_2 = "매도"
        token_2_mean = "매도"
        object_2 = "금융용어"

        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "주식상품명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "주식상품을 매도하여 입금된 내역의 적요이다." if tran_diff == "입금" else "에러",
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "주식상품을 매도하여 입금된 내역의 적요이다." if tran_diff == "입금" else "에러",
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_98(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']


        for i in ["용돈", "세배돈", "곗돈", "갯돈", "세뱃돈", "목돈"]:
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = i
                object_2 = "금융용어"

                tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            if tran_diff == "입금":
                object_1 = "보낸사람"
            else:
                object_1 = "받는사람"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
            
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%token_2_mean if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%token_2_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_99(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_2 = "1회"
        token_2_mean = token_2
        object_2 = "입금/지급횟수"
        
        tokens = del_sw(text_pre.replace("0회", ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "알수없음"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 이체한 내역의 적요이다."%(token_2_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 이체한 내역의 적요이다."%(token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_100(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        
        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        tokens = del_sw(text_pre.replace(token_1, ""))
        
        token_3 = "계"
        token_3_mean = "곗돈"
        object_3 = "금융용어"
        tokens = del_sw(text_pre.replace(token_3, ""))

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_3_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_1,
                                '단어일련번호':0,
                                '단어의미':token_1_mean,
                                '개체명': object_1,
                                '완료여부':1,
                                }, ignore_index=True)

                
    
        word_num = 1
        for i in tokens.split():
            token_2 = i
            token_2_mean = token_2
            if tran_diff == "입금":
                object_2 = "보낸사람"
            else:
                object_2 = "받는사람"
            
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_3_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_3_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_101(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        for i in inco_comp_dict.keys():
            if i in text_pre:
                token_2 = i
                token_2_mean = inco_comp_dict.get(token_2, token_2)
                object_2 = "법인명"
                tokens = del_sw(text_pre.replace(token_2, ""))
                break
            
        text_mean = list()
        if any(word in tran_code for word in ["급여", "대량"]):
            # 0: 입금 # 1: 출금
            text_mean.append("회사에서 급여가 입금된 내역의 적요이다.")
            text_mean.append("급여 이체한 내역의 적요이다.")
        else:
            # 0: 입금 # 1: 출금
            text_mean.append("회사에서 입금된 내역의 적요이다.")
            text_mean.append("회사에 이체한 내역의 적요이다.")
            
        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "회사명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': text_mean[0] if tran_diff == "입금" else text_mean[1],
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean[0] if tran_diff == "입금" else text_mean[1],
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_102(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        token_2 = "재료"
        token_2_mean = "재료비"
        object_2 = "금융용어"
        tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_103(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        

        for i in grou_word_for_contains.split("|"):
            if text_pre.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "모임종류"
                tokens = del_sw(text_pre.replace(token_2, ""))

        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "모임이름"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 에서(에) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s 에서(에) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_2,
                                '단어일련번호':word_num,
                                '단어의미':token_2_mean,
                                '개체명': object_2,
                                '완료여부':1,
                                }, ignore_index=True)
        

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_104(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_3 = "상환"
        token_3_mean = token_3
        object_3 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_3, ""))

        token_2 = ""
        token_2_mean = token_2
        for i in ["중복", "원금", "차용", "대여금", "부채", "금전대차", "차입금", "주담대", "대출금", "원리금", "대출"]:
            if tokens.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "상환종류"
                tokens = del_sw(tokens.replace(token_2, ""))
                break


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "은행명/상환사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if token_2 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_105(path):
    ### input: DataFrame
    ### output: DataFrame
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df.reset_index(drop=True, inplace=True)
    new_df = pd.DataFrame()
    for i in tqdm(range(len(df))):
        text_pre = df.iloc[i]["적요_pre"]
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        token_3 = "이체"
        token_3_mean = token_3
        object_3 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_3, ""))

        token_2 = ""
        token_2_mean = token_2
        for i in ["상여", "자동", "정기", "대량", "일반", "입금", "적금", "대출이자", "CMA"]:
            if tokens.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "이체종류"
                tokens = del_sw(tokens.replace(token_2, ""))
                break


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "은행명/상환사유"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_1,
                                    '단어일련번호':word_num,
                                    '단어의미':token_1_mean,
                                    '개체명': object_1,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        if token_2 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': token_2,
                                    '단어일련번호':word_num,
                                    '단어의미':token_2_mean,
                                    '개체명': object_2,
                                    '완료여부':1,
                                    }, ignore_index=True)
            word_num += 1
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "%s%s 으로(로) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s 으로(로) 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': token_3,
                                '단어일련번호':word_num,
                                '단어의미':token_3_mean,
                                '개체명': object_3,
                                '완료여부':1,
                                }, ignore_index=True)

    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "../result/dataset/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df

if __name__ == "__main__":
    # split_data("./data/alldata.csv")
    case_1("../data/dataset/case/case_1.csv")
    case_1_1("../data/dataset/case/case_1_1.csv")
    case_2("../data/dataset/case/case_2.csv")
    case_3("../data/dataset/case/case_3.csv")
    case_4("../data/dataset/case/case_4.csv")
    case_5("../data/dataset/case/case_5.csv")
    case_6("../data/dataset/case/case_6.csv")
    case_7("../data/dataset/case/case_7.csv")
    case_8("../data/dataset/case/case_8.csv")
    case_9("../data/dataset/case/case_9.csv")
    case_10("../data/dataset/case/case_10.csv")
    case_10_1("../data/dataset/case/case_10_1.csv")
    case_10_2("../data/dataset/case/case_10_2.csv")
    case_11("../data/dataset/case/case_11.csv")
    case_12("../data/dataset/case/case_12.csv")
    case_13("../data/dataset/case/case_13.csv")
    case_14("../data/dataset/case/case_14.csv")
    case_15("../data/dataset/case/case_15.csv")
    case_16("../data/dataset/case/case_16.csv")
    case_17("../data/dataset/case/case_17.csv")
    case_18("../data/dataset/case/case_18.csv")
    case_19("../data/dataset/case/case_19.csv")
    case_20("../data/dataset/case/case_20.csv")
    case_21("../data/dataset/case/case_21.csv")
    case_21_1("../data/dataset/case/case_21_1.csv")
    case_22("../data/dataset/case/case_22.csv")
    case_23("../data/dataset/case/case_23.csv")
    case_24("../data/dataset/case/case_24.csv")
    case_25("../data/dataset/case/case_25.csv")
    case_26("../data/dataset/case/case_26.csv")
    case_27("../data/dataset/case/case_27.csv")
    case_27_1("../data/dataset/case/case_27_1.csv")
    case_28("../data/dataset/case/case_28.csv")
    case_29("../data/dataset/case/case_29.csv")
    case_30("../data/dataset/case/case_30.csv")
    case_31("../data/dataset/case/case_31.csv")
    case_32("../data/dataset/case/case_32.csv")
    case_33("../data/dataset/case/case_33.csv")
    case_34("../data/dataset/case/case_34.csv")
    case_35("../data/dataset/case/case_35.csv")
    case_36("../data/dataset/case/case_36.csv")
    case_37("../data/dataset/case/case_37.csv")
    case_38("../data/dataset/case/case_38.csv")
    case_39("../data/dataset/case/case_39.csv")
    case_39_1("../data/dataset/case/case_39_1.csv")
    case_40("../data/dataset/case/case_40.csv")
    case_41("../data/dataset/case/case_41.csv")
    case_41_1("../data/dataset/case/case_41_1.csv")
    case_42("../data/dataset/case/case_42.csv")
    case_43("../data/dataset/case/case_43.csv")
    case_43_1("../data/dataset/case/case_43_1.csv")
    case_44("../data/dataset/case/case_44.csv")
    case_45("../data/dataset/case/case_45.csv")
    case_46("../data/dataset/case/case_46.csv")
    case_47("../data/dataset/case/case_47.csv")
    case_48("../data/dataset/case/case_48.csv")
    case_49("../data/dataset/case/case_49.csv")
    case_50("../data/dataset/case/case_50.csv")
    case_51("../data/dataset/case/case_51.csv")
    case_52("../data/dataset/case/case_52.csv")
    case_53("../data/dataset/case/case_53.csv")
    case_54("../data/dataset/case/case_54.csv")
    case_55("../data/dataset/case/case_55.csv")
    case_55_1("../data/dataset/case/case_55_1.csv")
    case_56("../data/dataset/case/case_56.csv")
    case_57("../data/dataset/case/case_57.csv")
    case_58("../data/dataset/case/case_58.csv")
    case_59("../data/dataset/case/case_59.csv")
    case_60("../data/dataset/case/case_60.csv")
    case_61("../data/dataset/case/case_61.csv")
    case_62("../data/dataset/case/case_62.csv")
    case_63("../data/dataset/case/case_63.csv")
    case_64("../data/dataset/case/case_64.csv")
    case_65("../data/dataset/case/case_65.csv")
    case_66("../data/dataset/case/case_66.csv")
    case_67("../data/dataset/case/case_67.csv")
    case_67_1("../data/dataset/case/case_67_1.csv")
    case_68("../data/dataset/case/case_68.csv")
    case_69("../data/dataset/case/case_69.csv")
    case_69_1("../data/dataset/case/case_69_1.csv")
    case_69_2("../data/dataset/case/case_69_2.csv")
    case_70("../data/dataset/case/case_70.csv")
    case_71("../data/dataset/case/case_71.csv")
    case_72("../data/dataset/case/case_72.csv")
    case_73("../data/dataset/case/case_73.csv")
    case_74("../data/dataset/case/case_74.csv")
    case_75("../data/dataset/case/case_75.csv")
    case_76("../data/dataset/case/case_76.csv")
    case_77("../data/dataset/case/case_77.csv")
    case_78("../data/dataset/case/case_78.csv")
    case_79("../data/dataset/case/case_79.csv")
    case_80("../data/dataset/case/case_80.csv")
    case_80_1("../data/dataset/case/case_80_1.csv")
    case_80_2("../data/dataset/case/case_80_2.csv")
    case_80_3("../data/dataset/case/case_80_3.csv")
    case_81("../data/dataset/case/case_81.csv")
    case_81_1("../data/dataset/case/case_81_1.csv")
    case_82("../data/dataset/case/case_82.csv")
    case_83("../data/dataset/case/case_83.csv")
    case_84("../data/dataset/case/case_84.csv")
    case_85("../data/dataset/case/case_85.csv")
    case_86("../data/dataset/case/case_86.csv")
    case_87("../data/dataset/case/case_87.csv")
    case_88("../data/dataset/case/case_88.csv")
    case_89("../data/dataset/case/case_89.csv")
    case_89_1("../data/dataset/case/case_89_1.csv")
    case_89_2("../data/dataset/case/case_89_2.csv")
    case_90("../data/dataset/case/case_90.csv")
    case_91("../data/dataset/case/case_91.csv")
    case_92("../data/dataset/case/case_92.csv")
    case_93("../data/dataset/case/case_93.csv")
    case_94("../data/dataset/case/case_94.csv")
    case_94_1("../data/dataset/case/case_94_1.csv")
    case_95("../data/dataset/case/case_95.csv")
    case_96("../data/dataset/case/case_96.csv")
    case_97("../data/dataset/case/case_97.csv")
    case_98("../data/dataset/case/case_98.csv")
    case_99("../data/dataset/case/case_99.csv")
    case_100("../data/dataset/case/case_100.csv")
    case_101("../data/dataset/case/case_101.csv")
    case_102("../data/dataset/case/case_102.csv")
    case_103("../data/dataset/case/case_103.csv")
    case_104("../data/dataset/case/case_104.csv")
    case_105("../data/dataset/case/case_105.csv")
