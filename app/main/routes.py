from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm


#@main.route('/', methods=['GET', 'POST'])
@main.route('/django', methods=['GET', 'POST'])
def index():
    """"Login form to enter a room."""
    print('哈哈 index')
    return render_template('index.html')



@main.route('/', methods=['GET', 'POST'])
#@main.route('/django', methods=['GET', 'POST'])
def index_django():
    """"Login form to enter a room."""
    #form = LoginForm()
    # if form.validate_on_submit():
    #     session['name'] = form.name.data
    #     session['room'] = form.room.data
    #     return redirect(url_for('.chat'))
    print('哈哈 django')
    if request.method == 'POST':
        user = { 'username': request.form['username'],
                'nickname' : request.form['nickname'],
                'uid' : request.form['uid'],
                'room' : request.form['room'],
                }
    else:
        user = { 'username': '临时用户',
                'nickname' : '临时用户',
                'uid' : 0,
                'room' : '临时房间',
                }

    return render_template('index_django.html',user = user)


# @main.route('/chat')
# def chat():
#     """Chat room. The user's name and room must be stored in
#     the session."""
#     name = session.get('name', '')
#     room = session.get('room', '')
#     if name == '' or room == '':
#         return redirect(url_for('.index'))
#     return render_template('chat.html', name=name, room=room)
