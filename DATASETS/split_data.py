import pandas as pd
from utils import *
from tqdm import tqdm
tqdm.pandas()

def split_data(path):
    # path = "../data/우리은행/작업/공통/*.csv"
    # df = pd.DataFrame()
    # for path in glob(path):
    #     etc = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    #     df = pd.concat([df, etc], axis=0)
    # df_1 = df[df["완료여부"]==1].copy()
    # df_2 = df[df["완료여부"].isnull()].copy()


    # path = "../data/우리은행/작업/최승언/dataset16_4_최승언.csv"
    # df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    # df_1 = df[df["완료여부"]==1].copy()
    # df_2 = df[df["완료여부"].isnull()].copy()

    # one_text = df_1["적요"].value_counts()[df_1["적요"].value_counts()==1].index
    # df_1_1 = df_1[df_1["적요"].isin(one_text)].copy()
    # df_1_2 = df_1[~df_1["적요"].isin(one_text)].copy()


    # df = df[~df["확인용"].isnull()]
    # df = df.drop_duplicates(['확인용'])

    # path = "../data/우리은행/작업/공통/dataset_16.csv"
    # df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    # df = df[~df["확인용"].isnull()]
    # df = df.drop_duplicates(['확인용'])
    # df["적요 설명"] = ""
    # df["단어"] = ""
    # df["단어일련번호"] = ""
    # df["단어의미"] = ""
    # df["개체명"] = ""
    # df["완료여부"] = ""
    # df.to_csv("../data/우리은행/작업/오리지널/original.csv", encoding="utf-8-sig")


    # df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df = pd.read_csv(path, encoding="cp949", index_col=0)

    df["적요_pre"] = df["적요"].progress_apply(lambda x: process_text(x))
    df["적요길이"] = df["적요_pre"].progress_apply(lambda x: len([i for i in x if i not in (" ", "　", "-", "－", "_", "＿", "0", "．", "／", "(", ")")]))
    df["적요반대_pre"] = df["적요_pre"].progress_apply(lambda x: x[::-1])


    ################################################## v1
    ## 케이스 별로 나누자
    # 은행명으로 시작하고 2번째가 -로 시작하면서 길이가 5인 케이스
    case_1_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    (df["적요길이"]==5)].index.tolist()
    case_1 = df[df.index.isin(case_1_index)].copy()
    case_1.to_csv("../data/dataset/case/case_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_1_index)]
    


    # 2번째 또는 3번째가 청약으로 시작하는 케이스
    case_1_1_index = df[((df["적요_pre"].str[2:4]==("청약")) | 
                        (df["적요_pre"].str[3:5]==("청약")))].index.tolist()
    case_1_1 = df[df.index.isin(case_1_1_index)].copy()
    case_1_1.to_csv("../data/dataset/case/case_1_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_1_1_index)]
    
    
    # 은행명으로 시작하고 2번째가 -로 시작하면서 급여로 끝나는 케이스
    case_2_index = df[((df["적요_pre"].str.startswith(tuple(bank_dict.keys())))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    (df["적요_pre"].str.endswith("급여"))].index.tolist()
    case_2 = df[df.index.isin(case_2_index)].copy()
    case_2.to_csv("../data/dataset/case/case_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_2_index)]



    # 00 뒤에 월급여로 시작하고 길이가 8글자인 케이스
    case_3_index = df[(df["적요_pre"].str[2:5] == "월급여") & 
                    (df["적요길이"]==8)].index.tolist()
    case_3 = df[df.index.isin(case_3_index)].copy()
    case_3.to_csv("../data/dataset/case/case_3.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_3_index)]



    # 신한-신한으로 시작하는 케이스
    case_4_index = df[(df["적요_pre"].str.startswith("신한-신한"))].index.tolist()
    case_4 = df[df.index.isin(case_4_index)].copy()
    case_4.to_csv("../data/dataset/case/case_4.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_4_index)]



    # 은행명으로 시작하고 급여로 끝나면서 길이가 7 이상인 케이스
    case_5_index = df[((df["적요_pre"].str.startswith(tuple(bank_dict.keys())))) & 
                    (df["적요_pre"].str.endswith("급여")) &
                    (df["적요길이"]>6)].index.tolist()
    case_5 = df[df.index.isin(case_5_index)].copy()
    case_5.to_csv("../data/dataset/case/case_5.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_5_index)]



    # 은행명으로 시작하고 회사사용 단어가 들어있는 케이스
    case_6_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(comp_word_for_contains))].index.tolist()
    case_6 = df[df.index.isin(case_6_index)].copy()
    case_6.to_csv("../data/dataset/case/case_6.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_6_index)]



    # 국민-국민으로 시작하는 케이스
    case_7_index = df[(df["적요_pre"].str.startswith(("국민-국민", "국민－국민")))].index.tolist()
    case_7 = df[df.index.isin(case_7_index)].copy()
    case_7.to_csv("../data/dataset/case/case_7.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_7_index)]



    # 은행명으로 시작하고 저축관련 단어가 들어있는 케이스
    case_8_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(save_word_for_contains))].index.tolist()
    case_8 = df[df.index.isin(case_8_index)].copy()
    case_8.to_csv("../data/dataset/case/case_8.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_8_index)]



    # 은행명으로 시작하고 두번째가 -로 시작하고 교육관련 단어가 들어있는 케이스
    case_9_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) &
                    (df["적요_pre"].str.contains(ede_word_for_contains))].index.tolist()
    case_9 = df[df.index.isin(case_9_index)].copy()
    case_9.to_csv("../data/dataset/case/case_9.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_9_index)]



    # 은행명으로 시작하고 보험관련 단어가 뒤에 들어있는 케이스
    case_10_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(insu_word_for_contains))].index.tolist()
    case_10 = df[df.index.isin(case_10_index)].copy()
    case_10.to_csv("../data/dataset/case/case_10.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_10_index)]



    # 은행명으로 시작하고 주거관련 단어가 들어있는 케이스
    case_10_1_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(resi_word_for_contains))].index.tolist()
    case_10_1 = df[df.index.isin(case_10_1_index)].copy()
    case_10_1.to_csv("../data/dataset/case/case_10_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_10_1_index)]



    # 은행명으로 시작하고 대출관련 단어가 들어있는 케이스
    case_10_2_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(loan_word_for_contains))].index.tolist()
    case_10_2 = df[df.index.isin(case_10_2_index)].copy()
    case_10_2.to_csv("../data/dataset/case/case_10_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_10_2_index)]



    # 이름 3글자인 경우
    case_11_index = df[(df["적요길이"]==3) &
                       (df["적요_pre"].apply(lambda x: check_language(x))) & 
                       (~df["적요_pre"].str.endswith(("회","차","집","짐","여","약","비","료","급","금")))].index.tolist()
    case_11 = df[df.index.isin(case_11_index)].copy()
    case_11.to_csv("../data/dataset/case/case_11.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_11_index)]



    # 지역명으로 시작하고 길이가 5인 케이스
    case_12_index = df[(df["적요_pre"].str.startswith(tuple(place))) & 
                    (df["적요길이"]==5)].index.tolist()
    case_12 = df[df.index.isin(case_12_index)].copy()
    case_12.to_csv("../data/dataset/case/case_12.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_12_index)]



    # 0회, 00회, 000회로 시작하는 케이스
    case_13_index = df[(df["적요_pre"].str.startswith(("0회","00회","000회")))].index.tolist()
    case_13 = df[df.index.isin(case_13_index)].copy()
    case_13.to_csv("../data/dataset/case/case_13.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_13_index)]



    # 00금으로 끝나는 케이스
    case_14_index = df[(df["적요_pre"].str.endswith(tuple(goal_word_for_contains.split("|"))))].index.tolist()
    case_14 = df[df.index.isin(case_14_index)].copy()
    case_14.to_csv("../data/dataset/case/case_14.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_14_index)]



    # 세무법인으로 시작하거나 끝나는 케이스
    case_15_index = df[((df["적요_pre"].str.startswith("세무법인")) |
                    (df["적요_pre"].str.endswith("세무법인")))].index.tolist()
    case_15 = df[df.index.isin(case_15_index)].copy()
    case_15.to_csv("../data/dataset/case/case_15.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_15_index)]



    # 세무사로 시작하거나 끝나고 길이가 8이하 인 케이스
    case_16_index = df[((df["적요_pre"].str.endswith("세무사")) | 
                        (df["적요_pre"].str.startswith("세무사"))) & 
                    (df["적요길이"]<9)].index.tolist()
    case_16 = df[df.index.isin(case_16_index)].copy()
    case_16.to_csv("../data/dataset/case/case_16.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_16_index)]



    # 세무회계로 끝나거나 시작하고 길이가 5이상인 케이스
    case_17_index = df[((df["적요_pre"].str.endswith("세무회계")) | 
                        (df["적요_pre"].str.startswith("세무회계")))].index.tolist()
    case_17 = df[df.index.isin(case_17_index)].copy()
    case_17.to_csv("../data/dataset/case/case_17.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_17_index)]



    # 세무회계사로 끝나는 케이스
    case_18_index = df[df["적요_pre"].str.endswith("세무회계사")].index.tolist()
    case_18 = df[df.index.isin(case_18_index)].copy()
    case_18.to_csv("../data/dataset/case/case_18.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_18_index)]



    # 회계사로 끝나는 케이스
    case_19_index = df[df["적요_pre"].str.endswith("회계사")].index.tolist()
    case_19 = df[df.index.isin(case_19_index)].copy()
    case_19.to_csv("../data/dataset/case/case_19.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_19_index)]



    # 회계법인으로 끝나는 케이스
    case_20_index = df[(df["적요_pre"].str.endswith("회계법인"))].index.tolist()
    case_20 = df[df.index.isin(case_20_index)].copy()
    case_20.to_csv("../data/dataset/case/case_20.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_20_index)]



    # 급여이체, 급여입금, 급여지급으로 끝나는 케이스
    case_21_index = df[(df["적요_pre"].str.endswith(("급여이체", "급여입금", "급여지급", "급여수당"))) | 
                    (df["적요_pre"].str.startswith(("급여이체", "급여입금", "급여지급", "급여수당")))].index.tolist()
    case_21 = df[df.index.isin(case_21_index)].copy()
    case_21.to_csv("../data/dataset/case/case_21.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_21_index)]


    # 급여로 시작하거나 끝나고 길이가 4인 케이스
    case_21_1_index = df[(((df["적요_pre"].str.startswith("급여"))) | 
                        (df["적요_pre"].str.endswith("급여"))) &
                    (df["적요길이"]==4)].index.tolist()
    case_21_1 = df[df.index.isin(case_21_1_index)].copy()
    case_21_1.to_csv("../data/dataset/case/case_21_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_21_1_index)]


    # 세무그룹으로 시작하는 케이스
    case_22_index = df[(df["적요_pre"].str.startswith("세무그룹"))].index.tolist()
    case_22 = df[df.index.isin(case_22_index)].copy()
    case_22.to_csv("../data/dataset/case/case_22.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_22_index)]



    # 세무회로 끝나는 케이스
    case_23_index = df[(df["적요_pre"].str.endswith("세무회"))].index.tolist()
    case_23 = df[df.index.isin(case_23_index)].copy()
    case_23.to_csv("../data/dataset/case/case_23.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_23_index)]



    # 노무법인으로 시작하거나 끝나는 케이스
    case_24_index = df[(df["적요_pre"].str.startswith("노무법인")) | 
                    (df["적요_pre"].str.endswith("노무법인"))].index.tolist()
    case_24 = df[df.index.isin(case_24_index)].copy()
    case_24.to_csv("../data/dataset/case/case_24.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_24_index)]



    # SK쉴더스로 시작하는 케이스
    case_25_index = df[(df["적요_pre"].str.startswith("SK쉴더스"))].index.tolist()
    case_25 = df[df.index.isin(case_25_index)].copy()
    case_25.to_csv("../data/dataset/case/case_25.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_25_index)]



    # (주)로 시작하고 급여, 상여, 성과가 있는 케이스
    case_list = "|".join(["급여", "상여", "성과", "월급"])
    case_26_index = df[((df["적요_pre"].str.startswith(("(주)", "（주）", "㈜", "주식회사", "주）"))) | 
                        (df["적요_pre"].str.endswith(("(주)", "（주）", "㈜", "주식회사", "주）")))) &
                    (df["적요_pre"].str.contains(case_list))].index.tolist()
    case_26 = df[df.index.isin(case_26_index)].copy()
    case_26.to_csv("../data/dataset/case/case_26.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_26_index)]


    # (주)로 끝나는 케이스
    case_27_index = df[(df["적요_pre"].str.endswith(("(주)", "（주）", "㈜", "주식회사", "주）", "주식회")))].index.tolist()
    case_27 = df[df.index.isin(case_27_index)].copy()
    case_27.to_csv("../data/dataset/case/case_27.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_27_index)]


    # (주)로 시작하는 케이스
    case_27_1_index = df[(df["적요_pre"].str.startswith(("(주)", "（주）", "㈜", "주식회사", "주）")))].index.tolist()
    case_27_1 = df[df.index.isin(case_27_1_index)].copy()
    case_27_1.to_csv("../data/dataset/case/case_27_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_27_1_index)]


    # 세무서가 있는 케이스
    case_28_index = df[(df["적요_pre"].str.contains(("세무서")))].index.tolist()
    case_28 = df[df.index.isin(case_28_index)].copy()
    case_28.to_csv("../data/dataset/case/case_28.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_28_index)]


    # 요금으로 끝나는 경우
    case_29_index = df[(df["적요_pre"].str.endswith("요금"))].index.tolist()
    case_29 = df[df.index.isin(case_29_index)].copy()
    case_29.to_csv("../data/dataset/case/case_29.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_29_index)]


    # 입금으로 끝나는 케이스
    case_30_index = df[(df["적요_pre"].str.endswith("입금"))].index.tolist()
    case_30 = df[df.index.isin(case_30_index)].copy()
    case_30.to_csv("../data/dataset/case/case_30.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_30_index)]



    # 상금으로 끝나는 케이스
    case_31_index = df[(df["적요_pre"].str.endswith("상금"))].index.tolist()
    case_31 = df[df.index.isin(case_31_index)].copy()
    case_31.to_csv("../data/dataset/case/case_31.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_31_index)]



    # 세무로 끝나거나 시작하는 케이스
    case_32_index = df[((df["적요_pre"].str.endswith("세무")) | 
                        (df["적요_pre"].str.startswith("세무")))].index.tolist()
    case_32 = df[df.index.isin(case_32_index)].copy()
    case_32.to_csv("../data/dataset/case/case_32.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_32_index)]



    # 농협-농협으로 시작하는 케이스
    case_33_index = df[(df["적요_pre"].str.startswith("농협-농협"))].index.tolist()
    case_33 = df[df.index.isin(case_33_index)].copy()
    case_33.to_csv("../data/dataset/case/case_33.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_33_index)]



    # 은행명으로 시작하고 2번째가 -로 시작하면서 개인간입금 단어가 있는 케이스
    case_34_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(indi_word_for_contains))].index.tolist()
    case_34 = df[df.index.isin(case_34_index)].copy()
    case_34.to_csv("../data/dataset/case/case_34.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_34_index)]



    # 은행명으로 시작하고 2번째가 -로 시작하면서 길이가 4인 케이스
    case_35_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) &  
                    (df["적요길이"]==4)].index.tolist()
    case_35 = df[df.index.isin(case_35_index)].copy()
    case_35.to_csv("../data/dataset/case/case_35.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_35_index)]



    # 은행명으로 시작하고 2번째가 -로 시작하면서 이름이 들어있는 케이스
    case_36_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    (df["적요_pre"].apply(lambda x: find_name(x[3:])))].index.tolist()
    case_36 = df[df.index.isin(case_36_index)].copy()
    case_36.to_csv("../data/dataset/case/case_36.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_36_index)]



    # 기금으로 끝나는 케이스
    case_37_index = df[(df["적요_pre"].str.endswith("기금"))].index.tolist()
    case_37 = df[df.index.isin(case_37_index)].copy()
    case_37.to_csv("../data/dataset/case/case_37.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_37_index)]



    # 은행명으로 시작하고 길이가 5인 케이스
    case_38_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요길이"]==5)].index.tolist()
    case_38 = df[df.index.isin(case_38_index)].copy()
    case_38.to_csv("../data/dataset/case/case_38.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_38_index)]



    # 급여로 끝나는 케이스
    case_39_index = df[((df["적요_pre"].str.endswith("급여")))].index.tolist()
    case_39 = df[df.index.isin(case_39_index)].copy()
    case_39.to_csv("../data/dataset/case/case_39.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_39_index)]


    # 월급여, 급여로 시작하는 케이스
    case_39_1_index = df[(df["적요_pre"].str.startswith("급여")) |
                         (df["적요_pre"].str.startswith("월급여"))].index.tolist()
    case_39_1 = df[df.index.isin(case_39_1_index)].copy()
    case_39_1.to_csv("../data/dataset/case/case_39_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_39_1_index)]


    # 연말정산으로 끝나는 케이스
    case_40_index = df[(df["적요_pre"].str.endswith("연말정산"))].index.tolist()
    case_40 = df[df.index.isin(case_40_index)].copy()
    case_40.to_csv("../data/dataset/case/case_40.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_40_index)]


    # 특별상여금, 명절상여금, 성과상여금, 근로상여금으로 끝나는 케이스
    case_41_index = df[((df["적요_pre"].str.endswith(("특별상여금", "명절상여금", "성과상여금", "근로상여금"))))].index.tolist()
    case_41 = df[df.index.isin(case_41_index)].copy()
    case_41.to_csv("../data/dataset/case/case_41.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_41_index)]


    # 상여금으로 끝나는 케이스
    case_41_1_index = df[((df["적요_pre"].str.endswith("상여금")))].index.tolist()
    case_41_1 = df[df.index.isin(case_41_1_index)].copy()
    case_41_1.to_csv("../data/dataset/case/case_41_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_41_1_index)]



    # 성과급으로 끝나고 길이가 4이상인 케이스
    case_42_index = df[(df["적요_pre"].str.endswith(("성과급")))].index.tolist()
    case_42 = df[df.index.isin(case_42_index)].copy()
    case_42.to_csv("../data/dataset/case/case_42.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_42_index)]



    # 인센티브로 끝나는 케이스
    case_43_index = df[((df["적요_pre"].str.endswith("인센티브")))].index.tolist()
    case_43 = df[df.index.isin(case_43_index)].copy()
    case_43.to_csv("../data/dataset/case/case_43.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_43_index)]


    # 인센티브로 시작하는 케이스
    case_43_1_index = df[(df["적요_pre"].str.startswith("인센티브"))].index.tolist()
    case_43_1 = df[df.index.isin(case_43_1_index)].copy()
    case_43_1.to_csv("../data/dataset/case/case_43_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_43_1_index)]
    
    
    # 대금으로 끝나는 케이스
    case_44_index = df[(df["적요_pre"].str.endswith("대금"))].index.tolist()
    case_44 = df[df.index.isin(case_44_index)].copy()
    case_44.to_csv("../data/dataset/case/case_44.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_44_index)]


    # 연말정산으로 시작하는 케이스
    case_45_index = df[(df["적요_pre"].str.startswith("연말정산"))].index.tolist()
    case_45 = df[df.index.isin(case_45_index)].copy()
    case_45.to_csv("../data/dataset/case/case_45.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_45_index)]



    # 월급으로 끝나는 케이스
    case_46_index = df[(df["적요_pre"].str.endswith("학교"))].index.tolist()
    case_46 = df[df.index.isin(case_46_index)].copy()
    case_46.to_csv("../data/dataset/case/case_46.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_46_index)]



    # 거래코드가 수익증권 또는 수신입금인 케이스
    case_47_index = df[(df["거래코드"].str.contains("수익증권|수신입금"))].index.tolist()
    case_47 = df[df.index.isin(case_47_index)].copy()
    case_47.to_csv("../data/dataset/case/case_47.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_47_index)]



    # DB손보로 시작하고 길이가 5이상인 케이스
    case_48_index = df[(df["적요_pre"].str.startswith("DB손보"))].index.tolist()
    case_48 = df[df.index.isin(case_48_index)].copy()
    case_48.to_csv("../data/dataset/case/case_48.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_48_index)]



    # 증권으로 끝나는 케이스
    case_49_index = df[(df["적요_pre"].str.endswith("증권"))].index.tolist()
    case_49 = df[df.index.isin(case_49_index)].copy()
    case_49.to_csv("../data/dataset/case/case_49.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_49_index)]



    # KB증으로 시작하고 길이가 6인 케이스
    case_50_index = df[(df["적요_pre"].str.startswith("KB증")) & 
                    (df["적요길이"]==6)].index.tolist()
    case_50 = df[df.index.isin(case_50_index)].copy()
    case_50.to_csv("../data/dataset/case/case_50.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_50_index)]



    # ＹＭＣＡ, ＹＷＣＡ로 끝나는 케이스
    case_51_index = df[(df["적요_pre"].str.endswith(("ＹＭＣＡ", "ＹＷＣＡ")))].index.tolist()
    case_51 = df[df.index.isin(case_51_index)].copy()
    case_51.to_csv("../data/dataset/case/case_51.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_51_index)]



    # 연금으로 끝나는 케이스
    case_52_index = df[(df["적요_pre"].str.endswith("연금"))].index.tolist()
    case_52 = df[df.index.isin(case_52_index)].copy()
    case_52.to_csv("../data/dataset/case/case_52.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_52_index)]



    # 2번째가 우유, 유업로 시작하고 길이가 6인 케이스
    pattern = r'^.{2}(우유|유업)'
    case_53_index = df[(df["적요_pre"].str.match(pattern, na=False)) & 
                    (df["적요길이"]==6)].index.tolist()
    case_53 = df[df.index.isin(case_53_index)].copy()
    case_53.to_csv("../data/dataset/case/case_53.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_53_index)]



    # 앞에 2글자가 은행명이면서 뒤에 2글자와 같고 7글자 이상인 경우
    def same_start_end(text):
        start = text[:2]
        if start in bank_dict.keys():
            if text.endswith(start):
                return True
            else:
                return False
        elif start in place:
            if text.endswith(start):
                return True
            else:
                return False
        else:
            return False
    case_54_index = df[(df["적요_pre"].apply(lambda x: same_start_end(x))) & 
                    (df["적요길이"]>6)].index.tolist()
    case_54 = df[df.index.isin(case_54_index)].copy()
    case_54.to_csv("../data/dataset/case/case_54.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_54_index)]



    # 봉사, 공로, 복지, 조교, 근로, 학과 장학금으로 끝나는 케이스
    case_55_index = df[((df["적요_pre"].str.endswith(("봉사장학금", "공로장학금", "복지장학금", "조교장학금", "근로장학금", "학과장학금",))))].index.tolist()
    case_55 = df[df.index.isin(case_55_index)].copy()
    case_55.to_csv("../data/dataset/case/case_55.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_55_index)]


    # 장학금으로 끝나는 케이스
    case_55_1_index = df[((df["적요_pre"].str.endswith("장학금")))].index.tolist()
    case_55_1 = df[df.index.isin(case_55_1_index)].copy()
    case_55_1.to_csv("../data/dataset/case/case_55_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_55_1_index)]


    # 연차수당으로 끝나고 길이가 5이상인 케이스
    case_56_index = df[((df["적요_pre"].str.endswith("연차수당")))].index.tolist()
    case_56 = df[df.index.isin(case_56_index)].copy()
    case_56.to_csv("../data/dataset/case/case_56.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_56_index)]



    # 은행명으로 시작하며 -가 있고 00비로 끝나는 케이스
    case_57_index = df[((df["적요_pre"].str.startswith(tuple(bank_dict.keys())))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    ((df["적요_pre"].str.endswith(tuple(cost_word_for_contains.split("|")))))].index.tolist()
    case_57 = df[df.index.isin(case_57_index)].copy()
    case_57.to_csv("../data/dataset/case/case_57.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_57_index)]



    # 특별상여로 끝나는 케이스
    case_58_index = df[(df["적요_pre"].str.endswith("특별상여"))].index.tolist()
    case_58 = df[df.index.isin(case_58_index)].copy()
    case_58.to_csv("../data/dataset/case/case_58.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_58_index)]



    # 에너지로 끝나는 케이스
    case_59_index = df[((df["적요_pre"].str.endswith("에너지")))].index.tolist()
    case_59 = df[df.index.isin(case_59_index)].copy()
    case_59.to_csv("../data/dataset/case/case_59.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_59_index)]



    # 설상여로 끝나는 케이스
    case_60_index = df[((df["적요_pre"].str.endswith("설상여")))].index.tolist()
    case_60 = df[df.index.isin(case_60_index)].copy()
    case_60.to_csv("../data/dataset/case/case_60.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_60_index)]



    # 환불로 끝나는 케이스
    case_61_index = df[(df["적요_pre"].str.endswith("환불"))].index.tolist()
    case_61 = df[df.index.isin(case_61_index)].copy()
    case_61.to_csv("../data/dataset/case/case_61.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_61_index)]



    # # 00비로 끝나는 케이스    
    case_62_index = df[((df["적요_pre"].str.endswith(tuple(cost_word_for_contains.split("|")))))].index.tolist()
    case_62 = df[df.index.isin(case_62_index)].copy()
    case_62.to_csv("../data/dataset/case/case_62.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_62_index)]


    # 명절상여로 끝나고 길이가 4이상인 케이스
    case_63_index = df[((df["적요_pre"].str.endswith("명절상여"))) & 
                    (df["적요길이"]>4)].index.tolist()
    case_63 = df[df.index.isin(case_63_index)].copy()
    case_63.to_csv("../data/dataset/case/case_63.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_63_index)]



    # 사단법인으로 시작하는 케이스
    case_64_index = df[(df["적요_pre"].str.startswith(("(사)", "（사）", "사단법인", "사）"))) | 
                    (df["적요_pre"].str.endswith(("(사)", "（사）", "사단법인", "사）")))].index.tolist()
    case_64 = df[df.index.isin(case_64_index)].copy()
    case_64.to_csv("../data/dataset/case/case_64.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_64_index)]



    # 저축은행으로 끝나는 케이스
    case_65_index = df[(df["적요_pre"].str.endswith("저축은행"))].index.tolist()
    case_65 = df[df.index.isin(case_65_index)].copy()
    case_65.to_csv("../data/dataset/case/case_65.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_65_index)]



    # 정보통신으로 끝나고 길이가 9이하인 케이스
    case_66_index = df[(df["적요_pre"].str.endswith("정보통신")) & 
                    (df["적요길이"]<10)].index.tolist()
    case_66 = df[df.index.isin(case_66_index)].copy()
    case_66.to_csv("../data/dataset/case/case_66.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_66_index)]



    # 통신비지원으로 끝나는 케이스
    case_67_index = df[(df["적요_pre"].str.endswith(("통신비지원")))].index.tolist()
    case_67 = df[df.index.isin(case_67_index)].copy()
    case_67.to_csv("../data/dataset/case/case_67.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_67_index)]



    # 통신비가 있는 케이스
    # case_list = "|".join(["통신비", "SKT", "LGU"])
    case_67_1_index = df[(df["적요_pre"].str.contains("통신비"))].index.tolist()
    case_67_1 = df[df.index.isin(case_67_1_index)].copy()
    case_67_1.to_csv("../data/dataset/case/case_67_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_67_1_index)]



    # 명절수당으로 끝나는 케이스
    case_68_index = df[(df["적요_pre"].str.endswith("명절수당"))].index.tolist()
    case_68 = df[df.index.isin(case_68_index)].copy()
    case_68.to_csv("../data/dataset/case/case_68.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_68_index)]



    # 추가상여, 정기상여, 성과상여, 급여상여로 끝나는 케이스
    case_69_index = df[(df["적요_pre"].str.endswith(("추가상여", "정기상여", "성과상여", "급여상여", )))].index.tolist()
    case_69 = df[df.index.isin(case_69_index)].copy()
    case_69.to_csv("../data/dataset/case/case_69.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_69_index)]



    # 상여로 끝나고 길이가 5이상인 케이스
    case_69_1_index = df[(df["적요_pre"].str.endswith(("상여")) &
                        (df["적요길이"]>4))].index.tolist()
    case_69_1 = df[df.index.isin(case_69_1_index)].copy()
    case_69_1.to_csv("../data/dataset/case/case_69_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_69_1_index)]



    # 상여로 끝나는 케이스
    case_69_2_index = df[df["적요_pre"].str.endswith(("상여"))].index.tolist()
    case_69_2 = df[df.index.isin(case_69_2_index)].copy()
    case_69_2.to_csv("../data/dataset/case/case_69_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_69_2_index)]


    # 00료로 끝나는 경우
    case_70_index = df[(df["적요_pre"].str.endswith(tuple(fare_word_for_contains.split("|"))))].index.tolist()
    case_70 = df[df.index.isin(case_70_index)].copy()
    case_70.to_csv("../data/dataset/case/case_70.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_70_index)]



   # 은행명으로 시작하고 뒤에 회사나 법인이 들어있는 경우
    inco_comp_escaped = [re.escape(key) for key in inco_comp_dict.keys()]
    case_71_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains("|".join(inco_comp_escaped)))].index.tolist()
    case_71 = df[df.index.isin(case_71_index)].copy()
    case_71.to_csv("../data/dataset/case/case_71.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_71_index)]


    # 회사나 법인이 들어있고 회사사용 단어가 있는 경우
    inco_comp_escaped = [re.escape(key) for key in inco_comp_dict.keys()]
    case_72_index = df[(df["적요_pre"].str.contains("|".join(inco_comp_escaped))) &
                       (df["적요_pre"].str.contains(comp_word_for_contains))].index.tolist()
    case_72 = df[df.index.isin(case_72_index)].copy()
    case_72.to_csv("../data/dataset/case/case_72.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_72_index)]
    



    # 상여금이나 상여로 시작하고 길이가 5이상인 케이스
    case_73_index = df[df["적요_pre"].str.startswith(("상여금", "상여")) &
                        (df["적요길이"]>4)].index.tolist()
    case_73 = df[df.index.isin(case_73_index)].copy()
    case_73.to_csv("../data/dataset/case/case_73.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_73_index)]



    # 근로, 근무수당으로 끝나는 케이스
    case_74_index = df[(df["적요_pre"].str.endswith(("근로수당", "근무수당")))].index.tolist()
    case_74 = df[df.index.isin(case_74_index)].copy()
    case_74.to_csv("../data/dataset/case/case_74.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_74_index)]



    # 방과후로 끝나거나 시작하는 케이스
    case_75_index = df[(df["적요_pre"].str.startswith("방과후")) | 
                    (df["적요_pre"].str.endswith("방과후"))].index.tolist()
    case_75 = df[df.index.isin(case_75_index)].copy()
    case_75.to_csv("../data/dataset/case/case_75.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_75_index)]



    # 유치원으로 끝나는 케이스
    case_76_index = df[(df["적요_pre"].str.endswith("유치원"))].index.tolist()
    case_76 = df[df.index.isin(case_76_index)].copy()
    case_76.to_csv("../data/dataset/case/case_76.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_76_index)]



    # 은행명으로 시작하고 뒤에 이름이 있는 경우
    case_77_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].apply(lambda x: find_name(x[2:])))].index.tolist()
    case_77 = df[df.index.isin(case_77_index)].copy()
    case_77.to_csv("../data/dataset/case/case_77.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_77_index)]


    # 00예금으로 끝나는 경우
    case_78_index = df[(df["적요_pre"].str.endswith(("정기예금", "일반예금", "적립예금")))].index.tolist()
    case_78= df[df.index.isin(case_78_index)].copy()
    case_78.to_csv("../data/dataset/case/case_78.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_78_index)]


    # 교육관련 비용으로 끝나는 경우
    case_79_index = df[(df["적요_pre"].str.endswith(tuple(ede_word_for_contains.split("|"))))].index.tolist()
    case_79 = df[df.index.isin(case_79_index)].copy()
    case_79.to_csv("../data/dataset/case/case_79.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_79_index)]



    # 00급여로 시작하는 케이스
    case_80_index = df[(df["적요_pre"].str.startswith(("명절급여", "정기급여", "정산급여", "직원급여", "개인급여")))].index.tolist()
    case_80 = df[df.index.isin(case_80_index)].copy()
    case_80.to_csv("../data/dataset/case/case_80.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_index)]




    # 월급으로 시작하는 케이스
    case_80_1_index = df[(df["적요_pre"].str.startswith("월급"))].index.tolist()
    case_80_1 = df[df.index.isin(case_80_1_index)].copy()
    case_80_1.to_csv("../data/dataset/case/case_80_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_1_index)]




    # 월급으로 끝나는 케이스
    case_80_2_index = df[(df["적요_pre"].str.endswith("월급"))].index.tolist()
    case_80_2 = df[df.index.isin(case_80_2_index)].copy()
    case_80_2.to_csv("../data/dataset/case/case_80_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_2_index)]




    # 급여가 있는 케이스
    case_80_3_index = df[(df["적요_pre"].str.contains("급여"))].index.tolist()
    case_80_3 = df[df.index.isin(case_80_3_index)].copy()
    case_80_3.to_csv("../data/dataset/case/case_80_3.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_3_index)]




    # 00복지관으로 끝나는 경우
    case_81_index = df[(df["적요_pre"].str.endswith(("시각복지관", "실버복지관", "노인복지관", "장애인복지관", \
                                                    "노인종합복지관", "장애인복합복지관", "사회복지관", \
                                                    "종합사회복지관", "종합복지관")))].index.tolist()
    case_81 = df[df.index.isin(case_81_index)].copy()
    case_81.to_csv("../data/dataset/case/case_81.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_81_index)]



    # 복지관으로 끝나는 경우
    case_81_1_index = df[(df["적요_pre"].str.endswith("복지관"))].index.tolist()
    case_81_1 = df[df.index.isin(case_81_1_index)].copy()
    case_81_1.to_csv("../data/dataset/case/case_81_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_81_1_index)]



    # 성과급으로 시작
    case_82_index = df[(df["적요_pre"].str.startswith("성과급"))].index.tolist()
    case_82 = df[df.index.isin(case_82_index)].copy()
    case_82.to_csv("../data/dataset/case/case_82.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_82_index)]



    # 천주교회, 중앙교회, 교회로 끝나는 케이스
    case_83_index = df[(df["적요_pre"].str.endswith(("천주교회", "중앙교회", "교회")))].index.tolist()
    case_83 = df[df.index.isin(case_83_index)].copy()
    case_83.to_csv("../data/dataset/case/case_83.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_83_index)]



    # # 금융사명 뒤에 ( 로 시작하는 케이스
    # case_84_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
    #                 (df["적요_pre"].str[2].isin(("(", "（")))].index.tolist()
    # case_84 = df[df.index.isin(case_84_index)].copy()
    # case_84.to_csv("../data/dataset/case/case_84.csv", encoding="utf-8-sig")
    # df = df[~df.index.isin(case_84_index)]



    # 삼성금융으로 시작하는 경우
    case_85_index = df[(df["적요_pre"].str.startswith("삼성금융"))].index.tolist()
    case_85 = df[df.index.isin(case_85_index)].copy()
    case_85.to_csv("../data/dataset/case/case_85.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_85_index)]



    # ()안에 1글자가 들어있는 것으로 시작하는 경우
    def find_pare(text):
        # 정규표현식 패턴을 사용하여 괄호 안의 글자를 추출합니다.
        if (text[0] == "(") and (text[2] == ")"):
            return True
        elif (text[0] == "（") and (text[2] == "）"):
            return True
        else:
            return False
    case_86_index = df[(df["적요_pre"].apply(lambda x: find_pare(x)))].index.tolist()
    case_86 = df[df.index.isin(case_86_index)].copy()
    case_86.to_csv("../data/dataset/case/case_86.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_86_index)]



    # 대출소개로 시작하는 경우
    case_87_index = df[(df["적요_pre"].str.startswith("대출소개"))].index.tolist()
    case_87 = df[df.index.isin(case_87_index)].copy()
    case_87.to_csv("../data/dataset/case/case_87.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_87_index)]



    # 중진공으로 시작하는 경우
    case_88_index = df[(df["적요_pre"].str.startswith("중진공"))].index.tolist()
    case_88 = df[df.index.isin(case_88_index)].copy()
    case_88.to_csv("../data/dataset/case/case_88.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_88_index)]



    # 00수당으로 끝나고 길이가 4이상인 케이스
    case_89_index = df[(df["적요_pre"].str.endswith(("야근수당", "연구수당", "업무수당", "직무수당", \
                                                    "특별수당", "연수수당", "강의수당", "관리수당", \
                                                    "직책수당", "참석수당", "교육수당", "복지수당"))) &
                    (df["적요길이"]>3)].index.tolist()
    case_89 = df[df.index.isin(case_89_index)].copy()
    case_89.to_csv("../data/dataset/case/case_89.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_89_index)]



    # 수당으로 끝나고 길이가 4인 케이스
    case_89_1_index = df[(df["적요_pre"].str.endswith("수당")) &
                    (df["적요길이"]==4)].index.tolist()
    case_89_1 = df[df.index.isin(case_89_1_index)].copy()
    case_89_1.to_csv("../data/dataset/case/case_89_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_89_1_index)]


    # 수당으로 끝나고 길이가 4 이상인 케이스
    case_89_2_index = df[(df["적요_pre"].str.endswith("수당")) &
                    (df["적요길이"]>3)].index.tolist()
    case_89_2 = df[df.index.isin(case_89_2_index)].copy()
    case_89_2.to_csv("../data/dataset/case/case_89_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_89_2_index)]


    # ＣＪ로 시작하는 경우
    case_90_index = df[(df["적요_pre"].str.startswith("ＣＪ"))].index.tolist()
    case_90 = df[df.index.isin(case_90_index)].copy()
    case_90.to_csv("../data/dataset/case/case_90.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_90_index)]



    # DLIVE로 시작하는 경우
    case_91_index = df[(df["적요_pre"].str.startswith("DLIVE"))].index.tolist()
    case_91 = df[df.index.isin(case_91_index)].copy()
    case_91.to_csv("../data/dataset/case/case_91.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_91_index)]



    # 청약으로 끝나는 경우
    case_92_index = df[(df["적요_pre"].str.endswith("청약"))].index.tolist()
    case_92 = df[df.index.isin(case_92_index)].copy()
    case_92.to_csv("../data/dataset/case/case_92.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_92_index)]
    
    # df.to_csv("../data/dataset/case/etc.csv", encoding="utf-8-sig")
    df.to_csv("../data/dataset/case_v4/etc.csv", encoding="utf-8-sig")

    return df
    
    
def split_data_2(path):
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)

    # df["적요_pre"] = df["적요"].progress_apply(lambda x: process_text(x))
    # df["적요길이"] = df["적요_pre"].progress_apply(lambda x: len([i for i in x if i not in (" ", "　", "-", "－", "_", "＿")]))
    # df["적요반대_pre"] = df["적요_pre"].progress_apply(lambda x: x[::-1])
    
    ################################################## v2
    # 월세 또는 월세액으로 끝나는 경우
    case_93_index = df[(df["적요_pre"].str.endswith(("월세", "월세액")))].index.tolist()
    case_93 = df[df.index.isin(case_93_index)].copy()
    case_93.to_csv("../data/dataset/case/case_93.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_93_index)]
    
    # 교통으로 끝나는 경우
    case_94_index = df[(df["적요_pre"].str.endswith(("교통")))].index.tolist()
    case_94 = df[df.index.isin(case_94_index)].copy()
    case_94.to_csv("../data/dataset/case/case_94.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_94_index)]

    # 교통비로 시작하는 경우
    case_94_1_index = df[(df["적요_pre"].str.startswith(("교통비")))].index.tolist()
    case_94_1 = df[df.index.isin(case_94_1_index)].copy()
    case_94_1.to_csv("../data/dataset/case/case_94_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_94_1_index)]
    
    # 연말이 들어있는 경우
    case_95_index = df[(df["적요_pre"].str.contains("연말"))].index.tolist()
    case_95 = df[df.index.isin(case_95_index)].copy()
    case_95.to_csv("../data/dataset/case/case_95.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_95_index)]
    
    # 시스템으로 끝나는 경우
    case_96_index = df[(df["적요_pre"].str.endswith("시스템"))].index.tolist()
    case_96 = df[df.index.isin(case_96_index)].copy()
    case_96.to_csv("../data/dataset/case/case_96.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_96_index)]
    
    # 매도로 끝나는 경우
    case_97_index = df[(df["적요_pre"].str.endswith("매도"))].index.tolist()
    case_97 = df[df.index.isin(case_97_index)].copy()
    case_97.to_csv("../data/dataset/case/case_97.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_97_index)]
    
    # 00돈으로 끝나는 경우
    case_98_index = df[(df["적요_pre"].str.endswith(("용돈", "세배돈", "곗돈", "갯돈", "세뱃돈", "목돈")))].index.tolist()
    case_98 = df[df.index.isin(case_98_index)].copy()
    case_98.to_csv("../data/dataset/case/case_98.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_98_index)]
    
    # 협회로 끝나는 경우
    case_99_index = df[(df["적요_pre"].str.endswith("협회"))].index.tolist()
    case_99 = df[df.index.isin(case_99_index)].copy()
    case_99.to_csv("../data/dataset/case/case_99.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_99_index)]

    # 은행명으로 시작하고 두번째가 -이며 계로 끝나는 경우
    case_100_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) &
                    (df["적요_pre"].str.endswith(("계")))].index.tolist()
    case_100 = df[df.index.isin(case_100_index)].copy()
    case_100.to_csv("../data/dataset/case/case_100.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_100_index)]    
    

    # 회사나 법인이 들어있고 회사사용 단어가 있는 경우
    inco_comp_escaped = [re.escape(key) for key in inco_comp_dict.keys()]
    case_101_index = df[(df["적요_pre"].str.contains("|".join(inco_comp_escaped)))].index.tolist()
    case_101 = df[df.index.isin(case_101_index)].copy()
    case_101.to_csv("../data/dataset/case/case_101.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_101_index)]
    
    # 재료로 끝나는 경우
    case_102_index = df[(df["적요_pre"].str.endswith("재료"))].index.tolist()
    case_102 = df[df.index.isin(case_102_index)].copy()
    case_102.to_csv("../data/dataset/case/case_102.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_102_index)]

    # # 비로 끝나는 경우
    # case_103_index = df[(df["적요_pre"].str.endswith("비"))].index.tolist()
    # case_103 = df[df.index.isin(case_103_index)].copy()
    # case_103.to_csv("../data/dataset/case/case_103.csv", encoding="utf-8-sig")
    # df = df[~df.index.isin(case_103_index)]
    

    # 은행명으로 시작하고 두번째가 -인 경우
    case_999_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－")))].index.tolist()
    case_999 = df[df.index.isin(case_999_index)].copy()
    case_999.to_csv("../data/dataset/case/case_999.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_999_index)]
    
    df.to_csv("../data/dataset/case/etc.csv", encoding="utf-8-sig")

    return df

if __name__ == "__main__":
    split_data("../data/dataset/alldata.csv")
    split_data_2("../data/dataset/case_v4/etc.csv")
