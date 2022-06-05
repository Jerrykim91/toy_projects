

import fitz


# pno = 3
# page = doc.load_page(pno)  # loads page number 'pno' of the document (0-based)
# page = doc[pno]  # the short form - output) page 1 of 1909.12744.pdf
# page = doc[-pno] # 뒤에서부터 페이지 

# print(page)

# start, stop, step = 1, 4, 2
# for page in doc.pages(start, stop, step):
#     print(page)


# links = page.get_links()
# print(links)
# base = 'reference'

# for page in doc:
#     # base = 'abstract'
#     areas = page.search_for(base) # 대소문자를 구분하지 않음 - 글자가 존재하는 위치를 찾아줌 
#     print(areas)#.get_text())
    
Point_word = ['abstract','reference']
def find_point_page(doc,Point_word):
    send_point = dict()
    for point in Point_word:
        test = [(point, int(str(page).split(' ')[1])+1) for page in doc if len(page.search_for(point)) != 0 ]
        
        if point == 'reference':
            send_point[point] = test[-1][1]
        else: 
            send_point[point] = test[0][1]
    return send_point



if __name__ == '__main__':
    inputFile = '1909.12744.pdf'
    doc = fitz.open(inputFile)

    Point_word = ['abstract','reference',]
    print(find_point_page(doc,Point_word))
    # for page in doc:
    #     print(str(page).split(' ')[1])