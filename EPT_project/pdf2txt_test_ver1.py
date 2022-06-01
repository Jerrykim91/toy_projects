# 22.05.20

import pdfminer
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams

import cv2
from io import StringIO
from pdf2image import convert_from_path
import numpy as np
import matplotlib.pyplot as plt


fname = '1909.12744.pdf'

layout_type = ['LTTextBox', 'LTFigure', 'LTImage', 'LTCurve', 'LTRect']
color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (160, 32, 240)]

draw_color = dict(zip(layout_type, color))
fp = open(fname, 'rb')

def parse_obj(lt_objs):
    
    boxs = {x: [] for x in layout_type}
    # loop over the object list
    for obj in lt_objs:

        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            boxs['LTTextBox'].append(obj.bbox)
#         elif isinstance(obj, pdfminer.layout.LTFigure):
#             boxs['LTFigure'].append(obj.bbox)
#         elif isinstance(obj, pdfminer.layout.LTImage):
#             boxs['LTImage'].append(obj.bbox)
#         elif isinstance(obj, pdfminer.layout.LTCurve):
#             boxs['LTCurve'].append(obj.bbox)
#         elif isinstance(obj, pdfminer.layout.LTRect):
#             boxs['LTRect'].append(obj.bbox)
        else:
            pass
            #raise
    return boxs



# image = convert_from_path(fname)

fp = open(fname, 'rb')
parser = PDFParser(fp)
password = ''
document = PDFDocument(parser, password)

if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

    
rsrcmgr = PDFResourceManager()

# Set parameters for analysis.
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)

page_boxs = []
for page in PDFPage.create_pages(document):
    interpreter.process_page(page)
    # receive the LTPage object for the page.
    layout = device.get_result()
    # extract text from this object
    boxs = parse_obj(layout._objs)
    page_sized = tuple([round(i) for i in layout.bbox])
    page_boxs.append((page_sized, boxs))
    pass

image = convert_from_path(fname)

assert len(image) == len(page_boxs), "The number of boxes doesn't match the number of pictures"
for i in range(len(image)):
    image_pil = image[i]
    image_numpy = np.array(image_pil)

    page_boxs_height = page_boxs[i][0][3]
    page_size = page_boxs[i][0]
    box_cnt = len(page_boxs[i][1]['LTTextBox'])
    # print(page_boxs[i][1])
    print(page_boxs_height)
    print(box_cnt)

    for key, values in page_boxs[i][1].items():

        image_numpy = cv2.resize(image_numpy, page_boxs[i][0][2:4], interpolation=cv2.INTER_AREA)
        for value in values:
            # The y-coordinates are given as the distance from the bottom of the page.
            real_box = (value[0], page_boxs_height-value[3], value[2], page_boxs_height-value[1])
            real_box_integer = tuple([round(jj) for jj in real_box])
            cv2.rectangle(image_numpy, real_box_integer[:2], real_box_integer[2:], draw_color[key], 2)
#             cv2.rectangle(image_numpy, real_box_integer[:2], real_box_integer[2:], 'Black', 2)
    plt.figure(figsize=(10,15)), plt.imshow(image_numpy)
    plt.show()