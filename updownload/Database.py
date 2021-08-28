import sqlite3
import pandas as pd
from pandas import Series, DataFrame

conn = sqlite3.connect("database.db")
cursor = conn.cursor()


def checkdatabase():
    # all_data 테이블이없으면 all_data 테이블 생성
    cursor.execute("PRAGMA foreing_keys = 1;")
    sql = 'CREATE TABLE IF NOT EXISTS all_data(all_idx INTEGER NOT NULL UNIQUE, title TEXT, age_min INTEGER, age_max INTEGER, area_code INTEGER, area_list TEXT, work TEXT, type TEXT, area TEXT, host TEXT, href TEXT, PRIMARY KEY("all_idx" AUTOINCREMENT))'
    sql2 = "CREATE TABLE IF NOT EXISTS all_data_Exist(E_idx INTEGER PRIMARY KEY AUTOINCREMENT,exist INTEGER, CONSTRAINT all_data_index FOREIGN KEY(E_idx) REFERENCES all_data(all_idx))"
    sql3 = "CREATE TABLE IF NOT EXISTS all_data_Like(L_idx INTEGER PRIMARY KEY AUTOINCREMENT,like INTEGER, CONSTRAINT all_data_index FOREIGN KEY(L_idx) REFERENCES all_data(all_idx))"
    sql4 = "CREATE TABLE IF NOT EXISTS Person(idx INTEGER NOT NULL UNIQUE, nickname TEXT NOT NULL UNIQUE, id TEXT NOT NULL UNIQUE, pw TEXT NOT NULL, birth TEXT NOT NULL,PRIMARY KEY('P_idx' AUTOINCREMENT))"
    sql5 = "CREATE TABLE IF NOT EXISTS Person_Like(PL_idx INTEGER NOT NULL UNIQUE, P_idx INTEGER NOT NULL, ALL_idx INTEGER NOT NULL, PRIMARY KEY('PL_idx' AUTOINCREMENT))"
    sql6 = "CREATE TABLE IF NOT EXISTS Comment(C_idx INTEGER NOT NULL UNIQUE,Comment TEXT, nickname TEXT, P_idx INTEGER NOT NULL, ALL_idx INTEGER NOT NULL, PRIMARY KEY('C_idx' AUTOINCREMENT), FOREIGN KEY(P_idx) REFERENCES Person(idx), FOREIGN KEY(ALL_idx) REFERENCES all_data(all_idx))"

    cursor.execute(sql)
    cursor.execute(sql2)
    cursor.execute(sql3)
    cursor.execute(sql4)
    cursor.execute(sql5)
    cursor.execute(sql6)
    conn.commit()
    # youth 데이터 all_data로 이동


def UpdateAlldata():

    cursor.execute("SELECT all_data.all_idx FROM all_data LEFT OUTER JOIN youth ON youth.title = all_data.title and youth.host = all_data.host WHERE youth.title IS NULL;")

    Removed = cursor.fetchall()

    for alldata_idx in Removed:
        cursor.execute("UPDATE all_data_Exist set exist = 0 WHERE E_idx = '%d'" % alldata_idx)

    cursor.execute(
        "INSERT INTO all_data (title, age_min, age_max, area_code, area_list, work, type, area, host, href) SELECT youth.title, youth.age_min, youth.age_max, youth.area_code, youth.area_list, youth.work, youth.type, youth.area, youth.host, youth.href FROM youth LEFT OUTER JOIN all_data ON youth.title = all_data.title WHERE all_data.title IS NULL;"
    )
    conn.commit()

def NewDataExist():
    cursor.execute("SELECT * FROM all_data ORDER BY ROWID DESC LIMIT 1;")
    last_alldata = cursor.fetchone()
    cursor.execute("SELECT * FROM all_data_Exist ORDER BY ROWID DESC LIMIT 1;")
    last_exist = cursor.fetchone()
    if last_exist is None:
        last_exist = (0, )
    if last_exist[0] != last_alldata[0]:
        for idx in range(last_exist[0] + 1, last_alldata[0]):
            cursor.execute("INSERT INTO all_data_Exist (exist, E_idx) VALUES(?, ?);", (1, idx,))
    conn.commit()

def NewDataJJIM():
    cursor.execute("SELECT * FROM all_data ORDER BY ROWID DESC LIMIT 1;")
    last_alldata = cursor.fetchone()
    cursor.execute("SELECT * FROM all_data_Like ORDER BY ROWID DESC LIMIT 1;")
    last_like = cursor.fetchone()
    if last_like is None:
        last_like = (0, )

    if last_like[0] != last_alldata[0]:
        for idx in range(last_like[0]+1, last_alldata[0]):
            cursor.execute("INSERT INTO all_data_Like (like, L_idx) VALUES(?, ?);", (0, idx,))
    conn.commit()

checkdatabase()
UpdateAlldata()
NewDataExist()
NewDataJJIM()