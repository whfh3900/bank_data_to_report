import pandas as pd
from tqdm import tqdm
import os
tqdm.pandas()
from utils import *
import sys


def case_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_1_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_2(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_3(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_4(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_5(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_6(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_7(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_8(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_9(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_10(path, output_path):
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
        for i in bank_dict.keys():
            if text_pre.startswith(i):
                token_1 = i
                token_1_mean = bank_dict.get(token_1, token_1)
                object_1 = "은행명"
                tokens = del_sw(tokens.replace(token_1, ""))
                break
            
            
        for i in insu_word_for_contains.split("|"):
            if i in tokens:
                token_3 = i
                token_3_mean = token_3
                object_3 = "보험명/금융용어"
                
                tokens = del_sw(tokens.replace(token_3, " "))
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
                                    '적요 설명': "%s 계좌에서 %s 으로(로) 입금된 내역의 적요이다."%(token_1_mean, token_3_mean) if tran_diff == "입금" else "%s 계좌로 %s 으로(로) 이체한 내역의 적요이다."%(token_1_mean, token_3_mean),
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_10_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_10_2(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_11(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_12(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_13(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df
        
        
def case_14(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_15(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_16(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_17(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_18(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_19(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_20(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_21(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_21_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_22(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_23(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_24(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_25(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_26(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_27(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_27_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_28(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_29(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_30(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_31(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_32(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_33(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_34(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_35(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




# def case_36(path, output_path):
#     ### input: DataFrame
#     ### output: DataFrame
#     df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
#     df.reset_index(drop=True, inplace=True)
#     new_df = pd.DataFrame()
#     for i in tqdm(range(len(df))):
#         text_pre = df.iloc[i]["적요_pre"]
#         num = df.iloc[i]['확인용']
#         text = df.iloc[i]['적요']
#         text_num = df.iloc[i]['적요일련번호']
#         tran_diff = df.iloc[i]['입출금구분']
#         data_sour = df.iloc[i]['데이터셋출처']
#         sour_num = df.iloc[i]['출처번호']
#         text_stru = df.iloc[i]['적요구조']
#         text_stru_num = df.iloc[i]['적요구조일련번호']
#         # text_mean = df.iloc[i]['적요 설명']
#         tran_code = df.iloc[i]['거래코드']
#         clas = df.iloc[i]['분류']
#         clas_num = df.iloc[i]['분류번호']
#         min_amou = df.iloc[i]['최소금액']
#         max_amou = df.iloc[i]['최대금액']
        
#         tokens = re.split(r'-|－', text_pre)
#         token_1 = tokens[0]
#         token_1_mean = bank_dict.get(token_1, token_1)
#         object_1 = "은행명"
        
#         names = find_name(tokens[-1])
#         tokens = tokens[-1]
        
#         new_df = new_df.append({'확인용': num,
#                                 '적요': text,
#                                 '적요일련번호': text_num,
#                                 '입출금구분': tran_diff,
#                                 '데이터셋출처': data_sour,
#                                 '출처번호': sour_num,
#                                 '적요구조': text_stru,
#                                 '적요구조일련번호': text_stru_num,
#                                 '적요 설명': "%s 계좌에서 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 이체한 내역의 적요이다."%token_1_mean,
#                                 '거래코드': tran_code,
#                                 '분류': clas,
#                                 '분류번호': clas_num,
#                                 '최소금액': min_amou,
#                                 '최대금액': max_amou,
#                                 '단어': token_1,
#                                 '단어일련번호':0,
#                                 '단어의미':token_1_mean,
#                                 '개체명': object_1,
#                                 '완료여부':1,
#                                 }, ignore_index=True)
        
#         word_num = 1
#         for i in names:
#             token_2 = i
#             token_2_mean = "이름"
#             object_2 = "이름"
#             tokens = tokens.replace(token_2, "")
#             new_df = new_df.append({'확인용': num,
#                                     '적요': text,
#                                     '적요일련번호': text_num,
#                                     '입출금구분': tran_diff,
#                                     '데이터셋출처': data_sour,
#                                     '출처번호': sour_num,
#                                     '적요구조': text_stru,
#                                     '적요구조일련번호': text_stru_num,
#                                     '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
#                                     '거래코드': tran_code,
#                                     '분류': clas,
#                                     '분류번호': clas_num,
#                                     '최소금액': min_amou,
#                                     '최대금액': max_amou,
#                                     '단어': token_2,
#                                     '단어일련번호':word_num,
#                                     '단어의미':token_2_mean,
#                                     '개체명': object_2,
#                                     '완료여부':1,
#                                     }, ignore_index=True)
#             word_num +=1
#         tokens = re.sub(r'[^\w\s]', ' ', tokens)
#         for i in tokens.split():
#             token_3 = i
#             token_3_mean = token_3
#             object_3 = "알수없음"
#             new_df = new_df.append({'확인용': num,
#                                     '적요': text,
#                                     '적요일련번호': text_num,
#                                     '입출금구분': tran_diff,
#                                     '데이터셋출처': data_sour,
#                                     '출처번호': sour_num,
#                                     '적요구조': text_stru,
#                                     '적요구조일련번호': text_stru_num,
#                                     '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
#                                     '거래코드': tran_code,
#                                     '분류': clas,
#                                     '분류번호': clas_num,
#                                     '최소금액': min_amou,
#                                     '최대금액': max_amou,
#                                     '단어': token_3,
#                                     '단어일련번호':word_num,
#                                     '단어의미':token_3_mean,
#                                     '개체명': object_3,
#                                     '완료여부':1,
#                                     }, ignore_index=True)
#             word_num += 1
            
        
#     result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    
#     result_path = os.path.join(output_path, result_file_name)
#     new_df.to_csv(result_path, encoding="utf-8-sig")
#     return new_df




def case_37(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_38(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_39(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_39_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_40(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_41(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_41_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_42(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_43(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_43_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_44(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_45(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_46(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



##  나중에
def case_47(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_48(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_49(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_50(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_51(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_52(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_53(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_54(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_55(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_55_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_56(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_57(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_58(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_59(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_60(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_61(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_62(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_63(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_64(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_65(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_66(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_67(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_67_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_68(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_69(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_69_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_69_2(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_70(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_71(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df







def case_72(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_73(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_74(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_75(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_76(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





# def case_77(path, output_path):
#     ### input: DataFrame
#     ### output: DataFrame
#     df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
#     df.reset_index(drop=True, inplace=True)
#     new_df = pd.DataFrame()
#     for i in tqdm(range(len(df))):
#         text_pre = df.iloc[i]["적요_pre"]
#         num = df.iloc[i]['확인용']
#         text = df.iloc[i]['적요']
#         text_num = df.iloc[i]['적요일련번호']
#         tran_diff = df.iloc[i]['입출금구분']
#         data_sour = df.iloc[i]['데이터셋출처']
#         sour_num = df.iloc[i]['출처번호']
#         text_stru = df.iloc[i]['적요구조']
#         text_stru_num = df.iloc[i]['적요구조일련번호']
#         # text_mean = df.iloc[i]['적요 설명']
#         tran_code = df.iloc[i]['거래코드']
#         clas = df.iloc[i]['분류']
#         clas_num = df.iloc[i]['분류번호']
#         min_amou = df.iloc[i]['최소금액']
#         max_amou = df.iloc[i]['최대금액']

#         token_1 = text_pre[0:2]
#         token_1_mean = bank_dict.get(token_1, token_1)
#         object_1 = "은행명"
        
#         names = find_name(text_pre)
#         tokens = text_pre.replace(token_1, "")

#         new_df = new_df.append({'확인용': num,
#                                 '적요': text,
#                                 '적요일련번호': text_num,
#                                 '입출금구분': tran_diff,
#                                 '데이터셋출처': data_sour,
#                                 '출처번호': sour_num,
#                                 '적요구조': text_stru,
#                                 '적요구조일련번호': text_stru_num,
#                                 '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
#                                 '거래코드': tran_code,
#                                 '분류': clas,
#                                 '분류번호': clas_num,
#                                 '최소금액': min_amou,
#                                 '최대금액': max_amou,
#                                 '단어': token_1,
#                                 '단어일련번호':0,
#                                 '단어의미':token_1_mean,
#                                 '개체명': object_1,
#                                 '완료여부':1,
#                                 }, ignore_index=True)
#         word_num = 1
#         for i in names:
#             token_2 = i
#             token_2_mean = "이름"
#             object_2 = "이름"
#             tokens = tokens.replace(token_2, "")
#             new_df = new_df.append({'확인용': num,
#                                     '적요': text,
#                                     '적요일련번호': text_num,
#                                     '입출금구분': tran_diff,
#                                     '데이터셋출처': data_sour,
#                                     '출처번호': sour_num,
#                                     '적요구조': text_stru,
#                                     '적요구조일련번호': text_stru_num,
#                                     '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
#                                     '거래코드': tran_code,
#                                     '분류': clas,
#                                     '분류번호': clas_num,
#                                     '최소금액': min_amou,
#                                     '최대금액': max_amou,
#                                     '단어': token_2,
#                                     '단어일련번호':word_num,
#                                     '단어의미':token_2_mean,
#                                     '개체명': object_2,
#                                     '완료여부':1,
#                                     }, ignore_index=True)
#             word_num += 1

#         for i in del_sw(tokens).split():
#             token_3 = i
#             token_3_mean = token_3
#             object_3 = "알수없음"
#             new_df = new_df.append({'확인용': num,
#                                     '적요': text,
#                                     '적요일련번호': text_num,
#                                     '입출금구분': tran_diff,
#                                     '데이터셋출처': data_sour,
#                                     '출처번호': sour_num,
#                                     '적요구조': text_stru,
#                                     '적요구조일련번호': text_stru_num,
#                                     '적요 설명': token_1_mean+" 계좌에서 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 이체한 내역의 적요이다.",
#                                     '거래코드': tran_code,
#                                     '분류': clas,
#                                     '분류번호': clas_num,
#                                     '최소금액': min_amou,
#                                     '최대금액': max_amou,
#                                     '단어': token_3,
#                                     '단어일련번호':word_num,
#                                     '단어의미':token_3_mean,
#                                     '개체명': object_3,
#                                     '완료여부':1,
#                                     }, ignore_index=True)
#             word_num += 1
            
            
#     result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    
#     result_path = os.path.join(output_path, result_file_name)
#     new_df.to_csv(result_path, encoding="utf-8-sig")
#     return new_df




def case_78(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_79(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_80(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_80_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_80_2(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_80_3(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_81(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_81_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_82(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_83(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_84(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_85(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_86(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_87(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_88(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_89(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df

    
    
def case_89_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_89_2(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_90(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_91(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_92(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_93(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_94(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_94_1(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_95(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_96(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_97(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_98(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_99(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_100(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_101(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_102(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_103(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_104(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_105(path, output_path):
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_106(path, output_path):
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
        

        token_3 = "정산"
        token_3_mean = token_3
        object_3 = "금융용어"
        
        tokens = del_sw(text_pre.replace(token_3, ""))
        
        token_2 = ""
        token_2_mean = ""
        object_2 = ""
        for i in fina_word_for_contains.split("|"):
            if tokens.endswith(i):
                token_2 = i
                token_2_mean = token_2
                object_2 = "정산명"
                tokens = del_sw(tokens.replace(token_2, ""))
                break


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "날짜/회사명"

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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


def case_107(path, output_path):
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
        
        
        for i in ["초등", "고등"]:
            if text_pre.endswith(i):
                token_3 = i
                token_3_mean = token_3+"학교"
                object_3 = "학교"
        
                tokens = del_sw(text_pre.replace(token_3, ""))
                break

        token_2 = ""
        token_2_mean = "교육비"
        object_2 = ""
        for i in scho_word_for_contains.split("|"):
            if i in tokens:
                token_2 = i
                if i.endswith("비"):
                    token_2_mean = token_2
                else:
                    token_2_mean = token_2+"비"
                object_2 = "비용명"
                tokens = del_sw(tokens.replace(token_2, " "))
                break


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "숫자단위/학교명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 으로(로) %s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s 으로(로) %s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
                                    '적요 설명': "%s 으로(로) %s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s 으로(로) %s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
                                '적요 설명': "%s 으로(로) %s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s 으로(로) %s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_108(path, output_path):
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
        
        
        for i in ["연합", "조합"]:
            if text_pre.endswith(i):
                token_3 = i
                token_3_mean = token_3
                object_3 = "그룹/단체"
        
                tokens = del_sw(text_pre.replace(token_3, ""))
                break

        token_2 = ""
        token_2_mean = ""
        for i in unio_word_for_contains.split("|"):
            if i in tokens:
                token_2 = i
                token_2_mean = token_2
                object_2 = "그룹종류"
                tokens = del_sw(tokens.replace(token_2, " "))
                break


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = bank_dict.get(token_1, token_1)
            object_1 = "그룹명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
                                    '적요 설명': "%s%s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
                                '적요 설명': "%s%s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



def case_109(path, output_path):
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
        

        token_2 = "정수기"
        token_2_mean = "정수기"
        object_2 = "회사업종"
        
        token_1 = del_sw(text_pre.replace(token_2, ""))
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
                                '적요 설명': "%s 비용으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 비용으로(로) 이체한 내역의 적요이다."%(token_2_mean),
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
        if token_2 != "":
            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s 비용으로(로) 입금된 내역의 적요이다."%(token_2_mean) if tran_diff == "입금" else "%s 비용으로(로) 이체한 내역의 적요이다."%(token_2_mean),
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_110(path, output_path):
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
        
        
        token_3 = "센터"
        token_3_mean = token_3
        object_3 = "건물"

        tokens = del_sw(text_pre.replace(token_3, ""))

        token_2 = ""
        token_2_mean = ""
        for i in cent_word_for_contains.split("|"):
            if i in tokens:
                token_2 = i
                token_2_mean = token_2
                object_2 = "센터종류"
                tokens = del_sw(tokens.replace(token_2, ""))
                break


        word_num = 0
        for i in tokens.split():
            token_1 = i
            token_1_mean = token_1
            object_1 = "센터명"

            new_df = new_df.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': "%s%s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
                                    '적요 설명': "%s%s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
                                '적요 설명': "%s%s에서(에) 입금된 내역의 적요이다."%(token_2_mean, token_3_mean) if tran_diff == "입금" else "%s%s에 이체한 내역의 적요이다."%(token_2_mean, token_3_mean),
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df




def case_111(path, output_path):
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
        
        
        for i in ["야식대", "중식대", "식대"]:
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
    
    result_path = os.path.join(output_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    case_1(os.path.join(input_path, "case_1.csv"), output_path)
    case_1_1(os.path.join(input_path, "case_1_1.csv"), output_path)
    case_2(os.path.join(input_path, "case_2.csv"), output_path)
    case_3(os.path.join(input_path, "case_3.csv"), output_path)
    case_4(os.path.join(input_path, "case_4.csv"), output_path)
    case_5(os.path.join(input_path, "case_5.csv"), output_path)
    case_6(os.path.join(input_path, "case_6.csv"), output_path)
    case_7(os.path.join(input_path, "case_7.csv"), output_path)
    case_8(os.path.join(input_path, "case_8.csv"), output_path)
    case_9(os.path.join(input_path, "case_9.csv"), output_path)
    case_10(os.path.join(input_path, "case_10.csv"), output_path)
    case_10_1(os.path.join(input_path, "case_10_1.csv"), output_path)
    case_10_2(os.path.join(input_path, "case_10_2.csv"), output_path)
    case_11(os.path.join(input_path, "case_11.csv"), output_path)
    case_12(os.path.join(input_path, "case_12.csv"), output_path)
    case_13(os.path.join(input_path, "case_13.csv"), output_path)
    case_14(os.path.join(input_path, "case_14.csv"), output_path)
    case_15(os.path.join(input_path, "case_15.csv"), output_path)
    case_16(os.path.join(input_path, "case_16.csv"), output_path)
    case_17(os.path.join(input_path, "case_17.csv"), output_path)
    case_18(os.path.join(input_path, "case_18.csv"), output_path)
    case_19(os.path.join(input_path, "case_19.csv"), output_path)
    case_20(os.path.join(input_path, "case_20.csv"), output_path)
    case_21(os.path.join(input_path, "case_21.csv"), output_path)
    case_21_1(os.path.join(input_path, "case_21_1.csv"), output_path)
    case_22(os.path.join(input_path, "case_22.csv"), output_path)
    case_23(os.path.join(input_path, "case_23.csv"), output_path)
    case_24(os.path.join(input_path, "case_24.csv"), output_path)
    case_25(os.path.join(input_path, "case_25.csv"), output_path)
    case_26(os.path.join(input_path, "case_26.csv"), output_path)
    case_27(os.path.join(input_path, "case_27.csv"), output_path)
    case_27_1(os.path.join(input_path, "case_27_1.csv"), output_path)
    case_28(os.path.join(input_path, "case_28.csv"), output_path)
    case_29(os.path.join(input_path, "case_29.csv"), output_path)
    case_30(os.path.join(input_path, "case_30.csv"), output_path)
    case_31(os.path.join(input_path, "case_31.csv"), output_path)
    case_32(os.path.join(input_path, "case_32.csv"), output_path)
    case_33(os.path.join(input_path, "case_33.csv"), output_path)
    case_34(os.path.join(input_path, "case_34.csv"), output_path)
    case_35(os.path.join(input_path, "case_35.csv"), output_path)
    # case_36(os.path.join(input_path, "case_36.csv"), output_path)
    case_37(os.path.join(input_path, "case_37.csv"), output_path)
    case_38(os.path.join(input_path, "case_38.csv"), output_path)
    case_39(os.path.join(input_path, "case_39.csv"), output_path)
    case_39_1(os.path.join(input_path, "case_39_1.csv"), output_path)
    case_40(os.path.join(input_path, "case_40.csv"), output_path)
    case_41(os.path.join(input_path, "case_41.csv"), output_path)
    case_41_1(os.path.join(input_path, "case_41_1.csv"), output_path)
    case_42(os.path.join(input_path, "case_42.csv"), output_path)
    case_43(os.path.join(input_path, "case_43.csv"), output_path)
    case_43_1(os.path.join(input_path, "case_43_1.csv"), output_path)
    case_44(os.path.join(input_path, "case_44.csv"), output_path)
    case_45(os.path.join(input_path, "case_45.csv"), output_path)
    case_46(os.path.join(input_path, "case_46.csv"), output_path)
    case_47(os.path.join(input_path, "case_47.csv"), output_path)
    case_48(os.path.join(input_path, "case_48.csv"), output_path)
    case_49(os.path.join(input_path, "case_49.csv"), output_path)
    case_50(os.path.join(input_path, "case_50.csv"), output_path)
    case_51(os.path.join(input_path, "case_51.csv"), output_path)
    case_52(os.path.join(input_path, "case_52.csv"), output_path)
    case_53(os.path.join(input_path, "case_53.csv"), output_path)
    case_54(os.path.join(input_path, "case_54.csv"), output_path)
    case_55(os.path.join(input_path, "case_55.csv"), output_path)
    case_55_1(os.path.join(input_path, "case_55_1.csv"), output_path)
    case_56(os.path.join(input_path, "case_56.csv"), output_path)
    case_57(os.path.join(input_path, "case_57.csv"), output_path)
    case_58(os.path.join(input_path, "case_58.csv"), output_path)
    case_59(os.path.join(input_path, "case_59.csv"), output_path)
    case_60(os.path.join(input_path, "case_60.csv"), output_path)
    case_61(os.path.join(input_path, "case_61.csv"), output_path)
    case_62(os.path.join(input_path, "case_62.csv"), output_path)
    case_63(os.path.join(input_path, "case_63.csv"), output_path)
    case_64(os.path.join(input_path, "case_64.csv"), output_path)
    case_65(os.path.join(input_path, "case_65.csv"), output_path)
    case_66(os.path.join(input_path, "case_66.csv"), output_path)
    case_67(os.path.join(input_path, "case_67.csv"), output_path)
    case_67_1(os.path.join(input_path, "case_67_1.csv"), output_path)
    case_68(os.path.join(input_path, "case_68.csv"), output_path)
    case_69(os.path.join(input_path, "case_69.csv"), output_path)
    case_69_1(os.path.join(input_path, "case_69_1.csv"), output_path)
    case_69_2(os.path.join(input_path, "case_69_2.csv"), output_path)
    case_70(os.path.join(input_path, "case_70.csv"), output_path)
    case_71(os.path.join(input_path, "case_71.csv"), output_path)
    case_72(os.path.join(input_path, "case_72.csv"), output_path)
    case_73(os.path.join(input_path, "case_73.csv"), output_path)
    case_74(os.path.join(input_path, "case_74.csv"), output_path)
    case_75(os.path.join(input_path, "case_75.csv"), output_path)
    case_76(os.path.join(input_path, "case_76.csv"), output_path)
    # case_77(os.path.join(input_path, "case_77.csv"), output_path)
    case_78(os.path.join(input_path, "case_78.csv"), output_path)
    case_79(os.path.join(input_path, "case_79.csv"), output_path)
    case_80(os.path.join(input_path, "case_80.csv"), output_path)
    case_80_1(os.path.join(input_path, "case_80_1.csv"), output_path)
    case_80_2(os.path.join(input_path, "case_80_2.csv"), output_path)
    case_80_3(os.path.join(input_path, "case_80_3.csv"), output_path)
    case_81(os.path.join(input_path, "case_81.csv"), output_path)
    case_81_1(os.path.join(input_path, "case_81_1.csv"), output_path)
    case_82(os.path.join(input_path, "case_82.csv"), output_path)
    case_83(os.path.join(input_path, "case_83.csv"), output_path)
    case_84(os.path.join(input_path, "case_84.csv"), output_path)
    case_85(os.path.join(input_path, "case_85.csv"), output_path)
    case_86(os.path.join(input_path, "case_86.csv"), output_path)
    case_87(os.path.join(input_path, "case_87.csv"), output_path)
    case_88(os.path.join(input_path, "case_88.csv"), output_path)
    case_89(os.path.join(input_path, "case_89.csv"), output_path)
    case_89_1(os.path.join(input_path, "case_89_1.csv"), output_path)
    case_89_2(os.path.join(input_path, "case_89_2.csv"), output_path)
    case_90(os.path.join(input_path, "case_90.csv"), output_path)
    case_91(os.path.join(input_path, "case_91.csv"), output_path)
    case_92(os.path.join(input_path, "case_92.csv"), output_path)
    case_93(os.path.join(input_path, "case_93.csv"), output_path)
    case_94(os.path.join(input_path, "case_94.csv"), output_path)
    case_94_1(os.path.join(input_path, "case_94_1.csv"), output_path)
    case_95(os.path.join(input_path, "case_95.csv"), output_path)
    case_96(os.path.join(input_path, "case_96.csv"), output_path)
    case_97(os.path.join(input_path, "case_97.csv"), output_path)
    case_98(os.path.join(input_path, "case_98.csv"), output_path)
    case_99(os.path.join(input_path, "case_99.csv"), output_path)
    case_100(os.path.join(input_path, "case_100.csv"), output_path)
    case_101(os.path.join(input_path, "case_101.csv"), output_path)
    case_102(os.path.join(input_path, "case_102.csv"), output_path)
    case_103(os.path.join(input_path, "case_103.csv"), output_path)
    case_104(os.path.join(input_path, "case_104.csv"), output_path)
    case_105(os.path.join(input_path, "case_105.csv"), output_path)
    case_106(os.path.join(input_path, "case_106.csv"), output_path)
    case_107(os.path.join(input_path, "case_107.csv"), output_path)
    case_108(os.path.join(input_path, "case_108.csv"), output_path)
    case_109(os.path.join(input_path, "case_109.csv"), output_path)
    case_110(os.path.join(input_path, "case_110.csv"), output_path)
    case_111(os.path.join(input_path, "case_111.csv"), output_path)
