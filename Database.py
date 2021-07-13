import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

#all_data 테이블이없으면 all_data 테이블 생성
sql = "CREATE TABLE IF NOT EXISTS all_data(idx INTEGER PRIMARY KEY, title TEXT, age_min INTEGER, age_max INTEGER, area_code INTEGER, area_list TEXT, work TEXT, type TEXT, area TEXT, host TEXT, href TEXT)"
sql2 = "CREATE TABLE IF NOT EXISTS all_data_Exist(idx INTEGER PRIMARY KEY AUTOINCREMENT,exist INTEGER, CONSTRAINT all_data_index FOREIGN KEY(idx) REFERENCES all_data(idx))"

cursor.execute(sql)
cursor.execute(sql2)
conn.commit()

#youth 데이터 all_data로 이동
cursor.execute("INSERT INTO all_data SELECT * FROM youth;")
conn.commit()


