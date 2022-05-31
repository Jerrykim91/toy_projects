

# 쓰레기 





### 날짜 - 머름
```py
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