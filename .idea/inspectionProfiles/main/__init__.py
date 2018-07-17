# coding=utf-8
import requests
import re
import pymysql
from bs4 import BeautifulSoup

#获取文档
def get_content(url):
    response = requests.get(url,timeout=5000)
    soup=BeautifulSoup(response.content,"html.parser")
    return soup

def get_url(url):
    soup = get_content(url)
    #连接MySQL数据库
    db = pymysql.connect("47.98.115.186","root","lp12580","mysql",charset='utf8')
    cursor = db.cursor()

    list_new_url = []
    list_old_url = []
    #获取初始化URL
    for a in soup.find_all("a",attrs={'target':'_blank'}):
        try:
            target_url = a.get("href")
            if re.search(r"data", target_url) and re.search(r"html", target_url):
                list_new_url.append(target_url)
        except:
            continue
    #每新开一个页面都向该页面新加URL，并将打开过的放入老的URL
    for b in list_new_url:
        list_new_url.remove(b)
        if(not(b in list_old_url)):
            text = get_content(url+b)
            for a in text.find_all("a",attrs={'target':'_blank'}):
                try:
                    target_url = a.get("href")
                    if re.search(r"data", target_url) and re.search(r"html", target_url):
                        list_new_url.append(target_url)
                    list_old_url.append(b)
                    list_old_url = list(set(list_old_url))
                except:
                    continue
            sectences = text.find_all("p")
            article = ""
            for p in sectences:
                article = article.strip()  + p.get_text().strip()
            if ("" != article):
                sql = "SELECT * FROM article WHERE name = '%s'" % (b)
                try:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    if (len(result) ==0 ):
                        sql = """INSERT INTO article (name,content) VALUES ('%s','%s')""" % (b,article)
                        try:
                            cursor.execute(sql)
                            db.commit()
                        except:
                            print("insert wrong")
                except:
                    print("select wrong")
        print(str(len(list_old_url))+"---"+str(len(list_new_url)))
    db.close()
                 #file = open("D:/example"+ b +".txt",'wb+')
                 #file.write(article.encode("GBK", 'ignore'))

think_url = "http://www.aisixiang.com"
get_url(think_url)