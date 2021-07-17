from flask import Flask, render_template, session
import pandas as pd
from flask_login import LoginManager
from pandas import Series, DataFrame
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
login_manager = LoginManager()
login_manager.init_app(app)



# 루트
@app.route("/")
def hello():
    return render_template('index.html')


# db테이블확인
@app.route("/youth")
def youth():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    query = cur.execute("SELECT * From youth")
    cols = [column[0] for column in query.description]
    result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    con.close()
    #test = TodoPost()
    html = result.to_html(justify='center')
    return '<h1>Final_code_youth database.db - youth</h1><a href="/">홈화면으로 가기</br></br></a>' + html


# 제목, 링크, 나이, 직업, 소득분위, 지원금TF json 코드 str형태로 리턴
@app.route("/jsoncode")
def TodoPost():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    query = cur.execute("SELECT * From youth")
    cols = [column[0] for column in query.description]
    race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    title = race_result[['index', 'title', 'href', 'age_min', 'age_max', 'work', 'area', 'type', 'host']]
    js = title.to_json(orient='records')
    print(type(js))
    print(title)
    return js

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)
