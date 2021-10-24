from flask import Flask, request, render_template

import hashlib

import cx_Oracle as cx

host = "192.168.200.154"
port = 1521
user = "mina"
password = "120408"
sid = "xe"

dsn = cx.makedsn(host, port, sid)
conn = cx.connect(user, password, dsn)
cursor = conn.cursor()  # connection 객체로부터 cursor()메서드를 호출하여 Cursor 객체를 가져옴
cursor.execute("SELECT * FROM users")

x = cursor.fetchall()  # 모든 데이터를 한꺼번에 클라이언트로 가져올 때


print(x)  # >> [(행),(행)]
print(type(x))  # >> list

print(type(x[0]))  # >> tuple
print('mina2193' in x[0])


login = Flask(__name__)


@login.route('/', methods=["GET", "POST"])
def user_login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        try:
            condition = cursor.execute(
                f"select * from users where user_id = '{request.form['id']}'")
            condition = list(condition)
            hash = hashlib.sha256(
                (request.form['password']).encode('utf-8')).hexdigest()
            if condition[0][1] == hash:
                return render_template('success.html')
            else:
                return render_template('login.html', pw_fail="비밀번호를 다시 입력해주세요!")
        except:
            return render_template('login.html', fail="아이디가 없으시다면 회원가입을 해주세요!")


@login.route('/join', methods=["GET", "POST"])
def user_join():
    if request.method == "GET":
        return render_template('join.html')
    elif request.method == "POST":
        try:
            id_success = "이 아이디는 사용하실 수 있습니다!"
            id_fail = "아이디가 중복되었습니다. 다시 입력해주세요!"
            for i in x:
                if request.form['id'] not in i[0]:
                    continue
                else:
                    return render_template('join.html', id_fail=id_fail)
            if request.form['password1'] == request.form['password2']:
                sql_insert = 'INSERT INTO users (user_id, password, e_mail, region) VALUES (:u_id, :u_password, :u_email, :region)'
                u_id = request.form['id']
                u_password = hashlib.sha256(
                    (request.form['password1']).encode('utf-8')).hexdigest()
                u_email = request.form['email']
                u_region = request.form['region']
                cursor.execute(
                    sql_insert, (u_id, u_password, u_email, u_region))
                conn.commit()
                return render_template('join_success.html', id_success=id_success)
            else:
                pw_fail = "비밀번호가 일치하지 않습니다. 다시 입력해주세요!"
                return render_template('join.html', pw_fail=pw_fail, id_success=id_success)
        except:
            return render_template('join.html', id_success=id_success)


if __name__ == '__main__':
    login.run(port=8000, debug=True)
