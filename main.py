import sqlite3
import json
from random import randint

from bottle import run
from bottle import HTTPResponse
from bottle import request
from bottle import get
from bottle import post


#=== settings ===
hostname = 'spajam.hnron.net'
port = 8080
db_name = 'spajam.db'
FLAG_QUESTION = 'question'
FLAG_COMING_OUT = 'coming_out'
FLAG_NONE = None
#=== end ===


@post('/create_group')
def create_group_handler():
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    password = randint(0, 9999)

    while 1:
        if c.execute('''select count(*) from groups where password = ?''', (password, )).fetchone()[0] >= 1:
            password = randint(0, 9999)
        else:
            break

    c.execute('''insert into groups(password) values (?) ''', (password, ))
    group_id = c.lastrowid

    # for i in c.execute('''select id from groups where password = ?''', (password, )):
    #     group_id = i[0]

    # userの作成と、作成したuser_idの取得
    c.execute('''insert into users(group_id) values (?) ''', (group_id, ))
    user_id = c.lastrowid

    c.execute('''UPDATE groups SET number_of_people = (number_of_people + 1) WHERE id = ?''', (group_id, ))

    conn.commit()
    conn.close()

    # response作成
    body = json.dumps({"user_id": user_id, "group_id": group_id, "password": password})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@get('/join_group/<password>')
def join_group_handler(password=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for i in c.execute('''SELECT id FROM groups WHERE password = ? ''', (password, )):
        group_id = i[0]

    c.execute('''insert into users(group_id) VALUES (?)''', (group_id ,))
    user_id = c.lastrowid

    # number_of_people = c.execute('''SELECT count(*) FROM users WHERE group_id=? ''', (group_id, )).fetchone()[0]
    c.execute('''UPDATE groups SET number_of_people = (number_of_people + 1) WHERE id = ?''', (group_id, ))

    conn.commit()
    conn.close()

    body = json.dumps({"user_id": user_id, "group_id": group_id})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@post('/create_question/<group_id>')
def create_question(group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO state_groups(group_id, flag) VALUES (?, ?)''', (group_id, FLAG_QUESTION))
    state_group_id = c.lastrowid
    c.execute('''INSERT INTO question_groups(id) VALUES (?)''', (state_group_id, ))

    number_of_people = c.execute('''SELECT count(*) FROM users WHERE group_id=? ''', (group_id, )).fetchone()[0]
    c.execute('''UPDATE groups SET number_of_people = ? WHERE id = ?''', (number_of_people, group_id))

    conn.commit()
    conn.close()

    body = json.dumps({"question_group_id": state_group_id})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@post('/create_coming_out/<group_id>')
def create_coming_out(group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO state_groups(group_id, flag) VALUES (?, ?)''', (group_id, FLAG_COMING_OUT))
    state_group_id = c.lastrowid
    c.execute('''INSERT INTO coming_out_groups(id) VALUES (?)''', (state_group_id, ))

    number_of_people = c.execute('''SELECT count(*) FROM users WHERE group_id=? ''', (group_id, )).fetchone()[0]
    c.execute('''UPDATE groups SET number_of_people = ? WHERE id = ?''', (number_of_people, group_id))

    conn.commit()
    conn.close()

    body = json.dumps({"coming_out_group_id": state_group_id})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@post('/create_none/<group_id>')
def create_none(group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO state_groups(group_id, flag) VALUES (?, ?)''', (group_id, FLAG_NONE))

    conn.commit()
    conn.close()

    res = HTTPResponse(status=200, body='')
    return res


@get('/state_group/latest/<group_id>')
def state_group_latest_group_id_handler(group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # _list = None

    for i in c.execute('''SELECT id, flag FROM state_groups WHERE group_id=?''', (group_id, )):
        _list = i

    if _list == None:
        body = json.dumps({"id": None, "flag": None})
        # 一時的にstatusを400に
        res = HTTPResponse(status=400, body=body)
        res.set_header('Content-Type', 'application/json')
        return res

    body = json.dumps({"id": _list[0], "flag": _list[1]})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@get('/state_group/input/<group_id>/<state_group_id>')
def get_state_group_id(group_id='', state_group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    _flag = c.execute('''SELECT flag FROM state_groups WHERE id=?''', (state_group_id, )).fetchone()[0]

    if _flag == FLAG_QUESTION:
        _now = c.execute('''SELECT count(*) FROM state_groups INNER JOIN questions on state_groups.id = questions.question_group_id''').fetchone()[0]
        _all = c.execute('''SELECT number_of_people FROM groups WHERE id=?''', (group_id, )).fetchone()[0]
        if _now >= _all:
            body = json.dumps({"boolean": 1})
        else:
            body = json.dumps({"boolean": 0})
        return HTTPResponse(status=200, body=body)
    elif _flag == FLAG_COMING_OUT:
        _now = c.execute('''SELECT count(*) FROM state_groups INNER JOIN coming_outs on state_groups.id = coming_outs.coming_out_group_id''').fetchone()[0]
        _all = c.execute('''SELECT number_of_people FROM groups WHERE id=?''', (group_id, )).fetchone()[0]
        if _now >= _all:
            body = json.dumps({"boolean": 1})
        else:
            body = json.dumps({"boolean": 0})
        return HTTPResponse(status=200, body=body)
    else:
        res = HTTPResponse(status=200, body='')
        return res


@get('/question/<question_group_id>')
def return_question_list_handler(question_group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''SELECT text FROM questions WHERE question_group_id=?''', (question_group_id ,))

    body = json.dumps({"question_texts": c.fetchall()})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@post('/question/<state_group_id>/<user_id>')
def add_question_handler(state_group_id='', user_id=''):
    question_text = request.params.get('question_text')

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO questions(question_group_id, user_id, text) VALUES (?, ?, ?)''', (state_group_id, user_id, question_text))

    conn.commit()
    conn.close()

    res = HTTPResponse(status=200, body='')
    return res


@get('/coming_out/<coming_out_group_id>')
def return_coming_out_list_handler(coming_out_group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''SELECT text FROM coming_outs WHERE coming_out_group_id=?''', (coming_out_group_id ,))

    body = json.dumps({"coming_out_texts": c.fetchall()})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@post('/coming_out/<state_group_id>/<user_id>')
def add_coming_out_handler(state_group_id='', user_id=''):
    coming_out_text = request.params.get('coming_out_text')

    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO coming_outs(coming_out_group_id, user_id, text) VALUES (?, ?, ?)''', (state_group_id, user_id, coming_out_text))

    conn.commit()
    conn.close()

    res = HTTPResponse(status=200, body='')
    return res


@get('/group/users/<group_id>')
def return_number_of_people(group_id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    number_of_people = c.execute('''SELECT number_of_people FROM groups WHERE id=?''', (group_id, )).fetchone()[0]

    return HTTPResponse(status=200, body=json.dumps({"number_of_people": number_of_people}))



#####
# そのユーザがgroupに含まれているか確認して、含まれていたらquestion_group_idを使ってquestionテーブルに追加する


run(host=hostname, port=port)
