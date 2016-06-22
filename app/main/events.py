from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
import uuid
import json

class Room():
    #在线用户
    onlineUsers = {}
    #当前在线人数
    onlineCount = 0

Rooms = {}



#@socketio.on('connect')
@socketio.on('connect',namespace='/chat')
def test_connect():
    print('连接')
    #session['connect'] = '哈哈哈'

@socketio.on('disconnect',namespace='/chat')
def test_disconnect():
    username = session['name']
    room = session['room']
    uid = session['uid']
    if uid in Rooms[room].onlineUsers:
        Rooms[room].onlineCount -= 1
        Rooms[room].onlineUsers.pop(uid)

    print('Client {0} disconnected'.format((username)))


#@socketio.on('login')
@socketio.on('login',namespace='/chat')
def handle_login(user):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""

    print(user['username']+' 登录 房间=' + user['room'])
    #print(message)

    session['room'] = user['room']
    session['uid'] = user['userid']
    session['name'] = user['username']
    #print(session)
    room = session.get('room')
    uid = session.get('uid')

    if room  not in Rooms:
        Rooms[room] = Room()

    if uid not in Rooms[room].onlineUsers:
        Rooms[room].onlineCount += 1
        Rooms[room].onlineUsers[uid] = session['name']

    join_room(room)
    #print(Rooms[room].onlineUsers)
    emit('login', {'onlineUsers':Rooms[room].onlineUsers, 'onlineCount':Rooms[room].onlineCount, 'user':user}, room=room)


    #print(message['room'])
    #print(message['userid'])
    


@socketio.on('message_txt', namespace='/chat')
def message(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    #print('收到消息')
    #print(session)
    #print(message)
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

