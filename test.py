"""
这个脚本是用来测试一些不清楚的特性（git test）
"""
from flask import jsonify, Flask, make_response, request
import sys, requests, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/simple-mock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


print(list({"a":123}.keys())[0], {"a":123}.values())


class mock_config(db.Model):
    """定义数据模型"""
    __tablename__ = 'mock_config'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    reqparams = db.Column(db.String(500))
    methods = db.Column(db.String(50))
    domain = db.Column(db.String(50))
    description = db.Column(db.String(50))
    resparams = db.Column(db.String(500))
    update_time = db.Column(db.TIMESTAMP)
    status = db.Column(db.Integer)
    ischeck = db.Column(db.Integer)
    project_name = db.Column(db.String(20))




def getvar(value):
    value = value[::-1]
    result = ''
    f = 0
    for i in range(len(value)):
        for j in range(len(value[i])):
            if f % 2 == 0:
                result = result + value[i][j] + '='
                f = f + 1
            else:
                result = result + value[i][j] + '&'
                f = f + 1
    return result[0:-1]
#
# xy = dict([('title', 'test'), ('name', 'vacon')])
# print(xy)

all_mock_datas = [{
                'id': 1,
                'project_name': '腾讯博物官',
                'test_name': '首页',
                'test_point': '获取首页推荐',
                'route_url': '/api/getHomeRecommendV2',
                'method': 'post',
                'req_para': 'req_para',
                'req_data': 'req_data',
                'res_data': '{"x":123,"y":456}',
                'test_detail_des': "test_detail_des",
                'current_active': '1',
                'update_time': '2018-08-22 18:58:19',
                'item_selected': False,
            }, {
                'id': 2,
                'project_name': '腾讯博物官',
                'test_name': '首页',
                'test_point': '获取首页推荐',
                'route_url': '/api/getHomeRecommendV2',
                'method': 'post',
                'req_para': 'req_para',
                'req_data': 'req_data',
                'res_data': '{"x":123,"y":456}',
                'test_detail_des': "test_detail_des",
                'current_active': '1',
                'update_time': '2018-08-22 18:58:19',
                'item_selected': False,
            }]
sorted_list = sorted(all_mock_datas, key=lambda x: x['id'], reverse=True)

print(sorted_list)

class testx(object):
    abc = 1
    efg = 2
    xyz = 3

xx = testx()

x = [1,2 ,3,4,5,6,7,8]
print(x[2:10])


