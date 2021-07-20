from flask import Flask, render_template, session, redirect, request, jsonify
import pandas as pd
import sqlite3
app = Flask(__name__)

# 암호키 생성
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# 데이터베이스 접근
con = sqlite3.connect("database.db", check_same_thread=False)
cur = con.cursor()

# 루트
@app.route("/")
def hello():
    return render_template('index.html')

# db 테이블 확인
@app.route("/youth")
def youth():
    query = cur.execute("SELECT * From youth")
    cols = [column[0] for column in query.description]
    result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    #test = TodoPost()
    html = result.to_html(justify='center')
    return '<h1>Final_code_youth database.db - youth</h1><a href="/">홈화면으로 가기</br></br></a>' + html


# 제목, 링크, 나이, 직업, 소득분위, 지원금 TF json 코드 str 형태로 리턴
@app.route("/jsoncode")
def TodoPost():
    query = cur.execute("SELECT * From youth")
    cols = [column[0] for column in query.description]
    race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    title = race_result[['index', 'title', 'href', 'age_min', 'age_max', 'work', 'area', 'type', 'host']]
    js = title.to_json(orient='records')
    print(type(js))
    print(title)
    return js

@app.route("/sign-up", methods=['POST'])
def sign_up():
    try:
        new_user = request.json
        nickname = new_user.get('nickname')
        id = new_user.get('id')
        pw = new_user.get('pw')
        birth = new_user.get('birth')
        con.execute("INSERT INTO Person VALUES (NULL, ?, ?, ?, ?)", (nickname, id, pw, birth,))
        con.commit()
        return jsonify({"isOK": True})
    except:
        return jsonify({"isOK": False})

@app.route("/login", methods=['POST'])
def login():
    try:
        login_user = request.json
        cur.execute("SELECT * FROM Person WHERE id = ? AND pw = ?", (login_user.get('id'), login_user.get('pw')))
        user_info = cur.fetchone()
        print(cur.fetchall())
        return jsonify({"isValid": True, "nickname": user_info[1], "birth": user_info[4]})
    except:
        return jsonify({"isValid": False, "nickname": "", "birth": ""})

@app.route("/User")
def UserInfo():
     result = cur.execute("SELECT * FROM Person")
     cols = [column[0] for column in result.description]
     result = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
     html = result.to_html(justify='center')
     return '<h1>Final_code_youth database.db - youth</h1><a href="/">홈화면으로 가기</br></br></a>' + html

if __name__ == '__main__':
    app.run(debug=True)
