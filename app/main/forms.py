from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a nickname and a room."""
    user_name = StringField('用户名', validators=[Required()])
    nickname = StringField('姓名', validators=[Required()])
    room = StringField('聊天室', validators=[Required()])
    submit = SubmitField('输入聊天室名字')
