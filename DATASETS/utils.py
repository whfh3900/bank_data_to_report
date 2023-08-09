
import re
import unicodedata
from ats_module.text_preprocessing import *
nk = Nickonlpy(base=False)

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
cost_word_for_contains = "|".join(["축하금", "장려금", "포상금", "퇴직금", "정산금", "교부금", "할부금", \
                                    "한국전자금", "성과금", "등록금", "보조금", "격려금", "환불금", "증거금", \
                                    "후원금", "경조금", "회수금", "시상금", "기부금", "비상금", "분배금", \
                                    "학자금", "보증금", "배당금", "대여금", "지원금", "전도금", "지급금", \
                                    "예치금", "일시금", "환급금", "초과금", "추가금", "현금", "양도금", \
                                    "수익금", "상환금", "반환금", "보험금", "방송헌금", "헌금", "전별금", \
                                    "입학금", "예치금", "대출금", "건축금", "정착금", "연차금", "복지금", \
                                    "공제금", "적금", "저금", "축의금", "조의금", "사은금", "공과금", "잔금", \
                                    "지원금", "대부금", "적립금", "원리금", "위로금", "사례금", "배려금", \
                                    "충당금", "부담금", "추납금", "상납금", "반납금", "공납금", "보관금", \
                                    "출금", "부의금", "부원금", "예수금", "보상금", "특별금", "임대금",  \
                                    "교무금", "협력금", "자금", "납입금", "선입금", "임금", "분납금", \
                                    "주택부금", "세금", "의무금", "공동모금"])

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