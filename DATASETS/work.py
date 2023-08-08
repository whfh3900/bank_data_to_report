import pandas as pd
from tqdm import tqdm 
from ats_module.text_preprocessing import *
nk = Nickonlpy(base=False)


##################################################### 전처리 함수
# lambda에서 사용할 전처리 함수
def lambda_preprocessing_2(text):
    
    text = find_null(text)
    text = ascii_check(text)
    text = change_upper(text)
    # text = remove_bank(text)
    # text = corporatebody(text)
    text = numbers_to_zero(text)
    text = remove_specialchar(text)
    text = find_null(text)
    result = nk.post.pos(text)
    text = " ".join([i[0] for i in result])
    pos = [i[1] for i in result]
    
    return text, pos

def has_bank(text):
    banks = ['카카','SC','KB','KB증','국민','우체','대신','수협','삼성','신협','농협','NH투자증권', '경남', '광주', '금고', 
             '부산', '산업', '신한', '씨티', '전북', '하나', 'ＳＣ', '기업', '미래', '산림', '산업', '삼성', '국고', '대구', '조흥']
    
    result = False
    bank = False
    name = False
    
    for n in banks:
        if text.startswith(n):
            name = text.replace(n, "")
            bank = n
            result = True
            break
    
    return result, (bank, name)

def change_bank_name(text):
    if text == '카카':
        return '카카오뱅크'
    elif text == 'SC':
        return 'SC제일은행'
    elif text == 'KB':
        return 'KB국민은행'
    elif text == 'KB증':
        return 'KB증권'
    elif text == '국민':
        return 'KB국민은행'
    elif text == '우체':
        return '우체국'
    elif text == '대신':
        return '대신증권'
    elif text == '미래':
        return '미래에셋'
    elif text in ['국고', '수협', '삼성', '신협', '농협', 'NH투자증권']:
        return text
    else:
        return text+"은행"
    
def has_comp_sala(string):
    result = list()
    pattern = r"\((주)\)|（주）|㈜|（유）|（유한）|（의）|（재）|（사）|\((사)\)|\((재)\)|\((유)\)|"
    match = re.search(pattern, string)
    if match:
        comp_word = string
        result.append("1")
        keywords = ["월급여", "급여"]
        if any(keyword in string for keyword in keywords):
            result.append("1")
            for keyword in keywords:
                if keyword in string:
                    pay_word = keyword
                    comp_word = comp_word.replace(pay_word, "")
                    break
        else:
            pay_word = None
            result.append("0")

    else:
        result.append("00")
        
    ## 00 이면 회사명 급여 아무것도 없음
    ## 01 이면 회사명은 없고 급여는 있음
    ## 10 이면 회사명은 있고 급여는 없음
    ## 11 이면 회사명 급여 둘 다 있음
    result = "".join(result)

    return (comp_word, pay_word), result


def has_tex_rela(string):
    start_word = ['SK쉴더스', '세무사', ('노무법인', '세무법인', '세무그룹', '세무회계')]
    end_word = ['세무회', ('세무사', '회계사', '세무', '세무회계사'), ('세무회계', '세무법인', '회계법인')]
    result = dict()
    
    result["tran_word"] = None
    result["name_word"] = None
    result["comp_word"] = None
    result["plac_word"] = None
    result["job_word"] = None
    
    for i, word in enumerate(start_word):
        if string.startswith(word):
            if i == 0:
                result["comp_word"] = word
                result["plac_word"] = string.replace(word, "")
                break
            if i == 1:
                result["job_word"] = word
                result["name_word"] = string.replace(word, "")
                break
            if i == 2:
                for n in list(word):
                    if n in string:
                        result["tran_word"] = n
                        result["comp_word"] = string.replace(n, "")

    for i, word in enumerate(end_word):
        if string.endswith(word):
            if i == 0:
                result["tran_word"] = word
                result["name_word"] = string.replace(word, "")
                break
            if i == 1:
                for n in list(word):
                    if n in string:
                        result["job_word"] = n
                        result["name_word"] = string.replace(n, "")
                break
            if i == 2:
                for n in list(word):
                    if n in string:
                        result["tran_word"] = n
                        result["comp_word"] = string.replace(n, "")
    
    return result
                    

def has_educ(text):
    text_dict = dict()
    end_words = ("교재비", "구입비", "재료비", "과재료", "방과후", "교과서", "수업료", "등록금",
                "학원비", "급식비", "앨범비", "검도비", "하복비", "월석식", "석식", "중식",  "방과후", "기숙사", "기숙",
                "활동비", "겨울석식", "겨울조식", "겨울석식", "체험비", "강사료", "석식비", "중식비",)
    start_words = ("신한", "농협",)
    result = False
    text_dict['educ_word'] = None
    text_dict['tax_word'] = None
    text_dict['bank_word'] = None
    
    for word in end_words:
        if word in text:
            text_dict['tax_word'] = word
            text_dict['educ_word'] = text.replace(word, "")
            result = True
            break
    
    for word in start_words:
        if word in text:
            text_dict['bank_word'] = word
            text_dict['educ_word'] = text.replace(word, "")
            result = True
            break
        
    return result, text_dict
    

def has_etc(text):
    text_dict = dict()
    result = False

    unib_start_words = "삼육대,홍익대".split(",") # 다음엔 직접입력한 텍스트
    tex_start_words = "연말정산,세무".split(",") # 다음엔 직접입력한 텍스트
    uniw_start_words = "코로나".split(",") # 다음엔 직접입력한 텍스트
    bank_start_words = "국민,금고,신한,하나,경남,광주,기업,부산,삼성,수협,농협,미래".split(",") # 다음엔 직접입력한 텍스트

    mana_start_words = "건강,서울가스".split(",") # 다음엔 이름
    loan_start_words = "DB손보,대출소개,메츠".split(",") # 다음엔 이름
    
    comp_start_words = "건국우유,남양우유,매일우유,매일유업,DLIVE,대한미용사회,중진공,삼성금융".split(",") # 다음엔 지역명

    subs_end_words = "청약".split(",") # 전에 이름
    loan_end_words = "대출이자".split(",") # 전에 은행명
    tex_end_workds = "세무서".split(",") # 전에 지역명
    bank_end_workds = "저축은행".split(",") # 전에 지역명

    
    text_dict["main_word"] = False
    text_dict["sub_word"] = False


    for word in unib_start_words:
        if text.startswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict
    
    for word in tex_start_words:
        if text.startswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict

    for word in uniw_start_words:
        if text.startswith(word):
            text_dict['sub_word'] = word
            text_dict['main_word'] = text.replace(word, "")
            result = True
            return result, text_dict

    for word in bank_start_words:
        if text.startswith(word):
            text_dict['sub_word'] = word
            text_dict['main_word'] = text.replace(word, "")
            result = True
            return result, text_dict
       
    for word in mana_start_words:
        if text.startswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict
        
    for word in loan_start_words:
        if text.startswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict
        
    for word in comp_start_words:
        if text.startswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict
      
    for word in subs_end_words:
        if text.endswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict
        
    for word in loan_end_words:
        if text.endswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict
        
    for word in tex_end_workds:
        if text.endswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict

    for word in bank_end_workds:
        if text.endswith(word):
            text_dict['main_word'] = word
            text_dict['sub_word'] = text.replace(word, "")
            result = True
            return result, text_dict

    return result, text_dict
    



## 1. 저축/투자에 있는 청약 적요를 처리한다.
def subs_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        etc = pd.DataFrame()
        if clas == '저축/투자':
            text_1, pos = lambda_preprocessing_2(text)
            if pos == ["Name", "Nic"]:
                text_stru = "name-prod"
                    
                for j, word in enumerate(text_1.split()):
                    
                    if tran_diff == "입금":
                        text_mean = "청약으로 입금된 내역의 적요이다."
                    elif tran_diff == "출금":
                        text_mean = "청약으로 출금된 내역의 적요이다."
                    
                    if j == 0:
                        word_mean = "이름"
                        object_name = "이름"
                    elif j == 1:
                        word_mean = word
                        object_name = "상품명"
                        
                    etc = etc.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': text_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': word,
                                    '단어일련번호':j,
                                    '단어의미':word_mean,
                                    '개체명': object_name,
                                    '완료여부':1,
                                    }, ignore_index=True)
            else:
                etc = df.iloc[i].to_frame().T 
        else:
            etc = df.iloc[i].to_frame().T   

        new_df = pd.concat([new_df, etc], axis=0) 
    return new_df



## 2. 개인입금, 개인간거래 처리
def pers_tran_proc(df):

    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        etc = pd.DataFrame()
        

        # 은행명 다음에 이름
        if clas in ['개인입금', '개인간거래']:
            # text_1, pos = lambda_preprocessing_2(text)
            # if pos == ["Nic", "Name"]:
            result, text_1 = has_bank(text)
            if result:
                text_1 = " ".join(text_1)
                text_stru = "bank-name"

                for j, word in enumerate(text_1.split()):
                    if j == 0:
                        word_mean = change_bank_name(word)
                        object_name = "은행명"
                        if tran_diff == "입금":
                            text_mean = "%s 계좌에서 입금받은 내역의 적요이다."%word_mean
                        elif tran_diff == "출금":
                            text_mean = "%s 계좌로 이체한 내역의 적요이다."%word_mean

                    elif j == 1:
                        word_mean = "이름"
                        object_name = "이름"
                    etc = etc.append({'확인용': num,
                                    '적요': text,
                                    '적요일련번호': text_num,
                                    '입출금구분': tran_diff,
                                    '데이터셋출처': data_sour,
                                    '출처번호': sour_num,
                                    '적요구조': text_stru,
                                    '적요구조일련번호': text_stru_num,
                                    '적요 설명': text_mean,
                                    '거래코드': tran_code,
                                    '분류': clas,
                                    '분류번호': clas_num,
                                    '최소금액': min_amou,
                                    '최대금액': max_amou,
                                    '단어': word,
                                    '단어일련번호':j,
                                    '단어의미':word_mean,
                                    '개체명': object_name,
                                    '완료여부':1,
                                    }, ignore_index=True)
            else:
                etc = df.iloc[i].to_frame().T 
        else:
            etc = df.iloc[i].to_frame().T 
        new_df = pd.concat([new_df, etc], axis=0)

    return new_df

# 회사명, 급여 처리
def come_pay_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        etc = pd.DataFrame()
        if clas in ['회사입금', '회사출금', '급여']:
            words, result = has_comp_sala(text)
            if words[1] is None:
                lists = [words[0]]
            else:
                lists = [words[0], words[1]]
                        
            for j, word in enumerate(lists):
                if j == 0:
                    word_mean = words[0]
                    object_name = "회사명"
                    # 회사명은 없고 급여는 있음
                    if result == "01":
                        if tran_diff == "입금":
                            text_mean = "%s로부터 급여를 입금받은 내역의 적요이다."%word_mean
                        elif tran_diff == "출금":
                            text_mean = "%s가 급여를 이체한 내역의 적요이다."%word_mean

                    # 회사명은 있고 급여는 없음 
                    elif result == "10":
                        # 거래분류코드에 급여라는 단어가 있으면 급여임
                        if "급여" in tran_code:
                            if tran_diff == "입금":
                                text_mean = "%s로부터 급여를 입금받은 내역의 적요이다."%word_mean
                            elif tran_diff == "출금":
                                text_mean = "%s가 급여를 이체한 내역의 적요이다."%word_mean 
                        else:
                            if tran_diff == "입금":
                                text_mean = "%s로부터 입금받은 내역의 적요이다."%word_mean
                            elif tran_diff == "출금":
                                text_mean = "%s가 이체한 내역의 적요이다."%word_mean 
                                
                    # 회사명 급여 둘 다 있음 
                    elif result == "11":
                        if tran_diff == "입금":
                            text_mean = "%s로부터 급여를 입금받은 내역의 적요이다."%word_mean
                        elif tran_diff == "출금":
                            text_mean = "%s가 급여를 이체한 내역의 적요이다."%word_mean


                    # 회사명 급여 둘 다 없음
                    else:
                        # 거래분류코드에 급여라는 단어가 있으면 급여임
                        if "급여" in tran_code:
                            if tran_diff == "입금":
                                text_mean = "%s로부터 급여를 입금받은 내역의 적요이다."%word_mean
                            elif tran_diff == "출금":
                                text_mean = "%s가 급여를 이체한 내역의 적요이다."%word_mean 
                        else:
                            if tran_diff == "입금":
                                text_mean = "%s로부터 입금받은 내역의 적요이다."%word_mean
                            elif tran_diff == "출금":
                                text_mean = "%s가 이체한 내역의 적요이다."%word_mean 

                elif j == 1:
                    word_mean = "급여"
                    object_name = "거래명"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
        
        else:
            etc = df.iloc[i].to_frame().T 
        new_df = pd.concat([new_df, etc], axis=0)

    return new_df
        
# 세무, 회계 등 전문서비스 처리
def prof_serv_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']
        
        etc = pd.DataFrame()

        if clas == '전문서비스':
            
            # (tran_word, name_word, comp_word, plac_word, job_word)
            text_dict = {key: value for key, value in has_tex_rela(text).items() if value is not None}
            
            # 회사명 나머지는 지역
            if "comp_word" in text_dict and "plac_word" in text_dict:
                word_mean = text_dict["comp_word"]
                if tran_diff == "입금":
                    text_mean = "%s로부터 입금받은 내역의 적요이다."%word_mean
                elif tran_diff == "출금":
                    text_mean = "%s가 이체한 내역의 적요이다."%word_mean 
                word = text_dict["comp_word"]
                j=0
                object_name = "회사명"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
                word = text_dict["plac_word"]
                j=1
                object_name = "장소"
                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)

            # 금융용어 나머지는 회사명
            elif "comp_word" in text_dict and "tran_word" in text_dict:
                
                word_mean_1 = text_dict["comp_word"]
                word_mean_2 = text_dict["tran_word"]

                if tran_diff == "입금":
                    text_mean = "%s로부터 입금받은 내역의 적요이다."%word_mean_1+word_mean_2
                elif tran_diff == "출금":
                    text_mean = "%s가 이체한 내역의 적요이다."%word_mean_1+word_mean_2
                    
                    
                word = text_dict["comp_word"]
                j=0
                object_name = "회사명"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean_1,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
                word = text_dict["tran_word"]
                j=1
                object_name = "금융용어"
                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean_2,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)

            # 직업 나머지는 이름
            elif "job_word" in text_dict and "name_word" in text_dict:
                
                word_mean_1 = text_dict["job_word"]
                word_mean_2 = text_dict["name_word"]

                if tran_diff == "입금":
                    text_mean = "%s로부터 입금받은 내역의 적요이다."%word_mean_1
                elif tran_diff == "출금":
                    text_mean = "%s가 이체한 내역의 적요이다."%word_mean_1
                    
                    
                word = text_dict["job_word"]
                j=0
                object_name = "직업"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean_1,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
                word = text_dict["name_word"]
                j=1
                object_name = "이름"
                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean_2,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
            # 직업 나머지는 이름
            elif "tran_word" in text_dict and "name_word" in text_dict:
                
                word_mean_1 = text_dict["tran_word"]
                word_mean_2 = text_dict["name_word"]

                if tran_diff == "입금":
                    text_mean = "%s로부터 입금받은 내역의 적요이다."%word_mean_1
                elif tran_diff == "출금":
                    text_mean = "%s가 이체한 내역의 적요이다."%word_mean_1
                    
                    
                word = text_dict["tran_word"]
                j=0
                object_name = "금융용어"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean_1,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
                word = text_dict["name_word"]
                j=1
                object_name = "이름"
                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean_2,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
            else:
                etc = df.iloc[i].to_frame().T 
        else:
            etc = df.iloc[i].to_frame().T 
        
        new_df = pd.concat([new_df, etc], axis=0)
        
    return new_df

# 기부
def dona_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        etc = pd.DataFrame()
        
        if clas == '기부':
            result, text_1 = has_bank(text)
            if result:
                word_mean = text_1[1]

                if tran_diff == "입금":
                    text_mean = "%s로부터 기부받은 내역의 적요이다."%word_mean
                elif tran_diff == "출금":
                    text_mean = "%s가 기부한 내역의 적요이다."%word_mean
                    
                    
                word = text_1[1]
                j=0
                object_name = "기부단체"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
                word = text_1[0]
                word_mean = word+"은행"
                j=1
                object_name = "은행명"
                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
            else:
                word_mean = text
                if tran_diff == "입금":
                    text_mean = "%s로부터 기부받은 내역의 적요이다."%word_mean
                elif tran_diff == "출금":
                    text_mean = "%s가 기부한 내역의 적요이다."%word_mean
                    
                    
                word = text
                j=0
                object_name = "기부단체"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
        else:
            etc = df.iloc[i].to_frame().T 
        
        new_df = pd.concat([new_df, etc], axis=0)
        
    return new_df
            
# 교육비
def educ_spen_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        etc = pd.DataFrame()
        
        if clas == '교육비':
            result, text_1 = has_educ(text)
            if result:
                if text_1["educ_word"].endswith(("초","고")):
                    word_mean = text_1["educ_word"]+"등학교"
                elif text_1["educ_word"].endswith(("중")):
                    word_mean = text_1["educ_word"]+"학교"
                else:
                    word_mean = text_1["educ_word"]
                
                if tran_diff == "입금":
                    text_mean = "%s로부터 %s를 위해 받은 내역의 적요이다."%(word_mean, text_1["tax_word"])
                elif tran_diff == "출금":
                    text_mean = "%s가 %s를 위해 이체한 내역의 적요이다."%(word_mean, text_1["tax_word"])
                
                for j,n in enumerate(text_1.keys()):
                    if text_1[n] is not None:
                        word = text_1[n]
                        if n == 'educ_word':
                            object_name = "교육기관"
                            if word.endswith(("초","고")):
                                word_mean = word+"등학교"
                            elif word.endswith(("중")):
                                word_mean = word+"학교"
                            else:
                                word_mean = text_1[n]
                            
                        elif n == 'tax_word':
                            object_name = "교육비용"
                            word_mean = text_1[n]
                            
                        elif n == 'bank_word':
                            object_name = "은행명"
                            word_mean = text_1[n]
                        etc = etc.append({'확인용': num,
                                        '적요': text,
                                        '적요일련번호': text_num,
                                        '입출금구분': tran_diff,
                                        '데이터셋출처': data_sour,
                                        '출처번호': sour_num,
                                        '적요구조': text_stru,
                                        '적요구조일련번호': text_stru_num,
                                        '적요 설명': text_mean,
                                        '거래코드': tran_code,
                                        '분류': clas,
                                        '분류번호': clas_num,
                                        '최소금액': min_amou,
                                        '최대금액': max_amou,
                                        '단어': word,
                                        '단어일련번호':j,
                                        '단어의미':word_mean,
                                        '개체명': object_name,
                                        '완료여부':1,
                                        }, ignore_index=True)

            else:
                etc = df.iloc[i].to_frame().T
        else:
            etc = df.iloc[i].to_frame().T     
            
        new_df = pd.concat([new_df, etc], axis=0)
        
    return new_df


# 그외
def etc_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        etc = pd.DataFrame()
        
        result, text_1 = has_etc(text)
        if result:
            if tran_diff == "입금":
                text_mean = "%s로부터 %s로 입금된 내역의 적요이다."%(text_1['sub_word'], text_1['main_word'])
            elif tran_diff == "출금":
                text_mean = "%s가 %s로 이체한 내역의 적요이다."%(text_1['sub_word'], text_1['main_word'])
            
            for j,n in enumerate(text_1.keys()):
                object_name = "직접입력"
                word = text_1[n]
                word_mean = text_1[n]

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)

        else:
            etc = df.iloc[i].to_frame().T
     
            
        new_df = pd.concat([new_df, etc], axis=0)
        
    return new_df      

# 회사출금
def comp_with_proc(df):
    new_df = pd.DataFrame(columns=['확인용', '적요', '적요일련번호', '금융회사', '입출금구분', '데이터셋출처', '출처번호', '적요구조',
                                    '적요구조일련번호', '적요 설명', '거래코드', '분류', '분류번호', '최소금액', '최대금액', '단어',
                                    '단어일련번호', '단어의미', '개체명',"완료여부"])

    for i in tqdm(range(len(df))):
        num = df.iloc[i]['확인용']
        text = df.iloc[i]['적요']
        text_num = df.iloc[i]['적요일련번호']
        tran_diff = df.iloc[i]['입출금구분']
        data_sour = df.iloc[i]['데이터셋출처']
        sour_num = df.iloc[i]['출처번호']
        text_stru = df.iloc[i]['적요구조']
        text_stru_num = df.iloc[i]['적요구조일련번호']
        # text_mean = df.iloc[i]['적요 설명']
        tran_code = df.iloc[i]['거래코드']
        clas = df.iloc[i]['분류']
        clas_num = df.iloc[i]['분류번호']
        min_amou = df.iloc[i]['최소금액']
        max_amou = df.iloc[i]['최대금액']

        etc = pd.DataFrame()
        
        if clas == '회사출금':
            if text.startswith("사단법인"):
                word_mean = text[4:]

                if tran_diff == "입금":
                    text_mean = "%s로부터 이체한 내역의 적요이다."%word_mean
                elif tran_diff == "출금":
                    text_mean = "%s가 이체한 내역의 적요이다."%word_mean
                    
                    
                word = text_1[1]
                j=0
                object_name = "기부단체"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
                
                word = text_1[0]
                word_mean = word+"은행"
                j=1
                object_name = "은행명"
                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
            else:
                word_mean = text
                if tran_diff == "입금":
                    text_mean = "%s로부터 기부받은 내역의 적요이다."%word_mean
                elif tran_diff == "출금":
                    text_mean = "%s가 기부한 내역의 적요이다."%word_mean
                    
                    
                word = text
                j=0
                object_name = "기부단체"

                etc = etc.append({'확인용': num,
                                '적요': text,
                                '적요일련번호': text_num,
                                '입출금구분': tran_diff,
                                '데이터셋출처': data_sour,
                                '출처번호': sour_num,
                                '적요구조': text_stru,
                                '적요구조일련번호': text_stru_num,
                                '적요 설명': text_mean,
                                '거래코드': tran_code,
                                '분류': clas,
                                '분류번호': clas_num,
                                '최소금액': min_amou,
                                '최대금액': max_amou,
                                '단어': word,
                                '단어일련번호':j,
                                '단어의미':word_mean,
                                '개체명': object_name,
                                '완료여부':1,
                                }, ignore_index=True)
        else:
            etc = df.iloc[i].to_frame().T 
        
        new_df = pd.concat([new_df, etc], axis=0)
        
    return new_df


if __name__ == '__main__':
    path = "../data/우리은행/작업/공통/dataset_4.csv"
    df = pd.read_csv(path, encoding="utf-8-sig", index_col=0)
    df_1 = df[df["완료여부"]==1].copy()
    df_2 = df[df["완료여부"].isnull()].copy()
    print(len(df), len(df_2))
    
    df_2 = pers_tran_proc(df_2)
    new_df = pd.concat([df_1, df_2], axis=0)
    print(len(new_df), len(df_2))


    a = len(new_df["확인용"].unique())
    b = len(new_df[new_df["완료여부"]==1]["확인용"].unique())

    print("전체개수: ", a)
    print("완료개수: ", b)