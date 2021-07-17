import sqlite3
import pandas as pd
from pandas import Series, DataFrame

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def checkdatabase():
    # all_data 테이블이없으면 all_data 테이블 생성
    sql = "CREATE TABLE IF NOT EXISTS all_data(idx INTEGER PRIMARY KEY, title TEXT, age_min INTEGER, age_max INTEGER, area_code INTEGER, area_list TEXT, work TEXT, type TEXT, area TEXT, host TEXT, href TEXT)"
    sql2 = "CREATE TABLE IF NOT EXISTS all_data_Exist(idx INTEGER PRIMARY KEY AUTOINCREMENT,exist INTEGER, CONSTRAINT all_data_index FOREIGN KEY(idx) REFERENCES all_data(idx))"

    cursor.execute(sql)
    cursor.execute(sql2)
    # youth 데이터 all_data로 이동
    conn.commit()


def UpdateAlldata():
    cursor.execute("SELECT * FROM youth")
    youth = cursor.fetchall()
    cursor.execute("SELECT * FROM all_data")
    alldata = cursor.fetchall()

    index_num = []

    if len(youth) > len(alldata):
        InsertData(youth, alldata, index_num)
    elif len(youth) < len(alldata):
        DeleteData(youth, alldata, index_num)


def InsertData(youth, alldata, index_num):
    print("Insert Data")
    check = True
    # youth의 인덱스가 alldata보다 많을 경우 -> 새롭게 지원금 게시물이 올라온 경우
    for i in youth:
        check = True
        for j in alldata:
            if i == j:
                check = False
                break
        if check == True:
            print(i)
            index_num.append(i[0])

    for insertion in index_num:
        cursor.execute('SELECT * FROM youth WHERE index="%d" ')
        insert_data = cursor.fetchone()
        sql = 'INSERT INTO all_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        print(cursor.execute(sql, insert_data))
    print(index_num)


def DeleteData(youth, alldata, index_num):
    print("Delete Data")
    check = True
    # youth의 인덱스가 alldata보다 적을 경우 -> 지원금게시물이 하나 삭제된 경우
    for i in alldata:
        check = True
        for j in youth:
            if i == j:
                check = False
                break
        if check == True:
            print(i[0])
            index_num.append(i[0])

    print(index_num)

    # cursor.execute("INSERT INTO all_data SELECT * FROM youth;")


checkdatabase()
UpdateAlldata()
conn.commit()
