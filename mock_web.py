# 注意 vue-resource 不维护了，使用axios进行post请求，这块要补一下
from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import *
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy

save_path = 'D:\\'
ALLOWED_EXTENSIONS = ['xls', 'xlsx']

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@127.0.0.1:3306/simple-mock"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_ECHO']=True
db = SQLAlchemy(app)


class MockData(db.Model):
    """定义数据模型"""
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


def mock_data_list_to_dict_list(mock_data_list):
    """
    把mock_data list 转换为dict list
    :param mock_data_list: mock_data 列表
    :return:
    """
    mock_data_json_list = []
    for mock_data in mock_data_list:
        print("type-mock-data", mock_data)
        json_data = {'id': mock_data.id,
                     'project_name': mock_data.project_name,
                     'test_page': mock_data.test_page,
                     'test_point': mock_data.test_point,
                     'route_url': mock_data.route_url,
                     'method': mock_data.method,
                     'req_para': mock_data.req_para,
                     'req_data': mock_data.req_data,
                     'res_data': mock_data.res_data,
                     'test_detail_des': mock_data.test_detail_des,
                     'current_active': mock_data.current_active,
                     'update_time': mock_data.update_time,
                     'item_selected': False}
        print("json_data", json_data)
        mock_data_json_list.append(json_data)
    return mock_data_json_list


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    """
    获取首页数据
    :return: 返回首页数据
    """
    return render_template('index.html')


@app.route('/add_mock_data', methods=['POST'])
def edit_add_mock_data():
    """
    页面添加或修改数据使用本函数
    :return:
    """
    # 获取数据后解析成字典 obj 结构
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    print(json_data)
    db_in_data = json_data['add_edit_data']
    # 添加当前时间
    db_in_data['update_time'] = datetime.now()

    if 'id' in db_in_data:
        edit_id = db_in_data['id']
        try:
            print("--edit-mock-data, id: ", type(edit_id), edit_id)
            # 修改数据库内容，直接修改查询数据后，提交即可
            mock = MockData.query.filter_by(id=int(edit_id)).first()
            # 重置mock的所有属性值
            for key_tmp in db_in_data:
                setattr(mock, key_tmp, db_in_data[key_tmp])
            db.session.commit()
            print("edit-mock-data add: ", db_in_data)
        except :
            return jsonify({"reCode": -1, "msg": "添加失败"})
    else:
        db_in_data['id'] = None
        try:
            print("add new data: ", db_in_data)
            mock_data = MockData(**db_in_data)
            db.session.add(mock_data)
            db.session.commit()
        except:
            jsonify({"reCode": -1, "msg": "添加失败"})

    return jsonify({"reCode": 0, "msg": "添加成功"})


@app.route('/batch_edit', methods=['POST'])
def batch_edit_mock_data():
    """
    页面添加或修改数据使用本函数
    :return:
    """
    # 获取数据后解析成字典 obj 结构
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    print(json_data)

    db_in_data_list_id = json_data['batch_edit_id']
    db_in_data_list_key_value = json_data['batch_edit_key_value']

    key = list(db_in_data_list_key_value.keys())[0]
    value = list(db_in_data_list_key_value.values())[0]

    print("批量修改的数据是： ", db_in_data_list_key_value)
    print("批量修改的id是： ", db_in_data_list_id)

    for tmp_id in db_in_data_list_id:
        try:
            print("--edit-mock-data, id: ", type(tmp_id), tmp_id)
            print("edit-mock-data add: ", key, value)
            # 修改数据库内容，直接修改查询数据后，提交即可
            mock = MockData.query.filter_by(id=int(tmp_id)).first()
            # 重置mock的所有属性值
            setattr(mock, key, value)
            setattr(mock, 'update_time', datetime.now())
            db.session.commit()

        except :
            return jsonify({"reCode": -1, "msg": "批量修改失败"})

    return jsonify({"reCode": 0, "msg": "批量修改成功"})


@app.route('/del_mock_data', methods=['POST'])
def del_mock_data():
    """
    删除mock数据
    :return:
    """
    # 获取数据后解析成字典 obj 结构
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    print(json_data)
    db_in_data = json_data['del_data']
    try:
        for tmp_id in db_in_data:
            mock = MockData.query.filter_by(id=int(tmp_id)).first()
            db.session.delete(mock)
            db.session.commit()
    except:
        jsonify({"reCode": -1, "msg": "删除失败"})

    return jsonify({"reCode": 0, "msg": "删除成功"})


@app.route('/search', methods=['GET'])
def search():
    """
    搜索函数
    :return:
    """
    # 获取get数据
    req_para = list(request.args.items())
    print("--req_para", req_para)

    dict_para = dict(req_para)

    project_name = dict_para['project_name']
    test_page = dict_para['test_page']
    test_point = dict_para['test_point']
    page_item_max = int(dict_para['page_item_max'])
    page_index = int(dict_para['page_index'])

    mock = MockData.query.filter()
    mock_all = mock
    if project_name != "all":
        print("--", (project_name,))
        mock = mock.filter(MockData.project_name == project_name)
    if test_page != "all":
        mock = mock.filter(MockData.test_page == test_page)
    if test_point:
        mock = mock.filter(MockData.test_point.like('%' + test_point + '%'))  # 实现数据库模糊查询
    mock_filter_all = mock

    # 从全部数据中获取所有的项目名称和页面名称
    mock_data_all_list = mock_all.all()
    mock_data_all_json_list = mock_data_list_to_dict_list(mock_data_all_list)
    proj_name_list = list(set([tmp['project_name'] for tmp in mock_data_all_json_list]))
    test_page_list = list(set([tmp['test_page'] for tmp in mock_data_all_json_list]))

    # 获取过滤的json信息
    mock_data_filter_list = mock_filter_all.all()
    # 返回的数据进行json转换
    mock_data_filter_json_list = mock_data_list_to_dict_list(mock_data_filter_list)
    if len(mock_data_filter_json_list):
        sorted_json_list = sorted(mock_data_filter_json_list, key=lambda x: x['id'], reverse=True)
    else:
        sorted_json_list = []

    print("sorted_json_list", sorted_json_list)
    # 处理分页数据
    return_mock_data_list = sorted_json_list[(page_index - 1) * page_item_max: page_index * page_item_max]

    # 如果返回结果是0，那可能是删除最后一页的数据后，最后一页有没有了，比如 22条数据，传递的page_index=2, 删除了后2条
    if not return_mock_data_list:
        return_mock_data_list = sorted_json_list[(page_index - 2) * page_item_max: (page_index-1) * page_item_max]

    return_data = {
        "proj_names": proj_name_list,
        "test_pages": test_page_list,
        "total_page": int((len(sorted_json_list) - 1)/page_item_max) + 1,
        "page_mock_datas": return_mock_data_list
    }

    print("return_data: ", return_data)
    return jsonify(return_data)


@app.route('/upload_file', methods=['POST'])
def upload_file():
    """
    用于上传文件的处理函数
    :return:
    """
    file = request.files['userfile']
    filename = file.filename
    print("filename", filename)

    file.save(save_path + filename)

    # 判断文件名是否合规
    # if file and allowed_file(filename):
    #     file.save(save_path + filename)
    #     excelName = save_path + filename
    #     bk = xlrd.open_workbook(excelName, encoding_override="utf-8")
    #     sh = bk.sheets()[0]  # 因为Excel里只有sheet1有数据，如果都有可以使用注释掉的语句
    #     nrows = sh.nrows  # 行
    #     for j in range(1, nrows):
    #         if j + 1 == nrows:
    #             return jsonify({'msg': "ok", "remark": "上传成功"})
    #         else:
    #             lvalues = sh.row_values(j + 1)
    #             if lvalues[6] == '是':
    #                 ischeckr = 0
    #             elif lvalues[6] == '否':
    #                 ischeckr = 1
    #             else:
    #                 ischeckr = 1
    #             try:
    #                 mock = mock_config(id=None, title=lvalues[0], reqparams=lvalues[4], methods=lvalues[3],
    #                                    domain=lvalues[2],
    #                                    description=lvalues[7], resparams=lvalues[5], update_time=datetime.now(),
    #                                    status=0, ischeck=ischeckr, project_name=lvalues[1])
    #                 db.session.add(mock)
    #                 db.session.commit()
    #             except:
    #                 return jsonify({'msg': "fail", "remark": "解析失败"})
    #     return jsonify({'msg': "ok", "remark": "上传成功"})
    # else:
    #     return jsonify({'msg': "fail", "remark": "上传文件不符合格式要求"})
    print("上传成功")
    return jsonify({'msg': "fail", "remark": "上传文件不符合格式要求"})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'msg': 'fail', 'error': '404 Not found'}), 404)


@app.errorhandler(500)
def not_found(error):
    return make_response("程序报错，可能是因为叙利亚战争导致", 500)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, threaded=True, port=5202)
