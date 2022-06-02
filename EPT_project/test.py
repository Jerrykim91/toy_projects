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

dev = True

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
    # print(val)
    if val[0].isdigit() == True: # 첫글자가 숫자면 
        # print(val)
        val.insert(1,' ')
        val.insert(3, '\n')
    return stacking_box

def Remove_hyphens(val,stacking_box, state=0):
    if dev == False :
        print(val)
        # stacking_box에 다가 문장을 만들도록 담는다. 
        if val[-1] == '-': # 하이픈 잇으면 
            val = val[:-1]
            stacking_box.append(val) # '-' 제거하고 append
            
        else: # 하이픈이 없는 경우 
            if len(stacking_box) == 0 or val[0].isupper() == True:
                stacking_box.append(val)
                stacking_box.append('@')
                
            else: # stacking_box 내부에 데이터가 있는 경우도 포함 
                if stacking_box[-1][-1] == '.': # 리스트에 데이터가 있고 마지막 데이터가 dot 인 경우 
                    handling_issue(stacking_box)
                    join_txt = "".join(stacking_box) # 합친다. 
                    txt = join_txt+'\n'# 추후 수정가능
                    # txt = join_txt+'/'# 추후 수정가능
                    state = 1
                    return txt , state
                else:
                    # val = ' '+val
                    if stacking_box[-1][-1].islower() == True and val[0].islower() == True:
                        # print('heyyyy',val,stacking_box[-1][-1])
                        stacking_box.append('@')
                        stacking_box.append(val)
                    else:
                        stacking_box.append(val)
                
        return 'Dev-Remove_hyphens' , state
    else:
        # 일단 리스트에 다담아 
        if len(stacking_box) <= 0:
            stacking_box.append(val)
        else:
            if stacking_box[-1][-1] == '-':
                pop_data = stacking_box.pop(-1)
                push_data = pop_data[:-1]+val
                stacking_box.append(push_data)
                print(push_data)
                print( )
            else:
                stacking_box.append(val)
        # print(stacking_box)
        return 'Dev-Remove_hyphens' , state
            
        # if val[-1] == '-': # 하이픈 잇으면 
        #     val = val[:-1]
        #     stacking_box.append(val) # '-' 제거하고 append
            
        # else: # 하이픈이 없는 경우 
        #     if len(stacking_box) == 0 or val[0].isupper() == True:
        #         stacking_box.append(val)
        #         stacking_box.append('@')
                
        #     else: # stacking_box 내부에 데이터가 있는 경우도 포함 
        #         if stacking_box[-1][-1] == '.': # 리스트에 데이터가 있고 마지막 데이터가 dot 인 경우 
        #             handling_issue(stacking_box)
        #             join_txt = "".join(stacking_box) # 합친다. 
        #             txt = join_txt+'\n'# 추후 수정가능
        #             # txt = join_txt+'/'# 추후 수정가능
        #             state = 1
        #             return txt , state
        #         else:
        #             # val = ' '+val
        #             if stacking_box[-1][-1].islower() == True and val[0].islower() == True:
        #                 # print('heyyyy',val,stacking_box[-1][-1])
        #                 stacking_box.append('@')
        #                 stacking_box.append(val)
        #             else:
        #                 stacking_box.append(val)
                
        # return 'Dev-Remove_hyphens' , state




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
                            save_box.append(j_txt)
                            # deg_for_test(1)
                        else:
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
                        save_box.append(j_txt)
                    stacking_box = list() # 초기화 
        return [page, save_box] #(page, save_box)


# 1차 
join_box = list()
last_data = 0 
page = 1 
state = 0

for i in doc_t:
    
    if page == 2: # DEV
        txt = i.get_text().split('\n')
        txt_box = Find_sentence(txt, page) # 문장 찾는 알고리즘 
        join_box.append(txt_box)
     # print(txt_box)
        break 
    page +=1
    
tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ')}\n " for i in join_box]
print(tmp)
    

save = 0 
if save == 1: # ','.join(i[1])
    
    tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ')}\n " for i in join_box]
    print(tmp)
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0602.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(tmp))
    fout.close()
        
        