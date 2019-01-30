# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 15:39:49 2018

@author: xiaozhen
"""

import time
import re
import json
from selenium import webdriver


starttime = time.time()
option = webdriver.ChromeOptions()
# option.add_argument('headless')
browser = webdriver.Chrome(chrome_options=option)
browser.minimize_window()
authors = "沈从文 王维 E·B·怀特 张爱玲 汪曾祺 顾城 苏轼 陶渊明 "
authors = ['李白', '木心', '鲁迅', '王尔德'] + authors.split()
authors = '''孔子 老子 庄子 屈原 诗经 司马迁 陶渊明 韩愈 柳宗元 苏轼 蒋捷 唐伯虎 张岱 汤显祖
            海子 顾城 北岛 钱钟书 杨绛 赫尔曼黑塞 弗吉尼亚·伍尔芙'''
authors = authors.split()
motto_content = []
motto_txt = open('motto.txt', 'w', encoding='utf-8')


for author in authors:
    motto_txt.write('\n\n# ' + author +
                    '\n------------------------------------\n')
    browser.get(u"https://www.juzimi.com")
    browser.find_element_by_id('edit-search-theme-form-1').send_keys(author)
    browser.find_element_by_id('edit-submit-1').click()
    pages = browser.find_element_by_class_name('pager-last')
    pages = int(pages.text)

    # author_motto = []
    for page in range(pages):
        print(f'{author} page:{page}/{pages}')
        try:
            # mottos = browser.find_elements_by_class_name('xlistju')
            mottos = browser.find_elements_by_class_name('views-row')
            for motto in mottos:
                t = motto.text
                t = t.split('喜欢')[0]
                # print(t)
                title = re.search(u'《(.*)》', t)
                if title:
                    title = title.group(1)
                else:
                    title = ''
                content = t.split('——')[0]
                # author_motto.append(motto.text)
                motto_txt.write(t + '\n\n')
                motto_content.append(
                    {'author': author, 'title': title,
                     'paragraphs': [content]})
                print(motto_content[-1])
            if page < pages:
                browser.find_element_by_class_name('pager-next').click()
        except UnicodeEncodeError:
            if page < pages:
                browser.find_element_by_class_name('pager-next').click()
        except Exception as e:
            print(e)

browser.close()
motto_txt.close()
with open('motto.json', 'w', encoding='utf-8') as f:
    json.dump(motto_content, f)

print(f'finished {time.time()-starttime}s')
