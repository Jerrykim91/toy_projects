# from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
# from pdfminer.converter import TextConverter
# from pdfminer.layout import LAParams
# from pdfminer.pdfpage import PDFPage
# from io import StringIO
# import os


# def convert_pdf_to_txt(path, fname, maxpages=10):
#     rsrcmgr = PDFResourceManager()
#     retstr = StringIO()
#     codec = 'utf-8'
#     laparams = LAParams()
#     device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
#     fp = open(os.path.join(path, fname), 'rb')
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     pw = ""
#     caching = True
#     pagenos = set()
    
#     for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=pw, caching=caching, check_extractable=True):
#         interpreter.process_page(page)
# #         layout = device.get_result() # 페이지 수
# #         print(layout)
#     text = retstr.getvalue()#.decode('utf-8-sig')
    
#     fp.close()
#     device.close()
#     retstr.close()
#     return text


# path = os.getcwd()
# fname = '1909.12744.pdf'
# v = convert_pdf_to_txt(path, fname, maxpages=32)
# print(v)
# fout = open(os.path.join(path, 'ref_01.txt'), 'w+', encoding='utf-8')
# fout.write(v)
# fout.close()



import os 
from io import StringIO
from pdfminer.high_level import extract_text_to_fp



path = os.getcwd()
fname = '1909.12744.pdf'


output_string = StringIO()
with open(os.path.join(path, fname), 'rb') as fin:
    extract_text_to_fp(fin, output_string)
print(output_string.getvalue())