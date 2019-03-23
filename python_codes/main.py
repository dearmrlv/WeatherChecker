from flask import Flask, render_template, session, redirect, url_for, flash
#其中，render_template函数把Flask提供的Jinja2模板引擎集成到了应用中
from flask_bootstrap import Bootstrap
from flask_moment import Moment
import requests, json

#引用自定义的表单类
from NameForm import *

#API供应者建议以id形式查询API数据
def search_city_id(city_name, city_list):
    for i in range(len(city_list)):
        if city_name==city_list[i]['name']:
            return city_list[i]['id']
    #错误检测，如果库中没有这个城市，就返回错误提示
    return '~'

#我的api_key
api_keys = '30b6b9e0b059743330d37865526ca4a6'
#测试api_keys是否有效
#data = requests.post('http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID='+api_keys).json()
#print(data)


app = Flask(__name__)   #创建Flask实例，__name__为Flask类构造函数的必要指定参数
app.config['SECRET_KEY'] = 'hard to guess string'       
bootstrap = Bootstrap(app)      #初始化bootstrap拓展
moment = Moment(app)            #初始化moment拓展

#查询forecast信息
def get_info(city_name, city_list):
    api_keys = '30b6b9e0b059743330d37865526ca4a6'
    city_id = search_city_id(city_name, city_list)
    if city_id != '~':
        city_info = requests.post('http://api.openweathermap.org/data/2.5/forecast?id=' + str(city_id) + '&APPID='+api_keys).json()
        return city_info
    else:
        return '~'

#查询当前天气信息
def get_info_now(city_name, city_list):
    api_keys = '30b6b9e0b059743330d37865526ca4a6'
    city_id = search_city_id(city_name, city_list)
    if city_id != '~':
        city_info = requests.post('http://api.openweathermap.org/data/2.5/weather?id=' + str(city_id) + '&APPID='+api_keys).json()
        return city_info
    else:
        return '~'

#加载保存在本地的城市列表
def load_list(filename):
    f = open(filename, encoding='utf-8')
    city_list = json.load(f)
    return city_list

#将数据写入json文件以便JS调用
import os
def print2json(info):
    with open(os.getcwd() + "/static/js/tmp_data.json", "w") as f:
        json.dump(info, f)

#在下面的这个例子里，我使用了Jinja2模板
from datetime import datetime
#定义路由
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()   #创建表单类实例
    city_list = load_list('city.list.json')     #加载city_list以供查询
    if form.validate_on_submit():       #表单请求
        session['name'] = form.name.data
        INFO = get_info(session.get('name'), city_list)
        if INFO != '~': #请求有效时
            #print2json(info)
            INFO_NOW = get_info_now(session.get('name'), city_list)
            return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'), info=INFO, info_now=INFO_NOW)
        else:   #请求无效时返回合肥的天气
            INFO = get_info('Hefei', city_list)
            INFO_NOW = get_info_now('Hefei', city_list)
            #print2json(info)
            return render_template('index.html', current_time=datetime.utcnow(), form=form, name='Hefei', info=INFO, info_now=INFO_NOW)
    else:       #首次进入网页时显示合肥的天气
        INFO = get_info('Hefei', city_list)
        INFO_NOW = get_info_now('Hefei', city_list)
        #print2json(info)
        return render_template('index.html', current_time=datetime.utcnow(), form=form, name='Hefei', info=INFO, info_now=INFO_NOW)     #使用Jinja2渲染为html

#定义另一个路由
@app.route('/about/')
def about():
    return render_template('about.html')

#定义错误界面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
