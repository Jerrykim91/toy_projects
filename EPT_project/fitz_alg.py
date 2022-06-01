"""
22.06.01 - 텍스트 추출 

## 할일 

"""
print(__doc__)

# import 
import fitz
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

def Remove_hyphens(val,stacking_box, state=0):
    # stacking_box에 다가 문장을 만들도록 담는다. 
    
    if val[-1] == '-':
        val = val[:-1]
        stacking_box.append(val) # '-' 제거하고 append
    else: # 하이픈이 없는 경우 
        if len(stacking_box) == 0:
            stacking_box.append(val)
        else: # stacking_box 내부에 데이터가 있는 경우도 포함 
            stacking_box.append(val)
            # print( )
            if stacking_box[-1][-1] == '.': # 리스트에 데이터가 있고 마지막 데이터가 dot 인 경우 
                join_txt = "".join(stacking_box) # 합친다. 
                txt = join_txt+'\n'# 추후 수정가능
                # txt = join_txt+'/'# 추후 수정가능
                state = 1
                return txt , state
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
                            save_box.append(j_txt)
                        else:
                            # print(j_txt)
                            """
                            # 이걸 어떻게 해결하나 몰라 - 하이픈은 아님 
                            - 1IntroductionPretrained Language Models (LM) 
                            such as ELMOand BERT (Peters et al., 2018; Devlin et al.,2018) have turned out to signiﬁcantly 
                            - 2Related WorksThe
                            - 3MethodsTypical
                            """
                            save_box.append(j_txt)
                        stacking_box = list() # 초기화 
        return [page, save_box]#(page, save_box[0])
    else:
        for idx, val in enumerate(txt[:]):        
            if len(val) != 0 :
                j_txt, state = Remove_hyphens(val, stacking_box) # 하이픈 제거하는 알고리즘
                if state == 1:
                    if j_txt[0].isupper() == True: # 숫자면
                        save_box.append(j_txt)
                    elif j_txt[0] in Special_characters:
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
    
    
    # if page == 6: # DEV
    #     break 
    page +=1
    
    

save = 1 
if save == 1:
    tmp = [f"\nPage:{str(i[0])} \n {','.join(i[1])}\n " for i in join_box]
    print(tmp)
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0601.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(tmp))
    fout.close()
        
        