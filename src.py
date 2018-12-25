# skku_parser.py

import requests

from bs4 import BeautifulSoup

import os

import telegram

#import schedule

import time

# telegram bot variable
bot = telegram.Bot(token=""Insert your token here"")

chat_id = bot.getUpdates()[-1].message.chat.id

print(chat_id)

# location of the file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# all 30 pages raw post
raw_posts = []

# originial_saved_posts
origin_posts = []

# selected_posts
selected_posts = []

keyword = "장학금"

#first parsing
for i in range(1, 11):
    req = requests.get('http://www.skku.edu/new_home/campus/skk_comm/notice_list.jsp?page={}&bCode=0&skey=BOARD_SUBJECT&keyword={}'.format(i, keyword))
    req.encoding = 'utf-8'
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('td.subject')
    for j in posts:
            selected_posts.append(j.text)
def parse_skku():
# parsing_process        
    for i in range(1, 11):
        req = requests.get('http://www.skku.edu/new_home/campus/skk_comm/notice_list.jsp?page={}&bCode=0&skey=BOARD_SUBJECT&keyword={}'.format(i, keyword))
        req.encoding = 'utf-8'
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.select('td.subject')
        for j in posts:
            if j.text not in selected_posts:
                selected_posts.insert(0, j.text)
    compare_posts(selected_posts)
def compare_posts(posts):
    with open(os.path.join(BASE_DIR, 'latest_post.txt'), 'r+') as f_read:
        saved_posts = f_read.readlines()
        print(len(saved_posts))
        print(len(posts))
        if len(saved_posts) != len(posts):
            bot.sendMessage(chat_id=chat_id, text='new post!')

            with open(os.path.join(BASE_DIR, 'latest_post.txt'), 'w+') as f_write:
                for i in posts:
                    f_write.write(i + '\n')
        else:
            bot.sendMessage(chat_id=chat_id, text="<New Post>\n"+selected_posts[0])
while True:
    parse_skku()
    time.sleep(10)
