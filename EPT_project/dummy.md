

# 쓰레기 

```py
"""
22.06.06 - 텍스트 추출 
"""
print(__doc__)

# import 
import fitz
from DEV import deg_for_test # 디버깅용
# import requests
# import time
# import re
 
#------- values ----------
inputFile = '1909.12744.pdf'
doc = fitz.open(inputFile)
doc_t = doc

Special_characters = ['•']
Special_word = ['Table','Figure']
Point_word = ['abstract','reference']
typing_error_dict = {':.':':',}

#------- Funtions ----------

dev = False #True #False
name = 0

# def model():
#   # 1. Table
#   # 2. Figer
#     pass 

# def typing_error(val): # 보류 
#     for err, chg in typing_error_dict:
#         if err in val : 
#             val = val.replace(err,chg) 
#     return val

def find_point_page(doc,Point_word):
    send_point = dict()
    for point in Point_word:
        test = [(point, int(str(page).split(' ')[1])+1) for page in doc if len(page.search_for(point)) != 0 ]
        
        if point == 'reference':
            send_point[point] = test[-1][1]
        else: 
            send_point[point] = test[0][1]
    return send_point


def handling_issue(stacking_box):
    val = stacking_box
    # print(val)
    if val[0].isdigit() == True: # 첫글자가 숫자면 
        val.insert(1,' ')
        val.insert(3, '\n')
    return stacking_box


def Remove_hyphens(val,stacking_box, state=0):
    if dev != False :
        # 일단 리스트에 다담아 
        if len(stacking_box) == 0 : # 빈 리스트거나 맨앞이 대문자 거나  
            stacking_box.append(val)
            
        else: # 리스트 활동성 있고 있는 ㅎㅎ              
            if stacking_box[-1][-1] == '-': # 마지막이 하이픈인 데이터 추출 
                pop_data = stacking_box.pop(-1) # 하이픈으로 추측 되는 데이터 꺼내기 
                push_data = pop_data[:-1]+val
                stacking_box.append(push_data)

            elif stacking_box[-1][-1] == '.':
                handling_issue(stacking_box)
                join_txt = " ".join(stacking_box) # 합친다. 
                txt = join_txt+'\n'# 추후 수정가능
                # txt = join_txt+'/'# 추후 수정가능
                state = 1
                stacking_box = list()
                stacking_box.append(val)
                return txt , state, stacking_box
                 
            else: # 하이픈으로 안나오는 데이터
                if val[0].isupper() == True :
                    stacking_box.append(val)     
                elif val[0].isdigit() == True:
                    stacking_box.append(val) 
                else: 
                    # stacking_box.append('@')
                    stacking_box.append(val)
                    
        return 'Dev-Remove_hyphens', state, stacking_box           
    else:
        if len(stacking_box) == 0 : # 빈 리스트거나 맨앞이 대문자 거나  
            stacking_box.append(val)
            
        else: # 리스트 활동성 있고 있는 ㅎㅎ              
            if stacking_box[-1][-1] == '-': # 마지막이 하이픈인 데이터 추출 
                pop_data = stacking_box.pop(-1) # 하이픈으로 추측 되는 데이터 꺼내기 
                push_data = pop_data[:-1]+val
                stacking_box.append(push_data)

            elif stacking_box[-1][-1] == '.':
                handling_issue(stacking_box)
                join_txt = " ".join(stacking_box) # 합친다. 
                txt = join_txt+'\n'# 추후 수정가능
                # txt = join_txt+'/'# 추후 수정가능
                state = 1
                stacking_box = list()
                stacking_box.append(val)
                return txt , state, stacking_box
                 
            else: # 하이픈으로 안나오는 데이터
                if val[0].isupper() == True :
                    stacking_box.append(val)     
                elif val[0].isdigit() == True:
                    stacking_box.append(val) 
                else: 
                    stacking_box.append(val)
                    
        return 'Dev-Remove_hyphens', state, stacking_box    


def Find_sentence(txt, page):
    stacking_box = list()
    save_box = list()
    if page == abstract:
        print(page)
        name = 'Abstract'
        Where_abstract = [i for i,J in enumerate(txt) if name.lower() == J.lower()][0]  # Abstract 위치 파악 
    
        for idx, val in enumerate(txt):        
            if idx > Where_abstract: # 해당 위치 아래는 진짜 글 
                if len(val) != 0 :
                    j_txt, state, stacking_box = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                    if state == 1:
                        if j_txt[0].isupper() == True:
                            save_box.append(j_txt)
                        elif j_txt[0].isdigit() == True:
                            j_txt = '\n' +j_txt 
                            save_box.append(j_txt)
                        else:
                            save_box.append(j_txt)
                            print('Why!!!!!'*50,'\n', j_txt)                        
        return [page, save_box]#(page, save_box[0])
    elif page >= reference:
        pass
        # # 레퍼런스 페이지 내에 contents가 있을 수 있음 
        # # - 그부분을 고려한 코드가 필요 
        # name = 'reference'
        # where_reference = [i for i,J in enumerate(txt) if name.lower() == J.lower()][0]  # Abstract 위치 파악 
        # print(where_reference)
        
        # print('-'*25, page,'-'*3,'reference','-'*25)
        # for idx, val in enumerate(txt): 
        #     # if idx > where_reference: 분류 옵션을 ... 함수로? 
                       
        #     if len(val) != 0 :
        #         j_txt, state, stacking_box = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
        #         if state == 1:
        #             if Special_characters[0] in j_txt:
        #                 j_txt = j_txt.replace(Special_characters[0], '\n'+j_txt[0])
        #                 # print(j_txt)
        #             if j_txt[0].isupper() == True:
        #                 save_box.append(j_txt)
        #             elif j_txt[0].isdigit() == True:
        #                 j_txt = '\n' +j_txt 
        #                 save_box.append(j_txt)
        #             else:
        #                 save_box.append(j_txt)
        # if len(stacking_box):
        #     join_txt= " ".join(stacking_box)+'\n'
        #     save_box.append(join_txt)
        # return [page, save_box] 
    else:
        for idx, val in enumerate(txt):        
            if len(val) != 0 :
                j_txt, state, stacking_box = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                if state == 1:
                    if Special_characters[0] in j_txt:
                        j_txt = j_txt.replace(Special_characters[0], '\n'+j_txt[0])
                        # print(j_txt)
                    if j_txt[0].isupper() == True:
                        save_box.append(j_txt)
                    elif j_txt[0].isdigit() == True:
                        j_txt = '\n' +j_txt 
                        save_box.append(j_txt)
                    else:
                        save_box.append(j_txt)
                        # print(page,'\n','Why!!!!!'*50,'\n', j_txt)
                        # print(page,'\n',j_txt)
                # elif state == 0:
                #     print(page,'\n',stacking_box)
        if len(stacking_box):
            # 일단은 append 해서 작업 진행 
            join_txt= " ".join(stacking_box)+'\n'
            save_box.append(join_txt)
            # for idx, re in enumerate(reversed(stacking_box)):
            #     if re[0].isdigit() != True:
                    
            #     if re[0].isdigit() == True:
            #         # re.insert(1, ' ')
            #         attachment = '\n' + re[:1]+' '+re[1:]
            #         join_txt= " ".join(stacking_box[:-idx])+'\n'
            #         save_box.append(join_txt)
            #         save_box.append(attachment)
            #     else:
            #         join_txt= " ".join(stacking_box)+'\n'
            #         save_box.append(join_txt)

            # 3. ['The motivation of using NMT-src is to test', 'whether the resulting NMT model is more robust', '3http://www.statmt.org/wmt19/translation-task.html']
            # 5. ['Based on these results, we conclude that pretraining the encoder with a masked LM task does not', 'really bring improvement in terms of robustness', 'to unknowns. It seems that BERT does yield improvement for NMT as a better initialization for']
        return [page, save_box] #(page, save_box)


# 1차 
page  = 1 
state = 0
join_box = list()

point_loction = find_point_page(doc,Point_word) #  앱슽랙트, 레퍼런스 위치 찾기 
abstract  = point_loction['abstract']
reference = point_loction['reference']

for i in doc_t:
    if dev == False :
        txt = i.get_text().split('\n')
        txt_box = Find_sentence(txt, page) # 문장 찾는 알고리즘 
        join_box.append(txt_box)

    if dev == True and page == 3: # DEV
        txt = i.get_text().split('\n')
        txt_box = Find_sentence(txt, page) # 문장 찾는 알고리즘 
        join_box.append(txt_box)
        # print(join_box)
        tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ').replace('~','')}\n " for i in join_box]
        print( )
        print(tmp)
        break 
    
    page +=1
print('Txet Append Done-')

    
# 본문 
save = 1
if save == 1: # ','.join(i[1])
    tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ')}\n " for i in join_box if i != None]
    # print(tmp)
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0605.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(tmp))
    fout.close()
        
```
---
```py
"""
22.06.04 - 텍스트 추출 

## 할일 

"""
print(__doc__)

# import 
import fitz


from DEV import deg_for_test
# import requests
# import time
# import re
 
#------- values ----------
inputFile = '1909.12744.pdf'
doc = fitz.open(inputFile)
doc_t = doc

Special_characters = ['•']
Special_word = ['Table','Figure']
# 오타 - ':.'
typing_error_dict = {':.':':',}
# 추후에 조건이 필요해 보임 - dict 아니 함수로 - 레퍼런스 , 제목 타이틀, 이런거 나눌때 사용

#------- Funtions ----------

dev = False #True #False


# def model():
#   # 1. Table
#   # 2. Figer
#     pass 

# def typing_error(val): # 보류 
#     for err, chg in typing_error_dict:
#         if err in val : 
#             val = val.replace(err,chg) 
#     return val

def handling_issue(stacking_box):
    val = stacking_box
    # print(val)
    if val[0].isdigit() == True: # 첫글자가 숫자면 
        val.insert(1,' ')
        val.insert(3, '\n')
    return stacking_box


def Remove_hyphens(val,stacking_box, state=0):
    if dev != False :
        # 일단 리스트에 다담아 
        if len(stacking_box) == 0 : # 빈 리스트거나 맨앞이 대문자 거나  
            stacking_box.append(val)
            
        else: # 리스트 활동성 있고 있는 ㅎㅎ              
            if stacking_box[-1][-1] == '-': # 마지막이 하이픈인 데이터 추출 
                pop_data = stacking_box.pop(-1) # 하이픈으로 추측 되는 데이터 꺼내기 
                push_data = pop_data[:-1]+val
                stacking_box.append(push_data)

            elif stacking_box[-1][-1] == '.':
                handling_issue(stacking_box)
                join_txt = " ".join(stacking_box) # 합친다. 
                txt = join_txt+'\n'# 추후 수정가능
                # txt = join_txt+'/'# 추후 수정가능
                state = 1
                stacking_box = list()
                stacking_box.append(val)
                return txt , state, stacking_box
                 
            else: # 하이픈으로 안나오는 데이터
                if val[0].isupper() == True :
                    stacking_box.append(val)     
                elif val[0].isdigit() == True:
                    stacking_box.append(val) 
                else: 
                    # stacking_box.append('@')
                    stacking_box.append(val)
                    
        return 'Dev-Remove_hyphens', state, stacking_box           
    else:
        if len(stacking_box) == 0 : # 빈 리스트거나 맨앞이 대문자 거나  
            stacking_box.append(val)
            
        else: # 리스트 활동성 있고 있는 ㅎㅎ              
            if stacking_box[-1][-1] == '-': # 마지막이 하이픈인 데이터 추출 
                pop_data = stacking_box.pop(-1) # 하이픈으로 추측 되는 데이터 꺼내기 
                push_data = pop_data[:-1]+val
                stacking_box.append(push_data)

            elif stacking_box[-1][-1] == '.':
                handling_issue(stacking_box)
                join_txt = " ".join(stacking_box) # 합친다. 
                txt = join_txt+'\n'# 추후 수정가능
                # txt = join_txt+'/'# 추후 수정가능
                state = 1
                stacking_box = list()
                stacking_box.append(val)
                return txt , state, stacking_box
                 
            else: # 하이픈으로 안나오는 데이터
                if val[0].isupper() == True :
                    stacking_box.append(val)     
                elif val[0].isdigit() == True:
                    stacking_box.append(val) 
                else: 
                    stacking_box.append(val)
                    
        return 'Dev-Remove_hyphens', state, stacking_box    
  
# def split_sction():
#     뒤에서부터 페이지랑 레퍼런스 위치 찾고 
#     if page == 1: 
#         base = 'Abstract'
#         where_base = [i for i,J in enumerate(txt) if base.lower() == J.lower()][0]  # Abstract 위치 파악 
#         return where_base
#     
#     pass

def Find_sentence(txt, page):
    stacking_box = list()
    save_box = list()
    if page == point_loction['abstract']:
        base = 'Abstract'
        where_base = [i for i,J in enumerate(txt) if base.lower() == J.lower()][0]  # Abstract 위치 파악 
    
        for idx, val in enumerate(txt):        
            if idx > where_base: # 해당 위치 아래는 진짜 글 
                if len(val) != 0 :
                    j_txt, state, stacking_box = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                    if state == 1:
                        if j_txt[0].isupper() == True:
                            save_box.append(j_txt)
                        elif j_txt[0].isdigit() == True:
                            j_txt = '\n' +j_txt 
                            save_box.append(j_txt)
                        else:
                            save_box.append(j_txt)
                            print('Why!!!!!'*50,'\n', j_txt)                        
        return [page, save_box]#(page, save_box[0])
    else:
        for idx, val in enumerate(txt):        
            # if  마지막 텍스트 이면 :
            #   숫자가 있다면 - 범례
            if len(val) != 0 :
                j_txt, state, stacking_box = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                if state == 1:
                    if Special_characters[0] in j_txt:
                        j_txt = j_txt.replace(Special_characters[0], '\n'+j_txt[0])
                        # print(j_txt)
                    if j_txt[0].isupper() == True:
                        save_box.append(j_txt)
                    elif j_txt[0].isdigit() == True:
                        j_txt = '\n' +j_txt 
                        save_box.append(j_txt)
                    else:
                        save_box.append(j_txt)
                        # print(page,'\n','Why!!!!!'*50,'\n', j_txt)
                        # print(page,'\n',j_txt)
                # elif state == 0:
                #     print(page,'\n',stacking_box)
        if len(stacking_box):
            # 일단은 append 해서 작업 진행 
            join_txt= " ".join(stacking_box)+'\n'
            save_box.append(join_txt)
            # for idx, re in enumerate(reversed(stacking_box)):
            #     if re[0].isdigit() != True:
                    
            #     if re[0].isdigit() == True:
            #         # re.insert(1, ' ')
            #         attachment = '\n' + re[:1]+' '+re[1:]
            #         join_txt= " ".join(stacking_box[:-idx])+'\n'
            #         save_box.append(join_txt)
            #         save_box.append(attachment)
            #     else:
            #         join_txt= " ".join(stacking_box)+'\n'
            #         save_box.append(join_txt)

            # 3. ['The motivation of using NMT-src is to test', 'whether the resulting NMT model is more robust', '3http://www.statmt.org/wmt19/translation-task.html']
            # 5. ['Based on these results, we conclude that pretraining the encoder with a masked LM task does not', 'really bring improvement in terms of robustness', 'to unknowns. It seems that BERT does yield improvement for NMT as a better initialization for']
        return [page, save_box] #(page, save_box)


# 1차 
join_box = list()
page = 1 
state = 0
# print(point_loction['abstract'])
# print(point_loction['reference'])
for i in doc_t:
    if dev == False :
        txt = i.get_text().split('\n')
        txt_box = Find_sentence(txt, page) # 문장 찾는 알고리즘 
        join_box.append(txt_box)
    
    if dev == True and page == 3: # DEV
        txt = i.get_text().split('\n')
        txt_box = Find_sentence(txt, page) # 문장 찾는 알고리즘 
        join_box.append(txt_box)
        tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ').replace('~','')}\n " for i in join_box]
        print( )
        print(tmp)
     # print(txt_box)
        break 
    
    page +=1
    
print('Txet Append Done-')

    
# 본문 
save = 0
if save == 1: # ','.join(i[1])
    tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ')}\n " for i in join_box]
    # print(tmp)
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0605.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(tmp))
    fout.close()
        
```

---

### 날짜 -  
```py
"""
22.06.01 - 텍스트 추출 

## 할일 

"""
print(__doc__)

# import 
from turtle import st
import fitz

from DEV import deg_for_test
# import requests
# import time
# import re
 
#------- values ----------
inputFile = '1909.12744.pdf'
doc = fitz.open(inputFile)
doc_t = doc

Special_characters = ['•']
Special_word = ['Table','Figure']

 
#------- Funtions ----------

def Jump_txt():
    # 1. 숫자뒤 
    # 2. )뒤
    pass 


def Table():
    pass 

def Figer():
    pass 

def handling_issue(stacking_box):
    val = stacking_box
    if val[0].isdigit() == True: # 첫글자가 숫자면 
        val.insert(1,' ')
        val.insert(3, '\n')
    return stacking_box

def Remove_hyphens(val,stacking_box, state=0):
    # stacking_box에 다가 문장을 만들도록 담는다. 
    
    if val[-1] == '-': # 하이픈 잇으면 
        val = val[:-1]
        # val = val[:-1] + ' '
        state = 3 # hist
        stacking_box.append(val) # '-' 제거하고 append
    else: # 하이픈이 없는 경우 
        if len(stacking_box) == 0:
            stacking_box.append(val)
            
        else: # stacking_box 내부에 데이터가 있는 경우도 포함 
            # print( )
            
            if stacking_box[-1][-1] == '.': # 리스트에 데이터가 있고 마지막 데이터가 dot 인 경우 
                handling_issue(stacking_box)
                join_txt = "".join(stacking_box) # 합친다. 
                txt = join_txt+'\n'# 추후 수정가능
                # txt = join_txt+'/'# 추후 수정가능
                state = 1
                return txt , state
            else:
                # if 문 이후
                if state == 3:
                    # print(val)
                    stacking_box.append(val)
                    state = 0
                else:
                    # print(val)
                    val = ' '+val
                    stacking_box.append(val)
                
            
    return 'Dev-Remove_hyphens' , state



def Find_sentence(txt, page):
    stacking_box = list()
    save_box = list()
    
    if page == 1:
        base = 'Abstract'
        where_base = [i for i,J in enumerate(txt) if base.lower() == J.lower()][0]  # Abstract 위치 파악 
    
        for idx, val in enumerate(txt):        
            if idx > where_base: # 해당 위치 아래는 진짜 글 
                if len(val) != 0 :
                    j_txt, state = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                    if state == 1:
                        
                        if j_txt[0].isupper() == True:
                            # j_txt = ' '+j_txt# + ' '
                            
                            # print(j_txt)
                            
                            save_box.append(j_txt)
                            print(save_box)
                            deg_for_test(1)
                        else:
                            # print(j_txt)
                            j_txt = ' '+j_txt
                            save_box.append(j_txt)
                        stacking_box = list() # 초기화 
        return [page, save_box]#(page, save_box[0])
    else:
        for idx, val in enumerate(txt):        
            if len(val) != 0 :
                j_txt, state = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                if state == 1:
                    if j_txt[0].isupper() == True: # 숫자면
                        save_box.append(j_txt)
                    elif j_txt[0] in Special_characters:
                        j_txt = '\n'+j_txt+'\n'
                        save_box.append(j_txt)
                        
                    else:
                        # print(j_txt)
                        save_box.append(j_txt)
                    stacking_box = list() # 초기화 
        return [page, save_box] #(page, save_box)


# 1차 
join_box = list()
last_data = 0 
page = 1 

for i in doc_t:
    txt = i.get_text().split('\n')
    txt_box = Find_sentence(txt, page) # 문장 찾는 알고리즘 
    join_box.append(txt_box)
    # print(txt_box)
    
    
    if page == 1: # DEV
        break 
    page +=1
    
    

save = 0 
if save == 1: # ','.join(i[1])
    tmp = [f"\nPage:{str(i[0])} \n {i[1]}\n " for i in join_box]
    # print(tmp)
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0602.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(tmp))
    fout.close()
        
        
 
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