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
        tmp = [f"\n<Page {str(i[0])}> \n {' '.join(i[1]).replace('@',' ').replace('~','')}\n " for i in join_box]
        print( )
        print(tmp)
        break 
    
    page +=1
print('Txet Append Done-')

    
    
def test_t(writing):
    # 텍스트를 전처리하는 부분에 들어가야 함 - 페이지당 하나만 나옴 
    # print(writing.find(":"))
    idx_num = writing.find(":")
    # writing[:idx_num+1]
    wtf = writing[idx_num-1]
    
    if wtf.isdigit() == True:
        print('-들어감-',wtf.isdigit())
        # 여기서부터 기능 추가 필요 
        # Lines Tokens NMT-src 4.5M 104M Wiki 72M 2086M News 210M 3657M Table 1: Monolingual (English) 
        # Table 1, Figure 기준으로 줄 바꿈 
        # 테이블 앞에 텍스트는 표에서 나온 txt 임으로 처리가 필요 
        # Figure 앞은 << 그림 >> 삽입 하기 
        # 테이블 텍스트 뒤의 데이터는 어떻게 분리하면 좋을지 생각해봐야 할듯 
    
    return int(writing.find(":"))
# 본문 
save = 1
if save == 1: # ','.join(i[1])
    writing = [f"\n<Page {str(i[0])}>\n {' '.join(i[1]).replace('@',' ')}\n " for i in join_box if i != None]
    # print(len(writing)) # page
    
    print(test_t(writing[3])) # 테스트 위치 
    
    import os
    path = os.getcwd()
    # print(path)
    fout = open(os.path.join(path, 'out_0606.txt'), 'w+', encoding='utf-8')
    fout.write(','.join(writing))
    fout.close()
      
        