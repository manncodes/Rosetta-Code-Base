# -*- coding: utf-8 -*-
"""RosettaCodeBaseScrapper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    ~~~
"""

import pandas as pd
import pprint as pp
import time
from multiprocessing.pool import ThreadPool as Pool
import concurrent
# import ast

import requests
from bs4 import BeautifulSoup
URL  = "http://www.rosettacode.org/wiki/Category:Programming_Tasks"
r=requests.get(URL)
soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())

programming_task_links = []
table = soup.find('div',attrs={'id':'mw-pages'})
# print(table)
idx =0
for li in table.findAll('li'):
  task = 'http://www.rosettacode.org'+li.a['href']
  print( str(idx)+ ":"+ str(task))
  idx=idx+1
  programming_task_links.append(task)

len(programming_task_links)

# # individual task scrapping
# task = {}
# URL = "http://www.rosettacode.org/wiki/100_prisoners"
# r=requests.get(URL)
# task_soup = BeautifulSoup(r.content, 'html5lib')
# task['task_name'] =task_soup.find('h1',attrs={'id':'firstHeading'}).text
# task['task_info']= task_soup.find('div',attrs={'id':'mw-content-text'}).text.split('Contents')[0]

# langs = ['c','cpp','','java','python']

# for lang in langs:
#   langblocks = task_soup.findAll('pre',attrs={'class':lang+' highlighted_source'})
#   for block in langblocks: 
#     task[lang] = block.text.encode('ascii', 'ignore').decode('unicode_escape').replace('\t',' ')
#     # task[lang] = ast.literal_eval(block.text.encode('ascii', 'ignore').decode('unicode_escape'))

# #use this as the dict labels
# # for lang in task_code:
# #   lang_name = lang['id']
# #   lang_code = 
# pp.pprint(task)

all_tasks = {}

## tried multithreading,not working :( ISSUE : Same item is being processed again by worker function.
# pool_size = 5
# def worker(task_URL):
#     try:
#         start_time = time.time()
#         task={}
#         task_r = requests.get(task_URL)
#         task_soup = BeautifulSoup(task_r.content,'html5lib')
#         task['task_name'] =task_soup.find('h1',attrs={'id':'firstHeading'})
#         task['task_info']= task_soup.find('div',attrs={'id':'mw-content-text'}).text.split('Contents')[0]
#         langs = ['c','cpp','','java','python']
#         for lang in langs:
#           langblocks = task_soup.findAll('pre',attrs={'class':lang+' highlighted_source'})
#           for block in langblocks: 
#             task[lang] = block.text.encode('ascii', 'ignore').decode('unicode_escape').replace('\t','    ')
#             # task[lang] = ast.literal_eval(block.text.encode('ascii', 'ignore').decode('unicode_escape'))
#         end_time = time.time()
#         pp.pprint(str(task['task_name'])+str(end_time - start_time))
#         all_tasks[task['task_name']] = task
#     except:
#         print('error with item')

# executor = concurrent.futures.ProcessPoolExecutor(5)
# futures = [executor.submit(worker, task_URL) for task_URL in programming_task_links]
# concurrent.futures.wait(futures)

for task_URL in programming_task_links[409:]:
  start_time = time.time()
  task={}
  task_r = requests.get(task_URL)
  task_soup = BeautifulSoup(task_r.content,'html5lib')
  task['task_name'] =task_soup.find('h1',attrs={'id':'firstHeading'}).text
  task['task_info']= task_soup.find('div',attrs={'id':'mw-content-text'}).text.split('Contents')[0]
  langs = ['c','cpp','','java','python']
  for lang in langs:
    langblocks = task_soup.findAll('pre',attrs={'class':lang+' highlighted_source'})
    for block in langblocks: 
      try:
        task[lang] = block.text.encode('ascii', 'ignore').decode('unicode_escape').replace('\t','    ')
        # task[lang] = ast.literal_eval(block.text.encode('ascii', 'ignore').decode('unicode_escape'))
      except:
        print("error encoding")
  end_time = time.time()
  print(str(task['task_name'])+' : '+str(end_time - start_time))
  all_tasks[task['task_name']] = task

pp.pprint(all_tasks)

list_of_all_task = [value for value in all_tasks.values()]

df = pd.DataFrame.from_dict(list_of_all_task)

df = df.iloc[2:]

df

df.to_csv('rosettaCodeBank.csv',index=False)
df.to_json('rosettaCodeBank.json')