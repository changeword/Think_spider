# coding=utf-8
import requests
import re
import pymysql
from bs4 import BeautifulSoup

#获取文档
def get_content(url):
    maxTryNum = 5
    for tries in range(maxTryNum):
        try:
            response = requests.get(url,timeout=500)
            soup=BeautifulSoup(response.content,"html.parser")
            return soup
        except:
            if tries < (maxTryNum-1):
                continue
            else:
                print("连接出错",maxTryNum,url)
                break

#递归查询下一页的文章
def deal_sectences(text,url,article,flag,b):
    sectences = text.find_all("p")
    ##查找是否包含下一页
    nextPages = text.find_all("a",string = re.compile("点击此处阅读下一页"))
    for p in sectences:
        if("进入专题" in p.get_text()):
            flag = flag + 1
        if("本文责编" in p.get_text() or "在方框中输入电子邮件地址" in p.get_text() or "的专栏" in p.get_text()):
           a = 1
        else:
            ##进入专题只让出现一次
            if("进入专题" in p.get_text()):
                if(flag==1):
                    article = article  + p.get_text()
            else:
                article = article  + p.get_text()
    if(len(nextPages)>0):
        for nextPage in nextPages:
            nextPageUrl = nextPage.get("href")
            nextSoup = get_content(url+nextPageUrl)
            deal_sectences(nextSoup,url,article,flag,b)

    #连接MySQL数据库
    db = pymysql.connect("47.98.115.186","root","lp12580","mysql",charset='utf8')
    cursor = db.cursor()
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

def get_url(url):
    soup = get_content(url)
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
            article = ""
            flag = 0

            article = deal_sectences(text,url,article,flag,b)
        print(str(len(list_old_url))+"---"+str(len(list_new_url)))
    db.close()
                 #file = open("D:/example"+ b +".txt",'wb+')
                 #file.write(article.encode("GBK", 'ignore'))
think_url = "http://www.aisixiang.com"
get_url(think_url)