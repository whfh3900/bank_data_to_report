import pandas as pd
from glob import glob
from work import *
from tqdm import tqdm
import re
import os
import unicodedata
from ats_module.text_preprocessing import *
nk = Nickonlpy(base=False)
tqdm.pandas()

def process_text(text):
    # 정규표현식 패턴을 사용하여 괄호 안의 글자를 추출합니다.
    pattern = r'[(（](.*?)[)）]'
    matches = re.findall(pattern, text)

    # 2글자 이상인 경우 특수문자를 제거하여 반환합니다.
    for match in matches:
        if len(match) != 1:
            # 특수문자를 제거합니다. (알파벳과 숫자만 남깁니다.)
            text = text.replace("(", "")
            text = text.replace("（", "")
            text = text.replace(")", "")
            text = text.replace("）", "")
    text = text.replace(" ", "0")
    text = text.replace("　", "0")

    return text

def convert_fullwidth_to_halfwidth(text):
    return ''.join(unicodedata.normalize('NFKC', c) for c in text)

def del_sw(text, delete_num=True):
    # 전각을 모두 반각으로
    text = convert_fullwidth_to_halfwidth(text)
    text = text.replace("(주", " 주 ")
    text = text.replace("주)", " 주 ")
    text = text.replace("㈜", " 주 ")
    
    text = re.sub(r'[^\w\s]', ' ', text)
    text = text.replace('_', ' ')

    text = text.replace(" 주 ", "(주)")
    text = text.replace(" 유 ", "(유)")
    text = text.replace(" 학 ", "(학)")
    text = text.replace(" 복 ", "(복)")
    text = text.replace(" 재 ", "(재)")
    text = text.replace(" 의 ", "(의)")
    text = text.replace(" 합 ", "(합)")
    text = text.replace(" 사 ", "(사)")

    text = text.strip()
    if delete_num:
        text = text.replace("0월", " 1월 ")
        text = text.replace("0년", " 1년 ")
        text = text.replace("0회", " 1회 ")
        text = text.replace("0일", " 1일 ")
        text = text.replace("0만", " 1만 ")
        text = text.replace("0분", " 1분 ")
        text = text.replace("0호", " 1호 ")
        text = text.replace("0층", " 1층 ")
        text = text.replace("0月", " 1月 ")
        text = text.replace("0주", " 1주 ")
        text = text.replace("0차", " 1차 ")
        text = text.replace("0동", " 1동 ")
        text = text.replace("0기", " 1기 ")

        text = text.replace("0세기", " 1세기 ")

        text = text.replace("1주 년", " 1주년 ")
        text = text.replace("1분 기", " 1분기 ")
        text = text.replace("1년 차", " 1년차 ")
        text = text.replace("1년 도", " 1년도 ")
        text = text.replace("1월 분", " 1월분 ")
        text = text.replace("1년 분", " 1년분 ")

        text = " ".join(text.split("0"))
    return text

def find_name(text):
    
    # 정규표현식을 사용하여 특수문자를 제거합니다.
    result = re.sub(r'[^\w\s]', ' ', text)
    result = [i[0] for i in nk.post.pos(result) if i[1] == 'Name']
    return result


def check_language(input_str):
    korean_pattern = re.compile(r'^[가-힣\s]+$')  # 한글 및 공백 문자만 포함하는 정규 표현식
    english_pattern = re.compile(r'^[A-Za-z\s]+$')  # 영어 및 공백 문자만 포함하는 정규 표현식
    
    if korean_pattern.match(input_str):
        return True
    elif english_pattern.match(input_str):
        return False
    else:
        return False
    
    
# bank = ["국민", "농협", "신한", "신협", "금고", "기업", "씨티", "산업", "ＳＣ","SC" \
#         "수협", "하나", "국고", "대신", "KB", "한화", "삼성", "미래","대구", \
#         "우체", "메츠", "산림"]

place = ["제주", "전북", "경남", "한국", "부산", "광주", "대구"]
sala_word_for_contains = "|".join(["월급여", "급여", "월급"])
bonu_word_for_contains = "|".join(["상여금", "상여", "성과", "인센티브"])
save_word_for_contains = "|".join(["주택청약금", "주택청약", "청약", "저축", "적금"])
ede_word_for_contains = "|".join(["교육비", "방과후", "학원비", "학습비", "등록금", "학비", \
                                "기숙사비", "교과서비", "석식비", "재료비", "급식비", \
                                "교재비", "하복비", "체험비", "체육복비", "수강료"])
insu_word_for_contains = "|".join(["화재보험료", "종신보험료", "연금보험", "종신보험", "암보험", "건강보험", \
                                "실비보험", "운전자보험", "손해보험", "보험료", "보험비", "보험"])
resi_word_for_contains = "|".join(["전세금", "전세", "관리비", "월세"])
loan_word_for_contains = "|".join(["대출이자", "이자", "대출"])

indi_word_for_contains = "|".join(["가족", "엄마", "아빠", "모임", "어머니", "아버지", \
                                "누나", "동생", "용돈", "생활비", "곗돈", "장모님", "회비", "친정", "계돈"])

# ede_word = ["교과서비", "석식비", "재료비", "급식비", "교재비", "하복비", "체험비", "체육복비"]

bank_dict={"금고":"새마을금고",
           "국민":"KB국민은행",
           "KB":"KB국민은행",
           "기업":"기업은행",
           "농협":"NH농협은행",
           "신한":"신한은행",
           "씨티":"한국씨티은행",
           "산업":"산업은행",
           "ＳＣ":"SC제일은행",
           "하나":"하나은행",
           "대신":"대신증권",
           "한화":"한화은행",
           "미래":"미래애셋증권",
           "우체":"우체국",
           "산림":"산림조합",
           "메츠":"메리츠",
           "부산":"부산은행",
           "대구":"대구은행",
           "경남":"경남은행",
           "광주":"광주은행",
           "대구":"대구은행",
           "전북":"전북은행",
           "제주":"제주은행",
           "한국":"한국은행",
           "카카":"카카오뱅크",
           "토뱅":"토스뱅크",
           "수협":"수협은행",
           "신협":"신협은행",
           "NH":"NH농협은행",
           "케이비":"KB국민은행",
           }

inco_comp_dict = {
                "（유）": "유한회사",
                "(유)": "유한회사",
                "（재）": "재단법인",
                "(재)": "재단법인",
                "（주）": "주식회사",
                "㈜": "주식회사",
                "(주)": "주식회사",
                "（사）": "사단법인",
                "(사)": "사단법인",
                "（의）": "의료법인",
                "(의)": "의료법인",
                "（학）": "학교법인",
                "(학)": "학교법인",
                "（합）": "합자회사",
                "(합)": "합자회사",
                "（복）": "복지재단",
                "(복)": "복지재단",
                }

bank_dict_2 = {"국민":['국민은행','KB','Kb','국민'],
                "신한":['신한은행','신한'],
                "기업":['기업은행','기업',"IBK"],
                "농협":['농협은행','NH','nh','농협'],
                "금고":["새마을금고","새마을","금고"],
                "신협":["신협"],
                "씨티":["씨티은행"],
                "ＳＣ":["SC제일은행"],
                "SC":["SC제일은행"],
                "수협":["수협"],
                "하나":["하나"],
                "국고":["국고"],
                "대신":["대신증권"],
                "KB":["국민"],
                "산업":["산업"],
                "한화":["한화"],
                "삼성":["삼성"],
                "미래":["미래애셋증권"],
                "우체":["우체국"],
                "메츠":["메리츠"],
                "산림":["산림"],
                "대구":["대구"]
                }

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
    df["적요길이"] = df["적요_pre"].progress_apply(lambda x: len([i for i in x if i not in (" ", "　", "-", "－", "_", "＿")]))
    df["적요반대_pre"] = df["적요_pre"].progress_apply(lambda x: x[::-1])


    ## 케이스 별로 나누자
    # 은행명으로 시작하고 2번째가 -로 시작하면서 길이가 5인 케이스
    case_1_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    (df["적요길이"]==5)].index.tolist()
    case_1 = df[df.index.isin(case_1_index)].copy()
    case_1.to_csv("./data/case/case_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_1_index)]


    # 2번째 또는 3번째가 청약으로 시작하는 케이스
    case_1_1_index = df[((df["적요_pre"].str[2:4]==("청약")) | 
                        (df["적요_pre"].str[3:5]==("청약")))].index.tolist()
    case_1_1 = df[df.index.isin(case_1_1_index)].copy()
    case_1_1.to_csv("./data/case/case_1_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_1_1_index)]
    
    
    # 은행명으로 시작하고 2번째가 -로 시작하면서 급여로 끝나는 케이스
    case_2_index = df[((df["적요_pre"].str.startswith(tuple(bank_dict.keys())))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    (df["적요_pre"].str.endswith("급여"))].index.tolist()
    case_2 = df[df.index.isin(case_2_index)].copy()
    case_2.to_csv("./data/case/case_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_2_index)]



    # 00 뒤에 월급여로 시작하고 길이가 8글자인 케이스
    case_3_index = df[(df["적요_pre"].str[2:5] == "월급여") & 
                    (df["적요길이"]==8)].index.tolist()
    case_3 = df[df.index.isin(case_3_index)].copy()
    case_3.to_csv("./data/case/case_3.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_3_index)]



    # 신한-신한으로 시작하는 케이스
    case_4_index = df[(df["적요_pre"].str.startswith("신한-신한"))].index.tolist()
    case_4 = df[df.index.isin(case_4_index)].copy()
    case_4.to_csv("./data/case/case_4.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_4_index)]



    # 은행명으로 시작하고 급여로 끝나면서 길이가 7 이상인 케이스
    case_5_index = df[((df["적요_pre"].str.startswith(tuple(bank_dict.keys())))) & 
                    (df["적요_pre"].str.endswith("급여")) &
                    (df["적요길이"]>6)].index.tolist()
    case_5 = df[df.index.isin(case_5_index)].copy()
    case_5.to_csv("./data/case/case_5.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_5_index)]



    # 은행명으로 시작하고 급여관련 단어가 들어있는 케이스
    case_6_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(sala_word_for_contains))].index.tolist()
    case_6 = df[df.index.isin(case_6_index)].copy()
    case_6.to_csv("./data/case/case_6.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_6_index)]



    # 은행명으로 시작하고 상여관련 단어가 들어있는 케이스
    case_6_1_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(bonu_word_for_contains))].index.tolist()
    case_6_1 = df[df.index.isin(case_6_1_index)].copy()
    case_6_1.to_csv("./data/case/case_6_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_6_1_index)]




    # 국민-국민으로 시작하는 케이스
    case_7_index = df[(df["적요_pre"].str.startswith(("국민-국민", "국민－국민")))].index.tolist()
    case_7 = df[df.index.isin(case_7_index)].copy()
    case_7.to_csv("./data/case/case_7.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_7_index)]



    # 은행명으로 시작하고 저축관련 단어가 들어있는 케이스
    case_8_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(save_word_for_contains))].index.tolist()
    case_8 = df[df.index.isin(case_8_index)].copy()
    case_8.to_csv("./data/case/case_8.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_8_index)]



    # 은행명으로 시작하고 두번째가 -로 시작하고 교육관련 단어가 들어있는 케이스
    case_9_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) &
                    (df["적요_pre"].str.contains(ede_word_for_contains))].index.tolist()
    case_9 = df[df.index.isin(case_9_index)].copy()
    case_9.to_csv("./data/case/case_9.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_9_index)]



    # 은행명으로 시작하고 보험관련 단어가 뒤에 들어있는 케이스
    case_10_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(insu_word_for_contains))].index.tolist()
    case_10 = df[df.index.isin(case_10_index)].copy()
    case_10.to_csv("./data/case/case_10.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_10_index)]



    # 은행명으로 시작하고 주거관련 단어가 들어있는 케이스
    case_10_1_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(resi_word_for_contains))].index.tolist()
    case_10_1 = df[df.index.isin(case_10_1_index)].copy()
    case_10_1.to_csv("./data/case/case_10_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_10_1_index)]



    # 은행명으로 시작하고 대출관련 단어가 들어있는 케이스
    case_10_2_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(loan_word_for_contains))].index.tolist()
    case_10_2 = df[df.index.isin(case_10_2_index)].copy()
    case_10_2.to_csv("./data/case/case_10_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_10_2_index)]



    # 지역명으로 시작하고 2번째가 -로 시작하면서 길이가 5인 케이스
    case_11_index = df[(df["적요길이"]==3) &
                       (df["적요_pre"].apply(lambda x: check_language(x))) & 
                       (~df["적요_pre"].str.endswith(("회","차","집","짐","여","약","비","료","급","금")))].index.tolist()
    case_11 = df[df.index.isin(case_11_index)].copy()
    case_11.to_csv("./data/case/case_11.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_11_index)]



    # 지역명으로 시작하고 길이가 5인 케이스
    case_12_index = df[(df["적요_pre"].str.startswith(tuple(place))) & 
                    (df["적요길이"]==5)].index.tolist()
    case_12 = df[df.index.isin(case_12_index)].copy()
    case_12.to_csv("./data/case/case_12.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_12_index)]



    # 0회, 00회, 000회로 시작하는 케이스
    case_13_index = df[(df["적요_pre"].str.startswith(("0회","00회","000회")))].index.tolist()
    case_13 = df[df.index.isin(case_13_index)].copy()
    case_13.to_csv("./data/case/case_13.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_13_index)]



    # 발전기금으로 끝나는 케이스
    case_14_index = df[(df["적요_pre"].str.endswith("발전기금"))].index.tolist()
    case_14 = df[df.index.isin(case_14_index)].copy()
    case_14.to_csv("./data/case/case_14.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_14_index)]



    # 세무법인으로 시작하거나 끝나는 케이스
    case_15_index = df[((df["적요_pre"].str.startswith("세무법인")) |
                    (df["적요_pre"].str.endswith("세무법인")))].index.tolist()
    case_15 = df[df.index.isin(case_15_index)].copy()
    case_15.to_csv("./data/case/case_15.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_15_index)]



    # 세무사로 시작하거나 끝나고 길이가 8이하 인 케이스
    case_16_index = df[((df["적요_pre"].str.endswith("세무사")) | 
                        (df["적요_pre"].str.startswith("세무사"))) & 
                    (df["적요길이"]<9)].index.tolist()
    case_16 = df[df.index.isin(case_16_index)].copy()
    case_16.to_csv("./data/case/case_16.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_16_index)]



    # 세무회계로 끝나거나 시작하고 길이가 5이상인 케이스
    case_17_index = df[((df["적요_pre"].str.endswith("세무회계")) | 
                        (df["적요_pre"].str.startswith("세무회계")))].index.tolist()
    case_17 = df[df.index.isin(case_17_index)].copy()
    case_17.to_csv("./data/case/case_17.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_17_index)]



    # 세무회계사로 끝나는 케이스
    case_18_index = df[df["적요_pre"].str.endswith("세무회계사")].index.tolist()
    case_18 = df[df.index.isin(case_18_index)].copy()
    case_18.to_csv("./data/case/case_18.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_18_index)]



    # 회계사로 끝나는 케이스
    case_19_index = df[df["적요_pre"].str.endswith("회계사")].index.tolist()
    case_19 = df[df.index.isin(case_19_index)].copy()
    case_19.to_csv("./data/case/case_19.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_19_index)]



    # 회계법인으로 끝나는 케이스
    case_20_index = df[(df["적요_pre"].str.endswith("회계법인"))].index.tolist()
    case_20 = df[df.index.isin(case_20_index)].copy()
    case_20.to_csv("./data/case/case_20.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_20_index)]



    # 급여이체, 급여입금, 급여지급으로 끝나는 케이스
    case_21_index = df[(df["적요_pre"].str.endswith(("급여이체", "급여입금", "급여지급", "급여수당"))) | 
                    (df["적요_pre"].str.startswith(("급여이체", "급여입금", "급여지급", "급여수당")))].index.tolist()
    case_21 = df[df.index.isin(case_21_index)].copy()
    case_21.to_csv("./data/case/case_21.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_21_index)]


    # 급여로 시작하거나 끝나고 길이가 4인 케이스
    case_21_1_index = df[(((df["적요_pre"].str.startswith("급여"))) | 
                        (df["적요_pre"].str.endswith("급여"))) &
                    (df["적요길이"]==4)].index.tolist()
    case_21_1 = df[df.index.isin(case_21_1_index)].copy()
    case_21_1.to_csv("./data/case/case_21_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_21_1_index)]


    # 세무그룹으로 시작하는 케이스
    case_22_index = df[(df["적요_pre"].str.startswith("세무그룹"))].index.tolist()
    case_22 = df[df.index.isin(case_22_index)].copy()
    case_22.to_csv("./data/case/case_22.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_22_index)]



    # 세무회로 끝나는 케이스
    case_23_index = df[(df["적요_pre"].str.endswith("세무회"))].index.tolist()
    case_23 = df[df.index.isin(case_23_index)].copy()
    case_23.to_csv("./data/case/case_23.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_23_index)]



    # 노무법인으로 시작하거나 끝나는 케이스
    case_24_index = df[(df["적요_pre"].str.startswith("노무법인")) | 
                    (df["적요_pre"].str.endswith("노무법인"))].index.tolist()
    case_24 = df[df.index.isin(case_24_index)].copy()
    case_24.to_csv("./data/case/case_24.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_24_index)]



    # SK쉴더스로 시작하는 케이스
    case_25_index = df[(df["적요_pre"].str.startswith("SK쉴더스"))].index.tolist()
    case_25 = df[df.index.isin(case_25_index)].copy()
    case_25.to_csv("./data/case/case_25.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_25_index)]



    # (주)로 시작하고 급여, 상여, 성과가 있는 케이스
    case_list = "|".join(["급여", "상여", "성과", "월급"])
    case_26_index = df[((df["적요_pre"].str.startswith(("(주)", "（주）", "㈜", "주식회사", "주）"))) | 
                        (df["적요_pre"].str.endswith(("(주)", "（주）", "㈜", "주식회사", "주）")))) &
                    (df["적요_pre"].str.contains(case_list))].index.tolist()
    case_26 = df[df.index.isin(case_26_index)].copy()
    case_26.to_csv("./data/case/case_26.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_26_index)]


    # (주)로 끝나는 케이스
    case_27_index = df[(df["적요_pre"].str.endswith(("(주)", "（주）", "㈜", "주식회사", "주）", "주식회")))].index.tolist()
    case_27 = df[df.index.isin(case_27_index)].copy()
    case_27.to_csv("./data/case/case_27.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_27_index)]


    # (주)로 시작하는 케이스
    case_27_1_index = df[(df["적요_pre"].str.startswith(("(주)", "（주）", "㈜", "주식회사", "주）")))].index.tolist()
    case_27_1 = df[df.index.isin(case_27_1_index)].copy()
    case_27_1.to_csv("./data/case/case_27_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_27_1_index)]


    # 세무서로 끝나는 케이스
    case_28_index = df[(df["적요_pre"].str.endswith(("세무서")))].index.tolist()
    case_28 = df[df.index.isin(case_28_index)].copy()
    case_28.to_csv("./data/case/case_28.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_28_index)]



    # 축하금으로 끝나는 케이스
    case_29_index = df[(df["적요_pre"].str.endswith("축하금"))].index.tolist()
    case_29 = df[df.index.isin(case_29_index)].copy()
    case_29.to_csv("./data/case/case_29.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_29_index)]



    # 장려금으로 끝나는 케이스
    case_30_index = df[(df["적요_pre"].str.endswith("장려금"))].index.tolist()
    case_30 = df[df.index.isin(case_30_index)].copy()
    case_30.to_csv("./data/case/case_30.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_30_index)]



    # 포상금으로 끝나는 케이스
    case_31_index = df[(df["적요_pre"].str.endswith("포상금"))].index.tolist()
    case_31 = df[df.index.isin(case_31_index)].copy()
    case_31.to_csv("./data/case/case_31.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_31_index)]



    # 세무로 끝나거나 시작하는 케이스
    case_32_index = df[((df["적요_pre"].str.endswith("세무")) | 
                        (df["적요_pre"].str.startswith("세무")))].index.tolist()
    case_32 = df[df.index.isin(case_32_index)].copy()
    case_32.to_csv("./data/case/case_32.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_32_index)]



    # 농협-농협으로 시작하는 케이스
    case_33_index = df[(df["적요_pre"].str.startswith("농협-농협"))].index.tolist()
    case_33 = df[df.index.isin(case_33_index)].copy()
    case_33.to_csv("./data/case/case_33.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_33_index)]



    # 은행명으로 시작하고 2번째가 -로 시작하면서 개인간입금 단어가 있는 케이스
    case_34_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str.contains(indi_word_for_contains))].index.tolist()
    case_34 = df[df.index.isin(case_34_index)].copy()
    case_34.to_csv("./data/case/case_34.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_34_index)]



    # 은행명으로 시작하고 2번째가 -로 시작하면서 길이가 4인 케이스
    case_35_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) &  
                    (df["적요길이"]==4)].index.tolist()
    case_35 = df[df.index.isin(case_35_index)].copy()
    case_35.to_csv("./data/case/case_35.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_35_index)]



    # 은행명으로 시작하고 2번째가 -로 시작하면서 이름이 들어있는 케이스
    case_36_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－"))) & 
                    (df["적요_pre"].apply(lambda x: find_name(x[3:])))].index.tolist()
    case_36 = df[df.index.isin(case_36_index)].copy()
    case_36.to_csv("./data/case/case_36.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_36_index)]



    # 보상금으로 끝나는 케이스
    case_37_index = df[(df["적요_pre"].str.endswith("보상금"))].index.tolist()
    case_37 = df[df.index.isin(case_37_index)].copy()
    case_37.to_csv("./data/case/case_37.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_37_index)]



    # 은행명으로 시작하고 길이가 5인 케이스
    case_38_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요길이"]==5)].index.tolist()
    case_38 = df[df.index.isin(case_38_index)].copy()
    case_38.to_csv("./data/case/case_38.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_38_index)]



    # 급여로 끝나는 케이스
    case_39_index = df[((df["적요_pre"].str.endswith("급여")))].index.tolist()
    case_39 = df[df.index.isin(case_39_index)].copy()
    case_39.to_csv("./data/case/case_39.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_39_index)]


    # 월급여, 급여로 시작하는 케이스
    case_39_1_index = df[(df["적요_pre"].str.startswith("급여")) |
                         (df["적요_pre"].str.startswith("월급여"))].index.tolist()
    case_39_1 = df[df.index.isin(case_39_1_index)].copy()
    case_39_1.to_csv("./data/case/case_39_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_39_1_index)]


    # 연말정산으로 끝나는 케이스
    case_40_index = df[(df["적요_pre"].str.endswith("연말정산"))].index.tolist()
    case_40 = df[df.index.isin(case_40_index)].copy()
    case_40.to_csv("./data/case/case_40.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_40_index)]


    # 특별상여금, 명절상여금, 성과상여금, 근로상여금으로 끝나는 케이스
    case_41_index = df[((df["적요_pre"].str.endswith(("특별상여금", "명절상여금", "성과상여금", "근로상여금"))))].index.tolist()
    case_41 = df[df.index.isin(case_41_index)].copy()
    case_41.to_csv("./data/case/case_41.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_41_index)]


    # 상여금으로 끝나는 케이스
    case_41_1_index = df[((df["적요_pre"].str.endswith("상여금")))].index.tolist()
    case_41_1 = df[df.index.isin(case_41_1_index)].copy()
    case_41_1.to_csv("./data/case/case_41_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_41_1_index)]



    # 성과금, 성과급으로 끝나고 길이가 4이상인 케이스
    case_42_index = df[(df["적요_pre"].str.endswith(("성과금", "성과급")))].index.tolist()
    case_42 = df[df.index.isin(case_42_index)].copy()
    case_42.to_csv("./data/case/case_42.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_42_index)]



    # 인센티브로 끝나는 케이스
    case_43_index = df[((df["적요_pre"].str.endswith("인센티브")))].index.tolist()
    case_43 = df[df.index.isin(case_43_index)].copy()
    case_43.to_csv("./data/case/case_43.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_43_index)]


    # 인센티브로 시작하는는 케이스
    case_43_1_index = df[(df["적요_pre"].str.startswith("인센티브"))].index.tolist()
    case_43_1 = df[df.index.isin(case_43_1_index)].copy()
    case_43_1.to_csv("./data/case/case_43_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_43_1_index)]
    
    
    # 등록금으로 끝나는 케이스
    case_44_index = df[(df["적요_pre"].str.endswith("등록금"))].index.tolist()
    case_44 = df[df.index.isin(case_44_index)].copy()
    case_44.to_csv("./data/case/case_44.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_44_index)]


    # 연말정산으로 시작하는 케이스
    case_45_index = df[(df["적요_pre"].str.startswith("연말정산"))].index.tolist()
    case_45 = df[df.index.isin(case_45_index)].copy()
    case_45.to_csv("./data/case/case_45.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_45_index)]



    # 월급으로 끝나는 케이스
    case_46_index = df[(df["적요_pre"].str.endswith("학교"))].index.tolist()
    case_46 = df[df.index.isin(case_46_index)].copy()
    case_46.to_csv("./data/case/case_46.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_46_index)]



    # 보조금으로 끝나는 케이스
    case_47_index = df[(df["적요_pre"].str.endswith("보조금"))].index.tolist()
    case_47 = df[df.index.isin(case_47_index)].copy()
    case_47.to_csv("./data/case/case_47.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_47_index)]



    # DB손보로 시작하고 길이가 5이상인 케이스
    case_48_index = df[(df["적요_pre"].str.startswith("DB손보"))].index.tolist()
    case_48 = df[df.index.isin(case_48_index)].copy()
    case_48.to_csv("./data/case/case_48.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_48_index)]



    # 증권으로 끝나는 케이스
    case_49_index = df[(df["적요_pre"].str.endswith("증권"))].index.tolist()
    case_49 = df[df.index.isin(case_49_index)].copy()
    case_49.to_csv("./data/case/case_49.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_49_index)]



    # KB증으로 시작하고 길이가 6인 케이스
    case_50_index = df[(df["적요_pre"].str.startswith("KB증")) & 
                    (df["적요길이"]==6)].index.tolist()
    case_50 = df[df.index.isin(case_50_index)].copy()
    case_50.to_csv("./data/case/case_50.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_50_index)]



    # ＹＭＣＡ, ＹＷＣＡ로 끝나는 케이스
    case_51_index = df[(df["적요_pre"].str.endswith(("ＹＭＣＡ", "ＹＷＣＡ")))].index.tolist()
    case_51 = df[df.index.isin(case_51_index)].copy()
    case_51.to_csv("./data/case/case_51.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_51_index)]



    # 격려금으로 끝나는 케이스
    case_52_index = df[(df["적요_pre"].str.endswith("격려금"))].index.tolist()
    case_52 = df[df.index.isin(case_52_index)].copy()
    case_52.to_csv("./data/case/case_52.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_52_index)]



    # 2번째가 우유, 유업로 시작하고 길이가 6인 케이스
    pattern = r'^.{2}(우유|유업)'
    case_53_index = df[(df["적요_pre"].str.match(pattern, na=False)) & 
                    (df["적요길이"]==6)].index.tolist()
    case_53 = df[df.index.isin(case_53_index)].copy()
    case_53.to_csv("./data/case/case_53.csv", encoding="utf-8-sig")
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
    case_54.to_csv("./data/case/case_54.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_54_index)]



    # 봉사, 공로, 복지, 조교, 근로, 학과 장학금으로 끝나는 케이스
    case_55_index = df[((df["적요_pre"].str.endswith(("봉사장학금", "공로장학금", "복지장학금", "조교장학금", "근로장학금", "학과장학금",))))].index.tolist()
    case_55 = df[df.index.isin(case_55_index)].copy()
    case_55.to_csv("./data/case/case_55.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_55_index)]


    # 장학금으로 끝나는 케이스
    case_55_1_index = df[((df["적요_pre"].str.endswith("장학금")))].index.tolist()
    case_55_1 = df[df.index.isin(case_55_1_index)].copy()
    case_55_1.to_csv("./data/case/case_55_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_55_1_index)]


    # 연차수당으로 끝나고 길이가 5이상인 케이스
    case_56_index = df[((df["적요_pre"].str.endswith("연차수당")))].index.tolist()
    case_56 = df[df.index.isin(case_56_index)].copy()
    case_56.to_csv("./data/case/case_56.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_56_index)]



    # 경비로 끝나는 케이스
    case_57_index = df[((df["적요_pre"].str.endswith("경비")))].index.tolist()
    case_57 = df[df.index.isin(case_57_index)].copy()
    case_57.to_csv("./data/case/case_57.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_57_index)]



    # 특별상여로 끝나는 케이스
    case_58_index = df[(df["적요_pre"].str.endswith("특별상여"))].index.tolist()
    case_58 = df[df.index.isin(case_58_index)].copy()
    case_58.to_csv("./data/case/case_58.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_58_index)]



    # 후원금으로 끝나는 케이스
    case_59_index = df[((df["적요_pre"].str.endswith("후원금")))].index.tolist()
    case_59 = df[df.index.isin(case_59_index)].copy()
    case_59.to_csv("./data/case/case_59.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_59_index)]



    # 설상여로 끝나는 케이스
    case_60_index = df[((df["적요_pre"].str.endswith("설상여")))].index.tolist()
    case_60 = df[df.index.isin(case_60_index)].copy()
    case_60.to_csv("./data/case/case_60.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_60_index)]



    # 환불로 끝나는 케이스
    case_61_index = df[(df["적요_pre"].str.endswith("환불"))].index.tolist()
    case_61 = df[df.index.isin(case_61_index)].copy()
    case_61.to_csv("./data/case/case_61.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_61_index)]



    # 휴가비로 끝나고 길이가 4이상인 케이스
    case_62_index = df[((df["적요_pre"].str.endswith("휴가비")) & 
                        (df["적요길이"]>2))].index.tolist()
    case_62 = df[df.index.isin(case_62_index)].copy()
    case_62.to_csv("./data/case/case_62.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_62_index)]



    # 명절상여로 끝나고 길이가 4이상인 케이스
    case_63_index = df[((df["적요_pre"].str.endswith("명절상여"))) & 
                    (df["적요길이"]>4)].index.tolist()
    case_63 = df[df.index.isin(case_63_index)].copy()
    case_63.to_csv("./data/case/case_63.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_63_index)]



    # 사단법인으로 시작하는 케이스
    case_64_index = df[(df["적요_pre"].str.startswith(("(사)", "（사）", "사단법인", "사）"))) | 
                    (df["적요_pre"].str.endswith(("(사)", "（사）", "사단법인", "사）")))].index.tolist()
    case_64 = df[df.index.isin(case_64_index)].copy()
    case_64.to_csv("./data/case/case_64.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_64_index)]



    # 저축은행으로 끝나는 케이스
    case_65_index = df[(df["적요_pre"].str.endswith("저축은행"))].index.tolist()
    case_65 = df[df.index.isin(case_65_index)].copy()
    case_65.to_csv("./data/case/case_65.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_65_index)]



    # 정보통신으로 끝나고 길이가 9이하인 케이스
    case_66_index = df[(df["적요_pre"].str.endswith("정보통신")) & 
                    (df["적요길이"]<10)].index.tolist()
    case_66 = df[df.index.isin(case_66_index)].copy()
    case_66.to_csv("./data/case/case_66.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_66_index)]



    # 통신비지원, 통신비지원금으로 끝나는 케이스
    case_67_index = df[(df["적요_pre"].str.endswith(("통신비지원금", "통신비지원")))].index.tolist()
    case_67 = df[df.index.isin(case_67_index)].copy()
    case_67.to_csv("./data/case/case_67.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_67_index)]



    # 통신비가 있는 케이스
    # case_list = "|".join(["통신비", "SKT", "LGU"])
    case_67_1_index = df[(df["적요_pre"].str.contains("통신비"))].index.tolist()
    case_67_1 = df[df.index.isin(case_67_1_index)].copy()
    case_67_1.to_csv("./data/case/case_67_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_67_1_index)]



    # 명절수당으로 끝나는 케이스
    case_68_index = df[(df["적요_pre"].str.endswith("명절수당"))].index.tolist()
    case_68 = df[df.index.isin(case_68_index)].copy()
    case_68.to_csv("./data/case/case_68.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_68_index)]



    # 추가상여, 정기상여, 성과상여, 급여상여로 끝나는 케이스
    case_69_index = df[(df["적요_pre"].str.endswith(("추가상여", "정기상여", "성과상여", "급여상여", )))].index.tolist()
    case_69 = df[df.index.isin(case_69_index)].copy()
    case_69.to_csv("./data/case/case_69.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_69_index)]



    # 상여로 끝나고 길이가 5이상인 케이스
    case_69_1_index = df[(df["적요_pre"].str.endswith(("상여")) &
                        (df["적요길이"]>4))].index.tolist()
    case_69_1 = df[df.index.isin(case_69_1_index)].copy()
    case_69_1.to_csv("./data/case/case_69_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_69_1_index)]



    # 상여로 끝나는 케이스
    case_69_2_index = df[df["적요_pre"].str.endswith(("상여"))].index.tolist()
    case_69_2 = df[df.index.isin(case_69_2_index)].copy()
    case_69_2.to_csv("./data/case/case_69_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_69_2_index)]



    # 수수료로 끝나는 케이스
    case_70_index = df[(df["적요_pre"].str.endswith("수수료"))].index.tolist()
    case_70 = df[df.index.isin(case_70_index)].copy()
    case_70.to_csv("./data/case/case_70.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_70_index)]



    # 알바비로 끝나고 길이가 6이상인 케이스
    case_71_index = df[(df["적요_pre"].str.endswith("알바비"))].index.tolist()
    case_71 = df[df.index.isin(case_71_index)].copy()
    case_71.to_csv("./data/case/case_71.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_71_index)]



    # 관리비로 끝나고 길이가 6이상인 케이스
    case_72_index = df[(df["적요_pre"].str.endswith("관리비"))].index.tolist()
    case_72 = df[df.index.isin(case_72_index)].copy()
    case_72.to_csv("./data/case/case_72.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_72_index)]



    # 상여금이나 상여로 시작하고 길이가 5이상인 케이스
    case_73_index = df[df["적요_pre"].str.startswith(("상여금", "상여")) &
                        (df["적요길이"]>4)].index.tolist()
    case_73 = df[df.index.isin(case_73_index)].copy()
    case_73.to_csv("./data/case/case_73.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_73_index)]



    # 근로, 근무수당으로 끝나는 케이스
    case_74_index = df[(df["적요_pre"].str.endswith(("근로수당", "근무수당")))].index.tolist()
    case_74 = df[df.index.isin(case_74_index)].copy()
    case_74.to_csv("./data/case/case_74.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_74_index)]



    # 방과후로 끝나거나 시작하는 케이스
    case_75_index = df[(df["적요_pre"].str.startswith("방과후")) | 
                    (df["적요_pre"].str.endswith("방과후"))].index.tolist()
    case_75 = df[df.index.isin(case_75_index)].copy()
    case_75.to_csv("./data/case/case_75.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_75_index)]



    # 유치원으로 끝나는 케이스
    case_76_index = df[(df["적요_pre"].str.endswith("유치원"))].index.tolist()
    case_76 = df[df.index.isin(case_76_index)].copy()
    case_76.to_csv("./data/case/case_76.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_76_index)]



    # 은행명으로 시작하고 뒤에 이름이 있는 경우
    case_77_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].apply(lambda x: find_name(x[2:])))].index.tolist()
    case_77 = df[df.index.isin(case_77_index)].copy()
    case_77.to_csv("./data/case/case_77.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_77_index)]



    # 은행명으로 시작하고 두번째가 -인 경우
    case_78_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("-", "－")))].index.tolist()
    case_78 = df[df.index.isin(case_78_index)].copy()
    case_78.to_csv("./data/case/case_78.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_78_index)]



    # 교육관련 비용으로 끝나는 경우
    case_79_index = df[(df["적요_pre"].str.endswith(tuple(ede_word_for_contains.split("|"))))].index.tolist()
    case_79 = df[df.index.isin(case_79_index)].copy()
    case_79.to_csv("./data/case/case_79.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_79_index)]



    # 00급여로 시작하는 케이스
    case_80_index = df[(df["적요_pre"].str.startswith(("명절급여", "정기급여", "정산급여", "직원급여", "개인급여")))].index.tolist()
    case_80 = df[df.index.isin(case_80_index)].copy()
    case_80.to_csv("./data/case/case_80.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_index)]




    # 월급으로 시작하는 케이스
    case_80_1_index = df[(df["적요_pre"].str.startswith("월급"))].index.tolist()
    case_80_1 = df[df.index.isin(case_80_1_index)].copy()
    case_80_1.to_csv("./data/case/case_80_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_1_index)]




    # 월급으로 끝나는 케이스
    case_80_2_index = df[(df["적요_pre"].str.endswith("월급"))].index.tolist()
    case_80_2 = df[df.index.isin(case_80_2_index)].copy()
    case_80_2.to_csv("./data/case/case_80_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_2_index)]




    # 급여가 있는 케이스
    case_80_3_index = df[(df["적요_pre"].str.contains("급여"))].index.tolist()
    case_80_3 = df[df.index.isin(case_80_3_index)].copy()
    case_80_3.to_csv("./data/case/case_80_3.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_80_3_index)]




    # 00복지관으로 끝나는 경우
    case_81_index = df[(df["적요_pre"].str.endswith(("시각복지관", "실버복지관", "노인복지관", "장애인복지관", \
                                                    "노인종합복지관", "장애인복합복지관", "사회복지관", \
                                                    "종합사회복지관", "종합복지관")))].index.tolist()
    case_81 = df[df.index.isin(case_81_index)].copy()
    case_81.to_csv("./data/case/case_81.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_81_index)]



    # 복지관으로 끝나는 경우
    case_81_1_index = df[(df["적요_pre"].str.endswith("복지관"))].index.tolist()
    case_81_1 = df[df.index.isin(case_81_1_index)].copy()
    case_81_1.to_csv("./data/case/case_81_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_81_1_index)]



    # 성과급으로 시작
    case_82_index = df[(df["적요_pre"].str.startswith("성과급"))].index.tolist()
    case_82 = df[df.index.isin(case_82_index)].copy()
    case_82.to_csv("./data/case/case_82.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_82_index)]



    # 천주교회, 중앙교회, 교회로 끝나는 케이스
    case_83_index = df[(df["적요_pre"].str.endswith(("천주교회", "중앙교회", "교회")))].index.tolist()
    case_83 = df[df.index.isin(case_83_index)].copy()
    case_83.to_csv("./data/case/case_83.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_83_index)]



    # 금융사명 뒤에 ( 로 시작하는 케이스
    case_84_index = df[(df["적요_pre"].str.startswith(tuple(bank_dict.keys()))) & 
                    (df["적요_pre"].str[2].isin(("(", "（")))].index.tolist()
    case_84 = df[df.index.isin(case_84_index)].copy()
    case_84.to_csv("./data/case/case_84.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_84_index)]



    # 삼성금융으로 시작하는 경우
    case_85_index = df[(df["적요_pre"].str.startswith("삼성금융"))].index.tolist()
    case_85 = df[df.index.isin(case_85_index)].copy()
    case_85.to_csv("./data/case/case_85.csv", encoding="utf-8-sig")
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
    case_86.to_csv("./data/case/case_86.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_86_index)]



    # 대출소개로 시작하는 경우
    case_87_index = df[(df["적요_pre"].str.startswith("대출소개"))].index.tolist()
    case_87 = df[df.index.isin(case_87_index)].copy()
    case_87.to_csv("./data/case/case_87.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_87_index)]



    # 중진공으로 시작하는 경우
    case_88_index = df[(df["적요_pre"].str.startswith("중진공"))].index.tolist()
    case_88 = df[df.index.isin(case_88_index)].copy()
    case_88.to_csv("./data/case/case_88.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_88_index)]



    # 00수당으로 끝나고 길이가 4이상인 케이스
    case_89_index = df[(df["적요_pre"].str.endswith(("야근수당", "연구수당", "업무수당", "직무수당", \
                                                    "특별수당", "연수수당", "강의수당", "관리수당", \
                                                    "직책수당", "참석수당", "교육수당", "복지수당"))) &
                    (df["적요길이"]>3)].index.tolist()
    case_89 = df[df.index.isin(case_89_index)].copy()
    case_89.to_csv("./data/case/case_89.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_89_index)]



    # 수당으로 끝나고 길이가 4인 케이스
    case_89_1_index = df[(df["적요_pre"].str.endswith("수당")) &
                    (df["적요길이"]==4)].index.tolist()
    case_89_1 = df[df.index.isin(case_89_1_index)].copy()
    case_89_1.to_csv("./data/case/case_89_1.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_89_1_index)]


    # 수당으로 끝나고 길이가 4 이상인 케이스
    case_89_2_index = df[(df["적요_pre"].str.endswith("수당")) &
                    (df["적요길이"]>3)].index.tolist()
    case_89_2 = df[df.index.isin(case_89_2_index)].copy()
    case_89_2.to_csv("./data/case/case_89_2.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_89_2_index)]


    # ＣＪ로 시작하는 경우
    case_90_index = df[(df["적요_pre"].str.startswith("ＣＪ"))].index.tolist()
    case_90 = df[df.index.isin(case_90_index)].copy()
    case_90.to_csv("./data/case/case_90.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_90_index)]



    # DLIVE로 시작하는 경우
    case_91_index = df[(df["적요_pre"].str.startswith("DLIVE"))].index.tolist()
    case_91 = df[df.index.isin(case_91_index)].copy()
    case_91.to_csv("./data/case/case_91.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_91_index)]



    # 청약으로 끝나는 경우
    case_92_index = df[(df["적요_pre"].str.endswith("청약"))].index.tolist()
    case_92 = df[df.index.isin(case_92_index)].copy()
    case_92.to_csv("./data/case/case_92.csv", encoding="utf-8-sig")
    df = df[~df.index.isin(case_92_index)]
    
    df.to_csv("./data/case/etc.csv", encoding="utf-8-sig")







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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
                token_1 = text_pre[0:2]
                for j in sala_word_for_contains.split("|"):
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
                                '적요 설명': "%s 계좌에서 급여 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 급여 이체한 내역의 적요이다."%token_1_mean,
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
                                    '적요 설명': "%s 계좌에서 급여 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 급여 이체한 내역의 적요이다."%token_1_mean,
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
                                '적요 설명': "%s 계좌에서 급여 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 급여 이체한 내역의 적요이다."%token_1_mean,
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
    new_path = "./result/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df





def case_6_1(path):
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
                for j in bonu_word_for_contains.split("|"):
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
                                '적요 설명': "%s 계좌에서 상여금이 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 상여금을 이체한 내역의 적요이다."%token_1_mean,
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
                                    '적요 설명': "%s 계좌에서 상여금이 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 상여금을 이체한 내역의 적요이다."%token_1_mean,
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
                                '적요 설명': "%s 계좌에서 상여금이 입금된 내역의 적요이다."%token_1_mean if tran_diff == "입금" else "%s 계좌로 상여금을 이체한 내역의 적요이다."%token_1_mean,
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        text_pre = text_pre.replace("발전기금", " 발전기금 ")
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
            elif tokens[i] in ["발전기금"]:
                tokens_mean.append("발전기금")
                object_mean.append("발전기금")
            else:
                tokens_mean.append("학교명")
                object_mean.append("학교명")
        
        for i in range(len(tokens)):
                new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': tokens[0]+"에서 발전기금이 입금된 내역의 적요이다." if tran_diff == "입금" else tokens[0]+"(으)로 발전기금을 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
                
        text_pre = text_pre.replace("세무서", " 세무서 ")
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
            elif tokens[i] in ["세무서"]:
                tokens_mean.append("세무서")
                object_mean.append("세무서")
            elif tokens[i] in ["주"]:
                tokens_mean.append("주식회사")
                object_mean.append("주식회사")
            else:
                tokens_mean.append("지역명")
                object_mean.append("지역명")
        
        for i in range(len(tokens)):
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
                                '단어': tokens[i],
                                '단어일련번호':i,
                                '단어의미':tokens_mean[i],
                                '개체명': object_mean[i],
                                '완료여부':1,
                                }, ignore_index=True)

        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "./result/case"
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
        
        tokens = del_sw(text_pre.replace("축하금", ""))

        
        token_2 = "축하금"
        token_2_mean = "축하금"
        object_2 = "금융용어"

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
                                    '적요 설명': "축하금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "축하금으로 이체한 내역의 적요이다.",
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
                                '적요 설명': "축하금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "축하금으로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
        

                
        tokens = del_sw(text_pre.replace("장려금", ""))

        
        token_2 = "장려금"
        token_2_mean = "장려금"
        object_2 = "금융용어"

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
                                    '적요 설명': "장려금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "장려금으로 이체한 내역의 적요이다.",
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
                                '적요 설명': "장려금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "장려금으로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
        
                
        tokens = del_sw(text_pre.replace("포상금", ""))

        
        token_2 = "포상금"
        token_2_mean = "포상금"
        object_2 = "금융용어"

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
                                    '적요 설명': "포상금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "포상금으로 이체한 내역의 적요이다.",
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
                                '적요 설명': "포상금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "포상금으로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        token_1 = text_pre.replace("보상금", "")
        token_2 = "보상금"
        
        token_1_mean = token_1
        object_1 = "사유"
        token_2_mean = token_2
        object_2 = "금융용어"

        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "보상금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "보상금으로 이체한 내역의 적요이다.",
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
                                '적요 설명': "보상금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "보상금으로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        token_2 = "인센티브"
        token_2_mean = token_2
        object_2 = "금융용어"
        
        tokens = del_sw(text_pre.replace("인센티브", ""))

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
                                    '적요 설명': "인센티브로 입금된 내역의 적요이다." if tran_diff == "입금" else "인센티브로 이체한 내역의 적요이다.",
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
        
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        token_2 = "등록금"
        token_2_mean = token_2
        object_2 = "금융용어"   
        
        tokens = del_sw(text_pre.replace("등록금", ""))
        
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
                                    '적요 설명': "등록금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "등록금으로 이체한 내역의 적요이다.",
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
                                '적요 설명': "등록금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "등록금으로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df



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
        
        token_1 = "보조금"
        token_1_mean = token_1
        object_1 = "금융용어"   
        
        tokens = del_sw(text_pre.replace("보조금", ""))
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': "보조금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "보조금으로 이체한 내역의 적요이다.",
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
                                    '적요 설명': "보조금으로 입금된 내역의 적요이다." if tran_diff == "입금" else "보조금으로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        token_2 = "격려금"
        token_2_mean = "격려금"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        token_2 = "경비"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
        
        token_2 = "휴가비"
        token_2_mean = "휴가비"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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


        token_2 = "수수료"
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
                                    '적요 설명': "수수료로 입금된 내역의 적요이다." if tran_diff == "입금" else "수수료를 이체한 내역의 적요이다.",
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
                                '적요 설명': "수수료로 입금된 내역의 적요이다." if tran_diff == "입금" else "수수료를 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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

        token_2 = "알바비"
        token_2_mean = "아르바이트비"
        object_2 = "금융용어"
        
        token_1 = del_sw(text_pre.replace(token_2, ""))
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
                                    '적요 설명': "아르바이트비 로 입금된 내역의 적요이다." if tran_diff == "입금" else "아르바이트비 로 이체한 내역의 적요이다.",
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
                                '적요 설명': "아르바이트비 로 입금된 내역의 적요이다." if tran_diff == "입금" else "아르바이트비 로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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

        token_2 = "관리비"
        token_2_mean = token_2
        object_2 = "금융용어"
        
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
                                    '적요 설명': "관리비로 입금된 내역의 적요이다." if tran_diff == "입금" else "관리비로 이체한 내역의 적요이다.",
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
                                '적요 설명': "관리비로 입금된 내역의 적요이다." if tran_diff == "입금" else "관리비로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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

        token_1 = text_pre[0:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "은행명"
        
        tokens = del_sw(text_pre[2:])
        
        

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

            
            
    result_file_name = os.path.basename(path).split(".")[0]+"_complete.csv"
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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


        token_1 = text_pre[:2]
        token_1_mean = bank_dict.get(token_1, token_1)
        object_1 = "금융기관"
        
        token_2 = text_pre[2:5]
        token_2_mean = "주식회사"
        object_2 = "금융용어"

        tokens = del_sw(text_pre[4:])

        
        
        new_df = new_df.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': token_1_mean+" 계좌에서 회사로 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 회사로 이체한 내역의 적요이다.",
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
                                '적요 설명': token_1_mean+" 계좌에서 회사로 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 회사로 이체한 내역의 적요이다.",
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
                                    '적요 설명': token_1_mean+" 계좌에서 회사로 입금된 내역의 적요이다." if tran_diff == "입금" else token_1_mean+" 계좌로 회사로 이체한 내역의 적요이다.",
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
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
    new_path = "./result/case"
    result_path = os.path.join(new_path, result_file_name)
    new_df.to_csv(result_path, encoding="utf-8-sig")
    return new_df


if __name__ == "__main__":
    # split_data("./data/alldata.csv")
    # case_1("./data/case/case_1.csv")
    # case_1_1("./data/case/case_1_1.csv")
    # case_2("./data/case/case_2.csv")
    # case_3("./data/case/case_3.csv")
    # case_4("./data/case/case_4.csv")
    # case_5("./data/case/case_5.csv")
    # case_6("./data/case/case_6.csv")
    # case_6_1("./data/case/case_6_1.csv")
    # case_7("./data/case/case_7.csv")
    # case_8("./data/case/case_8.csv")
    # case_9("./data/case/case_9.csv")
    # case_10("./data/case/case_10.csv")
    # case_10_1("./data/case/case_10_1.csv")
    # case_10_2("./data/case/case_10_2.csv")
    # case_11("./data/case/case_11.csv")
    # case_12("./data/case/case_12.csv")
    case_13("./data/case/case_13.csv")
    # case_14("./data/case/case_14.csv")
    # case_15("./data/case/case_15.csv")
    # case_16("./data/case/case_16.csv")
    # case_17("./data/case/case_17.csv")
    # case_18("./data/case/case_18.csv")
    # case_19("./data/case/case_19.csv")
    # case_20("./data/case/case_20.csv")
    # case_21("./data/case/case_21.csv")
    # case_21_1("./data/case/case_21_1.csv")
    # case_22("./data/case/case_22.csv")
    # case_23("./data/case/case_23.csv")
    # case_24("./data/case/case_24.csv")
    # case_25("./data/case/case_25.csv")
    # case_26("./data/case/case_26.csv")
    # case_27("./data/case/case_27.csv")
    # case_27_1("./data/case/case_27_1.csv")
    # case_28("./data/case/case_28.csv")
    # case_29("./data/case/case_29.csv")
    # case_30("./data/case/case_30.csv")
    # case_31("./data/case/case_31.csv")
    # case_32("./data/case/case_32.csv")
    # case_33("./data/case/case_33.csv")
    # case_34("./data/case/case_34.csv")
    # case_35("./data/case/case_35.csv")
    # case_36("./data/case/case_36.csv")
    # case_37("./data/case/case_37.csv")
    # case_38("./data/case/case_38.csv")
    # case_39("./data/case/case_39.csv")
    # case_39_1("./data/case/case_39_1.csv")
    # case_40("./data/case/case_40.csv")
    # case_41("./data/case/case_41.csv")
    # case_41_1("./data/case/case_41_1.csv")
    # case_42("./data/case/case_42.csv")
    # case_43("./data/case/case_43.csv")
    # case_43_1("./data/case/case_43_1.csv")
    # case_44("./data/case/case_44.csv")
    # case_45("./data/case/case_45.csv")
    # case_46("./data/case/case_46.csv")
    # case_47("./data/case/case_47.csv")
    # case_48("./data/case/case_48.csv")
    # case_49("./data/case/case_49.csv")
    # case_50("./data/case/case_50.csv")
    # case_51("./data/case/case_51.csv")
    # case_52("./data/case/case_52.csv")
    # case_53("./data/case/case_53.csv")
    # case_54("./data/case/case_54.csv")
    # case_55("./data/case/case_55.csv")
    # case_55_1("./data/case/case_55_1.csv")
    # case_56("./data/case/case_56.csv")
    # case_57("./data/case/case_57.csv")
    # case_58("./data/case/case_58.csv")
    # case_59("./data/case/case_59.csv")
    # case_60("./data/case/case_60.csv")
    # case_61("./data/case/case_61.csv")
    # case_62("./data/case/case_62.csv")
    # case_63("./data/case/case_63.csv")
    # case_64("./data/case/case_64.csv")
    # case_65("./data/case/case_65.csv")
    # case_66("./data/case/case_66.csv")
    # case_67("./data/case/case_67.csv")
    # case_67_1("./data/case/case_67_1.csv")
    # case_68("./data/case/case_68.csv")
    # case_69("./data/case/case_69.csv")
    # case_69_1("./data/case/case_69_1.csv")
    # case_69_2("./data/case/case_69_2.csv")
    # case_70("./data/case/case_70.csv")
    # case_71("./data/case/case_71.csv")
    # case_72("./data/case/case_72.csv")
    # case_73("./data/case/case_73.csv")
    # case_74("./data/case/case_74.csv")
    # case_75("./data/case/case_75.csv")
    # case_76("./data/case/case_76.csv")
    # case_77("./data/case/case_77.csv")
    # case_78("./data/case/case_78.csv")
    # case_79("./data/case/case_79.csv")
    # case_80("./data/case/case_80.csv")
    # case_80_1("./data/case/case_80_1.csv")
    # case_80_2("./data/case/case_80_2.csv")
    # case_80_3("./data/case/case_80_3.csv")
    # case_81("./data/case/case_81.csv")
    # case_81_1("./data/case/case_81_1.csv")
    # case_82("./data/case/case_82.csv")
    # case_83("./data/case/case_83.csv")
    # case_84("./data/case/case_84.csv")
    # case_85("./data/case/case_85.csv")
    # case_86("./data/case/case_86.csv")
    # case_87("./data/case/case_87.csv")
    # case_88("./data/case/case_88.csv")
    # case_89("./data/case/case_89.csv")
    # case_89_1("./data/case/case_89_1.csv")
    # case_89_2("./data/case/case_89_2.csv")
    # case_90("./data/case/case_90.csv")
    # case_91("./data/case/case_91.csv")
    # case_92("./data/case/case_92.csv")

