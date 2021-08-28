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
    query = cur.execute("SELECT * From all_data")
    cols = [column[0] for column in query.description]
    result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    html = result.to_html(justify='center')
    return '<h1>Final_code_youth database.db - youth</h1><a href="/">홈화면으로 가기</br></br></a>' + html


# 제목, 링크, 나이, 직업, 소득분위, 지원금 TF json 코드 str 형태로 리턴
@app.route("/jsoncode")
def TodoPost():
    query = cur.execute("SELECT * From all_data")
    cols = [column[0] for column in query.description]
    race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    title = race_result[['all_idx', 'title', 'href', 'age_min', 'age_max', 'work', 'area', 'type', 'host']]
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
        return jsonify({"isValid": True, "usernum": user_info[0], "nickname": user_info[1], "birth": user_info[4]})
    except:
        return jsonify({"isValid": False, "usernum": 0, "nickname": "", "birth": ""})


@app.route("/User")
def UserInfo():
    result = cur.execute("SELECT * FROM Person INNER JOIN Person_Like ON Person.idx = Person_Like.P_idx")
    cols = [column[0] for column in result.description]
    result = pd.DataFrame.from_records(data=result.fetchall(), columns=cols)
    html = result.to_html(justify='center')
    return '<h1>User</h1><a href="/">홈화면으로 가기</br></br></a>' + html


@app.route("/Search", methods=['POST'])
def Search():
    try:
        keyword = request.json
        query = cur.execute("SELECT * FROM all_data INNER JOIN all_data_Like ON all_data.all_idx = all_data_Like.L_idx WHERE title LIKE '%" + keyword.get('keyword') + "%'")
        cols = [column[0] for column in query.description]
        race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        title = race_result[['all_idx', 'title', 'href', 'age_min', 'age_max', 'work', 'area', 'type', 'host']]
        js = title.to_json(orient='records')
        return js
    except:
        return jsonify([{"all_idx": 0, "title": "", "href": "", "age_min": 0, "age_max": 0, "work": "", "area": "",
                         "type": "", "host": ""}])


@app.route("/Like/GetLike", methods=['POST'])
def Push_Post_Like():
    # 게시물의 찜 횟수
    try:
        json = request.json
        idx = json.get('idx')
        cur.execute("SELECT * FROM all_data_Like WHERE L_idx = ?", (idx,))
        result = cur.fetchone()
        print(result)
        return jsonify({"idx": idx, "num": result[1]})
    except:
        return jsonify({"idx": 0, "num": 0})


@app.route("/Like/Users", methods=['POST'])
def PUSH_USER_Like():
    # 유저가 어떤 걸 찜했는지
    try:
        p_idx = request.json
        query = cur.execute("SELECT ALL_idx FROM Person_Like WHERE P_idx = " + str(p_idx.get('P_idx')))
        result = query.fetchall()
        js = pd.DataFrame(
            columns=['all_idx', 'title', 'href', 'age_min', 'age_max', 'work', 'area', 'type', 'host', 'area_code'])
        for num in result:
            print(num)
            query = cur.execute("SELECT * FROM all_data WHERE all_idx = ?", (num[0],))
            cols = [column[0] for column in query.description]
            race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            js = pd.concat([js, race_result])
        return js.to_json(orient='records')
    except:
        return jsonify([{"all_idx": 0, "title": "", "href": "", "age_min": 0, "age_max": 0, "work": "", "area": "",
                         "type": "", "host": "", "like": ""}])


@app.route("/Like/Update", methods=['POST'])
def Update_JJIM():
    try:
        json = request.json
        cur.execute("INSERT INTO Person_Like VALUES (NULL, ?, ?)", (json.get('P_idx'), json.get('ALL_idx')))
        cur.execute("SELECT like FROM all_data_Like WHERE L_idx = ?", (json.get('ALL_idx'),))
        num = cur.fetchone()
        cur.execute("UPDATE all_data_Like SET like = ? WHERE L_idx = ?", (num[0] + 1, json.get('ALL_idx')))
        con.commit()
        return jsonify({"Check": True})
    except:
        return jsonify({"Check": False})

@app.route("/Like/Delete", methods=['POST'])
def Delete_JJIM():
    try:
        json = request.json
        cur.execute("DELETE FROM Person_Like WHERE P_idx = ? AND ALL_idx = ?", (json.get('P_idx'), json.get('ALL_idx')))
        cur.execute("SELECT like FROM all_data_Like WHERE L_idx = ?", (json.get('ALL_idx'),))
        num = cur.fetchone()
        cur.execute("UPDATE all_data_Like SET like = ? WHERE L_idx = ? AND NOT like = 0",
                    (num[0] - 1, json.get('ALL_idx')))
        con.commit()
        return jsonify({"Check": True})
    except:
        return jsonify({"Check": False})

@app.route("/Like/List", methods=['POST'])
def List_JJIM():
    try:
        query = cur.execute("SELECT * FROM all_data_like")
        cols = [column[0] for column in query.description]
        race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        title = race_result[['L_idx', 'like']]
        js = title.to_json(orient='records')
        return js
    except:
        return jsonify([{"L_idx": 0, "Like": 0}])

@app.route("/popular", methods=['POST'])
def Popular_List():
    try:
        query = cur.execute("SELECT * From all_data INNER JOIN all_data_Like ON all_data.all_idx = all_data_Like.L_idx")
        cols = [column[0] for column in query.description]
        race_result = pd.DataFrame.from_records(data=query.fetchall(),columns=cols)
        race_result.sort_values(by=['like'], axis=0, ascending=False, inplace=True)
        title = race_result[['all_idx', 'title', 'href', 'host', 'like']]
        js = title.to_json(orient='records')
        return js
    except:
        return jsonify([{"all_idx": 0, "title": "", "href": "", "host": "", "like": 0}])

@app.route("/new", methods=['POST'])
def New_List():
    try:
        query = cur.execute("SELECT * From all_data INNER JOIN all_data_Like ON all_data.all_idx = all_data_Like.L_idx")
        cols = [column[0] for column in query.description]
        race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        race_result.sort_values(by=['all_idx'], axis=0, ascending=False, inplace=True)
        race = race_result.head(30)
        title = race[['all_idx', 'title', 'href', 'host', 'like']]
        js = title.to_json(orient='records')
        return js
    except:
        return jsonify([{"all_idx": 0, "title": "", "href": "", "host": "", "like": 0}])

@app.route("/comment/add", methods=['POST'])
def Comment_add():
    try:
        json = request.json
        cur.execute("SELECT nickname FROM Person WHERE idx = ?", (json.get('P_idx'),))
        nickname = cur.fetchone()
        cur.execute("INSERT INTO Comment VALUES (NULL, ?, ?, ?, ?)",
                    (json.get('Comment'), nickname[0], json.get('P_idx'), json.get('ALL_idx')))
        con.commit()
        query = cur.execute("SELECT * FROM Comment")
        cols = [column[0] for column in query.description]
        race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        title = race_result[['C_idx', 'Comment', 'nickname', 'P_idx', 'ALL_idx']]
        js = title.to_json(orient='records')
        return js
    except:
        return jsonify([{"C_idx": 0, "Comment": "", "nickname": "", "P_idx": 0, "ALL_idx": 0}])

@app.route("/comment/delete", methods=['POST'])
def Comment_delete():
    try:
        json = request.json
        cur.execute("DELETE FROM Comment WHERE C_idx = ?", (json.get('C_idx'),))
        con.commit()
        query = cur.execute("SELECT * FROM Comment")
        cols = [column[0] for column in query.description]
        race_result = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        title = race_result[['C_idx', 'Comment', 'nickname', 'P_idx', 'ALL_idx']]
        js = title.to_json(orient='records')
        return js
    except:
        return jsonify([{"C_idx": 0, "Comment": "", "nickname": "", "P_idx": 0, "ALL_idx": 0}])

if __name__ == '__main__':
    app.run(host='172.30.1.2', port=5000, debug=False)
