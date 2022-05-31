"""
22.05.31 - 텍스트 추출 

## 할일 

"""
print(__doc__)

# import 
import fitz
import requests
import time
import re

inputFile = '1909.12744.pdf'
doc = fitz.open(inputFile)
doc_t = doc


# 1차 
join_box = list()
last_data = 0 
for i in doc_t:
    txt = i.get_text().split('\n')
    try:
        for i,t in enumerate(txt):
            if  last_data == 0 and t[-1] == '-':
                last_data = t[:-1]
            elif last_data != 0 and t[-1] == '-': # 히스토리 있고  하이픈 있을때
                last_data = last_data + t[:-1]
            elif last_data != 0: # 히스토리 있고 하이픈 없을떄
                last_data = last_data + t
                join_box.append(last_data)
                last_data = 0 
            else:
                join_box.append(t)
    except Exception as e:
        print(e,t)
    break # 1 page만 


# 2차
base = 'Abstract'
where_base = [i for i,J in enumerate(join_box) if base.lower() == J.lower()]


def Find_sentence(past, val):
    #     txt = 0 
    print(val)
    if val[-1] == '.' and val[0].isupper() == True and val[1].islower():
        print(txt)
        return val 
    
    else:
        if val[0].isupper() == True and val[1].islower() and val[-1] !='.': # 조건 앞이 대문자 그다음이 소문자 마지막이 '.' 이 아닌 경우 
    #         print(val)
            txt = past+' '+val
            print(txt)
        return txt 

# 현재 진행형 
txt_box = list()
past = 0 
for idx, val in enumerate(join_box):
    if idx > where_base[0] :
        print(val)
        if past == 0:
            past = val
        else: 
            if past != 0  and past[-1] != '.':
                txt = Find_sentence(past,val)
                print(txt)

                print( )
            elif past != 0  and  past[-1] == '.':
                print('1111',past)
                txt_box.append(past)
                past = 0

    # 일단 여기는 무시     
    else:
        txt_box.append(val)
        
# 논리가 존나 복잡하네 썅 