# -*- coding: utf-8 -*-
import json
import requests
from flask import jsonify, Flask, make_response, request
from flask_sqlalchemy import SQLAlchemy
from utils.common import *

debug_judge = True  # 调试打印开关
relay = True  # 如果在mock_server中没有数据是否进行转发， True为是
relay_host = 'http://127.0.0.1:5202'  # 转发服务器地址, 注意一定不能设置成和当前服务器地址一致，否则会造成死循环

app = Flask(__name__)
# 注意python3 的SQLAlchemy mysql的链接要加 +pymysql
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/simple-mock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


def check_json_format(raw_str):
    """
    用于判断一个字符串是否符合Json格式
    :param raw_str: 待判断的字符串
    :return:
    """
    if isinstance(raw_str, str):       # 首先判断变量是否为字符串
        try:
            json.loads(raw_str, encoding='utf-8')
        except ValueError:
            return False
        return True
    else:
        return False


class MockData(db.Model):
    """定义数据模型"""
    __tablename__ = 'mock_data'
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'mock_data'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))  # 项目名称
    test_page = db.Column(db.String(100))  # 测试名称
    test_point = db.Column(db.String(100))  # 测试点
    route_url = db.Column(db.String(50))  # 路由
    method = db.Column(db.String(5))  # 方法
    req_para = db.Column(db.String(200))  # req的参数（主要是get请求）字典方式保存
    req_data = db.Column(db.String(200))  # req 对应的data（主要是post请求）字典方式保存
    res_data = db.Column(db.String(5000))  # 保存返回的数据
    test_detail_des = db.Column(db.String(500))  # 测试详细描述
    current_active = db.Column(db.Integer)  # 当前是否激活0未激活，1激活
    update_time = db.Column(db.TIMESTAMP)  # 保存更新时间


# 在错误处理中，处理所有路由请求，并返回正确结果
@app.errorhandler(404)
def not_found(error):

    req_para = list(request.args.items())  # 获取的是类似这种格式的para的键值对[('title', 'test')],空则为[]
    if not req_para:
        req_para = None
    req_data = list(request.form.items())  # 获取的是类似这种格式的data的键值对[('title', 'test')],空则为[]
    if not req_data:
        req_data = None
    req_path = request.path                # 获取的是当前的路由路径
    req_method = request.method.lower()    # 获取的是method方法
    req_url = request.url                  # 返回请求的链接
    req_host = request.host                # 当前host

    debug_print(debug_judge, "req_url", req_url)
    debug_print(debug_judge, "req_host", req_host)
    debug_print(debug_judge, "req_para", req_para)
    debug_print(debug_judge, "req_data", req_data)
    debug_print(debug_judge, "req_path", req_path)
    debug_print(debug_judge, "req_method", req_method)
    mock_data = MockData.query.filter_by(method=req_method, route_url=req_path[1:]).first()
    if mock_data:
        res_data = mock_data.res_data
        debug_print(debug_judge, "res_data", res_data)
        # 如果是json，打包成json数据
        if check_json_format(res_data):
            res_data_obj = json.loads(res_data)  # 把数据库中的json字符串加载成 python对象数据
            # json.dumps 和 jsonify的区别：https://blog.csdn.net/Duke_Huan_of_Qi/article/details/76064225
            res_data_jsonify = jsonify(res_data_obj)  # 把数据加载成json字符串格式，不能用json.dumps, 返回数据的Content-Type不一致
            return make_response(res_data_jsonify, 200)
        # 否则 直接返回数据
        else:
            return make_response(res_data, 200)

    elif relay:
        # 获取转发host链接
        debug_print(debug_judge, req_url, dict(req_data))
        relay_req_url = req_url.replace("http://" + req_host, relay_host)
        debug_print(debug_judge, "relay_req_url", relay_req_url)

        if req_method == "get":
            re = requests.get(relay_req_url, params=dict(req_para))
        else:
            re = requests.post(relay_req_url, params=dict(req_para), data=dict(req_data))
        return re
    else:
        return jsonify({"status": "fail", "msg": "没有查找到正确的mock数据，请检查rotue信息"})
    

@app.errorhandler(500)
def not_found(error):
    debug_print(debug_judge, error)
    return make_response(u"程序报错，可能是因为叙利亚战争导致", 500)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5201, threaded=True)
