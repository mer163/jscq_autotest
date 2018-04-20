from flask import Flask,jsonify,make_response,abort,redirect,render_template
from . import power
import requests
import logging

logging.basicConfig(filename='monitor.log',format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
logger = logging.getLogger('manage')

@power.route('/', methods=['GET','POST'])
def index():

    return render_template('power.html', form=None, posts=None,
                           show_followed=None, pagination=None)


@power.route('/battery_level/<ip>',methods=['GET','POST'])
def battery_level(ip):

    try:
        logger.info('请求url=' + 'http://' + ip + ':7912/info')
        r = requests.get('http://' + ip + ':7912/info',timeout=3)\

    except requests.exceptions.ConnectTimeout:
        logger.info('连接超时')
        return ''
    except requests.exceptions.ConnectionError:
        logger.info("连接失败")
        return ''
    except ValueError:
        logger.info('json解析异常')
        return '0'

    return str(r.josn().get('battery').get('level'))