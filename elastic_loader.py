import string
import sys

import sys
import filter_sent

from elasticsearch import Elasticsearch
import xml.etree.ElementTree as ET

es = Elasticsearch()
TMX = '/home/igor/ARCH/en-ru.tmx'
v = False
with open(TMX) as source:
    context = iter(ET.iterparse(source, events=('start', 'end')))
    _, root = next(context)
    num = 1
    all_num=1
    for event, elem in context:
        if event == 'end' and elem.tag == 'tu':
            doc = {
                'eng': elem[0][0].text,
                'rus': elem[1][0].text,
                'len': len(elem[0][0].text)
            }
            all_num+=1
            if v: print('----')
            en_txt = elem[0][0].text
            if v: print(en_txt)
            res = filter_sent.filter_string(en_txt, v=False)
            if v: print(res)
            if res[0]:
                pass
            else:
                elem.clear()
                continue

            res_es = es.index(index="words25", id=num, body=doc)
            num += 1
            elem.clear()
            # print (doc)
            #if num > 4960000:
            #    break
            if num % 1000 == 0:
                print(all_num, "loaded=", num)

if __name__ == '__main__':
    print('---')
