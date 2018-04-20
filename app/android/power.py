from flask import Flask,jsonify,make_response,abort,redirect,render_template
from . import power
import requests

@power.route('/', methods=['GET','POST'])
def index():

    return render_template('power.html', form=None, posts=None,
                           show_followed=None, pagination=None)


@power.route('/battery_level/<ip>',methods=['GET','POST'])
def battery_level(ip):

    try:
        print('url=' + 'http://' + ip + ':7912/info')
        r = requests.get('http://' + ip + ':7912/info').json()
    except ValueError:
        print('json解析异常')
        return '0'

    return str(r.get('battery').get('level'))