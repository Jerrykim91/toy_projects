

# 쓰레기 




### 날짜 -  
```py

 
``` 

---

### 날짜 -  22.06.01 - 텍스트 추출 
```py
print(__doc__)

# import 
from imghdr import what
import fitz
import requests
import time
import re

from sympy import apart

inputFile = '1909.12744.pdf'
doc = fitz.open(inputFile)
doc_t = doc

def Remove_hyphens(val, stacking_box):
    # stacking_box에 다가 문장을 만들도록 담는다. 
    
    if val[-1] == '-':
        val = val[:-1]
        stacking_box.append(val) # '-' 제거하고 append
    else: # 하이픈이 없는 경우 
        if len(stacking_box) != 0:
            stacking_box.append(val)
            # if val[0].isupper() == True and val[1].islower():
            #     print(val)
            #     print(stacking_box[-1][-1])
            #     stacking_box.append(val)
                # if stacking_box[-1][-1] == '.': # 리스트에 데이터가 있고 마지막 데이터가 dot 인 경우 
                #     print(val)
                    
                #     join_txt = "".join(stacking_box) # 합친다. 
                #     join_txt = join_txt+' '# 추후 수정가능
                #     print('join_txt____',join_txt) #확인 필요
                #     stacking_box = list()
                #     # return join_txt
                # else:
                #     stacking_box.append(val)
                    
            # join_txt = "".join(stacking_box) # 합친다. 
            # join_txt = join_txt+' '# 추후 수정가능
            # print('join_txt____',join_txt) #확인 필요
            # print(stacking_box)
            print( )
            # stacking_box = list()
            # return join_txt
            if stacking_box[-1][-1] == '.': # 리스트에 데이터가 있고 마지막 데이터가 dot 인 경우 
                # print(val)
                join_txt = "".join(stacking_box) # 합친다. 
                join_txt = join_txt+' '# 추후 수정가능
                print('join_txt____',join_txt) #확인 필요
                stacking_box = list()
        else: # stacking_box 내부에 데이터가 있는 경우도 포함 
            stacking_box.append(val)
            # print(stacking_box)
            # if len(stacking_box) != 0: # 마지막이 .도 아니고 하이픈도 없는 경우 
            #     pass
            # else:
            #     stacking_box.append(val)
    return 'Dev-Remove_hyphens' 


# def Remove_hyphens(txt):
#     for i,t in enumerate(txt): # txt는 한 페이지의 텍스트 데이터 
#         if  last_data == 0 and t[-1] == '-':
#             last_data = t[:-1]
#         elif last_data != 0 and t[-1] == '-': # 히스토리 있고 하이픈 있을때
#             last_data = last_data + t[:-1]
#         elif last_data != 0: # 히스토리 있고 하이픈 없을떄
#             last_data = last_data + t
#             join_box.append(last_data)
#             last_data = 0 
#         else:
#             # join_box.append(t)
#             return t
    
#     return 0
# def Remove_hyphens(val, stacking_box):
#     # stacking_box에 다가 문장을 만들도록 담는다. 
#     if val[-1] == '.' and val[0].isupper() == True and val[1].islower():
#         # print('1')
#         pass
#     else:
#         # 하이픈 제거 
#         if val[-1] == '-':
#             val = val[:-1]
#             stacking_box.append(val)
#             # print(stacking_box)
#         else:
#             # print(val)
#             # elif len(stacking_box) != 0 and stacking_box[-1][-1] == '.':
                
#             #     join_txt = "".join(stacking_box)
#             #     join_txt = join_txt+' ' # 추후 수정가능
#             #     # print(join_txt)
#             #     # stacking_box = list()
#             if len(stacking_box) !=0:
#                 if stacking_box[-1][-1] == '.':
#                     join_txt = "".join(stacking_box)
#                     join_txt = join_txt+' '# 추후 수정가능
#                     print('join_txt____',join_txt)
#                     stacking_box = list()
                    
#                 else: 
#                     print(stacking_box[-1][-1])
#             else:
#                 # print(val)
#                 stacking_box.append(val)
#                 # print(stacking_box)

#         # print('2')
#     return 'Dev-Remove_hyphens' 


def Find_sentence(txt):
    base = 'Abstract'
    where_base = [i for i,J in enumerate(txt) if base.lower() == J.lower()][0]  # Abstract 위치 파악 
    
    stacking_box = list()
    save_box = list()
    for idx, val in enumerate(txt[:]):        
        if idx > where_base: # 해당 위치 아래는 진짜 글 
            if len(val) != 0 :
                # print(txt,'1111111111111111')
                j_txt = Remove_hyphens(val, stacking_box)
                save_box.append(j_txt)
            
    return 'Dev-Find_sentence'




# 1차 
join_box = list()
last_data = 0 
for i in doc_t:
    txt = i.get_text().split('\n')
    txt_box = Find_sentence(txt)
    # print(txt_box)
    
    break # 1 page만 
    # try:
    #     # for i,t in enumerate(txt):
    #     #     if  last_data == 0 and t[-1] == '-':
    #     #         last_data = t[:-1]
    #     #     elif last_data != 0 and t[-1] == '-': # 히스토리 있고  하이픈 있을때
    #     #         last_data = last_data + t[:-1]
    #     #     elif last_data != 0: # 히스토리 있고 하이픈 없을떄
    #     #         last_data = last_data + t
    #     #         join_box.append(last_data)
    #     #         last_data = 0 
    #     #     else:
    #     #         join_box.append(t)
    # except Exception as e:
    #     print(e,t)
    # break # 1 page만 


# # 2차
# base = 'Abstract'
# where_base = [i for i,J in enumerate(join_box) if base.lower() == J.lower()]


# def Find_sentence(past, val):
#     #     txt = 0 
#     print(val)
#     if val[-1] == '.' and val[0].isupper() == True and val[1].islower():
#         print(txt)
#         return val 
    
#     else:
#         if val[0].isupper() == True and val[1].islower() and val[-1] !='.': # 조건 앞이 대문자 그다음이 소문자 마지막이 '.' 이 아닌 경우 
#     #         print(val)
#             txt = past+' '+val
#             print(txt)
#         return txt 

# # 현재 진행형 
# txt_box = list()
# past = 0 
# for idx, val in enumerate(join_box):
#     if idx > where_base[0] :
#         print(val)
#         if past == 0:
#             past = val
#         else: 
#             if past != 0  and past[-1] != '.':
#                 txt = Find_sentence(past,val)
#                 print(txt)

#                 print( )
#             elif past != 0  and  past[-1] == '.':
#                 print('1111',past)
#                 txt_box.append(past)
#                 past = 0

#     # 일단 여기는 무시     
#     else:
#         txt_box.append(val)
        
# # 논리가 존나 복잡하네 썅 
 
``` 

---

### 날짜 - 22.05.31 - 텍스트 추출 
```py
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
```


---

### 날짜 - 머름
```py
from telnetlib import TM
import fitz
import requests
import time
import re

inputFile = '1909.12744.pdf'
doc = fitz.open(inputFile)
# print(doc)


for i in doc:
    temp = i.get_text()
    test = temp.split('\n')
    for t in test:
        if '-' in t :
            print(t)
    # temp = temp.replace()
    # print(len(test))
    break

```