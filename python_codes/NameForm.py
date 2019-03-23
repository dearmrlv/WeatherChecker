from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
#创建一个表单类，用于接收数据
class NameForm(FlaskForm):      #继承了FlaskForm表单类
    name = StringField('Please enter a city in English:', validators=[DataRequired()])  #设置文本输入框的文字提示，以及在用户输入为空时提示用户应当输入数据
    submit = SubmitField('Submit')  #提交按钮上的文字
