import pymysql


db = pymysql.connect("47.98.115.186","root","lp12580","mysql",charset='utf8' )
cursor = db.cursor()
sql = "SELECT * FROM article WHERE name = '%s'" % ("13.html.txt")
try:
    cursor.execute(sql)
    result = cursor.fetchall()
    if (len(result) ==0 ):
        print("True")
        sql = """INSERT INTO article (name,content) VALUES ('%s','%s')""" % ("李攀","李攀")
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print("insert wrong")

except:
    print("select Error")
db.close()