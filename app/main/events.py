# -*- coding:utf-8 -*-
from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import uuid
import json
import collections


class Room():
    #在线用户
    onlineUsers = {}
    #当前在线人数
    onlineCount = 0

Rooms = {}


def create_new_useritem(uid,username):
    '''建立一个新用户的各个字段'''
    item = {}
    item['uid'] = uid
    item['username'] = username
    if uid == 0:
        item['is_adimin'] = True    
    else:
        item['is_adimin'] = False

    item['is_emphasized'] = False
    item['is_silenced'] = False
    return item


def add_fake_useritems(room):
    '''建立几个假用户用来开发uselist功能'''
    item = create_new_useritem(uid=1,username='张三')
    Rooms[room].onlineUsers[1] = item
    item = create_new_useritem(uid=2,username='李四')
    Rooms[room].onlineUsers[2] = item



#@socketio.on('connect')
@socketio.on('connect',namespace='/chat')
def test_connect():
    print('连接')
    #session['connect'] = '哈哈哈'

@socketio.on('disconnect',namespace='/chat')
def test_disconnect():
    print('断开连接')
    username = session['username']
    room = session['room']
    uid = session['uid']

    user = {'username':username,'room':room,'uid':uid}

    if uid in Rooms[room].onlineUsers:
        Rooms[room].onlineUsers.pop(uid)
        Rooms[room].onlineCount = len(Rooms[room].onlineUsers)


        msg = {'onlineUsers':Rooms[room].onlineUsers, 
            'onlineCount':Rooms[room].onlineCount,
            'user':user}
        leave_room(room)
        emit('logout', json.dumps(msg, ensure_ascii = False), room=room)    
        print('用户： {0} 离开了房间：{1}'.format(username,room))



@socketio.on('message_login',namespace='/chat')
def handle_login(user):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    print(user)
    #user = json.loads(user)
    #print(user)

    print(user['username']+' 登录 房间=' + user['room'])
    #print(message)
    room = user['room']
    uid = user['userid']
    username = user['username']
    session['room'] = room
    session['uid'] = uid
    session['username'] = username
    #print(session)



    if room  not in Rooms:
        Rooms[room] = Room()

    if uid not in Rooms[room].onlineUsers:
        item = create_new_useritem(uid,username)
        Rooms[room].onlineUsers[uid] = item

        add_fake_useritems(room) # 调试userlist用的


        Rooms[room].onlineCount = len(Rooms[room].onlineUsers)
        join_room(room)
        #print(Rooms[room].onlineUsers)
        msg = {'onlineUsers':Rooms[room].onlineUsers, 
            'onlineCount':Rooms[room].onlineCount,
            'user':user}

        emit('login', json.dumps(msg, ensure_ascii = False), room=room)

    


@socketio.on('message_txt', namespace='/chat')
def message(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    #print('收到消息')
    #print(session)
    print(Rooms)
    emit('message_txt', message, room=room)
    print(message['username']+'说：'+message['content']);


def output():
    with open('./1.wav','wb') as f:
        f.write("haha")

@socketio.on('message_wav', namespace='/chat')
def message(bit_mp3):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    print('收到语音消息')
    #print(session)
    #print(message)
    with open('./' + str(uuid.uuid1()) + '.wav','wb') as f:
        print('写文件')
        f.write(message)
    #output()
    #print(message['content'])

    emit('message_wav', message, room=room)
    print(message['username']+'说: (语音)');

@socketio.on('message_mp3', namespace='/chat')
def message(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    print('收到mp3语音消息')
    #print(session)
    #print(message)
    mp3_name = str(uuid.uuid1())
    with open('./' + mp3_name + '.mp3','wb') as f:
    # #with open('./' + '1.mp3','wb') as f:
         print('写文件')
         f.write(message['content'])
    message['mp3_name'] = mp3_name
    emit('message_audio', message, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)

