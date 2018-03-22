from flask import Flask
# WSGI：Web Server Gateway Interface。
# WSGI接口定义非常简单，它只要求Web开发者实现一个函数，就可以响应HTTP请求

# 传入__name__是为了用这个参数决定根目录，以便于以后能够找到相对于程序根目录的资源文件位置
app = Flask(__name__)


# 以下把index函数注册为程序根地址的处理函数，也就是说如果 服务器的域名地址是 www.example.com，那么在浏览器中访问
# http://www.example.com后，会出发服务器执行index函数
@app.route('/')
def index():
    return '<h1>hello world</h1>'


# url中的可变部分对应在代码中的处理如下：http://www.facebook.com/<your-name>,用户名是地址的一部分
# 路由中的动态部分默认使用字符串，不过也可使用类型定义，如：/user/<int:id>,Flask支持int，float 和path 但默认是字符串类型
# path 类型也是字符串，但是不把斜线视作分隔符，而当作动态片段的一部分。
@app.route('/user/<name>')  # <>中内容就是可变部分，调用这个函数时，Flask会将动态的参数传入函数
def user(name):
    return '<h1>hello， %s </h1>' % name


# 404 不存在的网址
#

# 启动服务器
if __name__ == '__main__':
    # debug 参数控制服务器以调试模式启动
    app.run(debug=True)