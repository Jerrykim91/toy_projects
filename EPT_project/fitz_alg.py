"""
22.06.03 - 텍스트 추출 

## 할일 

"""
print(__doc__)

# import 
import fitz
from regex import E


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
    
    if page == 1:
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
save = 1 
if save == 1: # ','.join(i[1])
    tmp = [f"\nPage:{str(i[0])} \n {' '.join(i[1]).replace('@',' ')}\n " for i in join_box]
    # print(tmp)
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0604.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(tmp))
    fout.close()
        