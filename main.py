import sys
import sqlite3
import json
from random import randint

from bottle import run
from bottle import HTTPResponse
from bottle import request
from bottle import get
from bottle import post
from bottle import put
from bottle import delete


#=== settings ===
hostname = '127.0.0.1'
port = 8080
db_name = 'spajam.db'
FLAG_QUESTION = 'question'
FLAG_COMING_OUT = 'coming_out'
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

    conn.commit()
    conn.close()

    body = json.dumps({"coming_out_group_id": state_group_id})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@get('/state_group/latest/<group_id>')
def state_group_latest_group_id_handler(group_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    for i in c.execute('''SELECT id, flag FROM state_groups WHERE group_id=?''', (group_id, )):
        print(i)
        _list = i

    body = json.dumps({"id": _list[0], "flag": _list[1]})
    res = HTTPResponse(status=200, body=body)
    res.set_header('Content-Type', 'application/json')
    return res


@get('/question/<state_group_id>')
def return_question_list_handler(question_group_id=''):
    # conn = sqlite3.connect(db_name)
    # c = conn.cursor()
    #
    # c.execute('''select * from question_groups where id''', (question_group_id ,))
    #
    # body = json.dumps(c.fetchall())
    # res = HTTPResponse(status=200, body=body)
    # res.set_header('Content-Type', 'application/json')
    # return res
    return None


@post('/question/<state_group_id>/<user_id>')
def add_question_handler(state_group_id='', user_id=''):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''INSERT INTO ''')

    conn.commit()
    conn.close()

    res = HTTPResponse(status=200, body='')
    return res



    # そのユーザがgroupに含まれているか確認して、含まれていたらquestion_group_idを使ってquestionテーブルに追加する

    return None


# @route(api_v1, method='GET')
# def create_group():
#     # json処理
#     body = json.dumps({"name": "user", "id": "111"})
#     res = HTTPResponse(status=200, body=body)
#     res.set_header('Content-Type', 'application/json')
#     return res
#
# @route(api_v1)
# @route('create_group/<group_id>', method='POST')
# def index(group_id=None):
#     return 'ok'
#
# @route('/')
# def hoge():
#     return 'a'


# conn = sqlite3.connect('spajam.db')
# c = conn.cursor()
# c.execute()

#--- mongodb ---
# client = MongoClient()
# db = client.testdb
#--- end ---

# @route(api_dir + '/json', 'GET')
# def index():
#     body = json.dumps({"name": "user", "id": "111"})
#     res = HTTPResponse(status=200, body=body)
#     res.set_header('Content-Type', 'application/json')
#     return res

run(host=hostname, port=port)
