# simple_mock
# sql文件为mysql中表结构文件
# mock_server.py为实际mock文件。
# mock_web.py为web管理页面所用server。
# mock文件夹中为管理页面,在indexJQ.js文件中配置mock_web.py访问地址。

## 操作步骤简述：
# 1、执行sql脚本建表
# 2、修改db.config数据库配置文件
# 3、安装需要的第三方依赖库，运行mock_server.py。
# 4、运行mock_web.py。
# 5、把web项目拷贝到web容器中正常访问，修改mock/js/config.js接口访问地址为mock_web的地址和端口。
# 6、打开index页，添加/导入自己需要的mock数据。



# 小程序的请求分为：所以，只需要过滤这几类请求即可
# a     get     req: url + 参数, url
# b     post    req: url + data


问题1：什么方式组织测试比较好呢？
理想状况是：
get情况   路由 + 参数  ： 对应一个响应
get情况   路由        ： 对应一个响应
post情况  路由 + data ： 对应一个响应
所以，后台只要保存好对应的这些参数值映射即可，所以数据库的组织形式

相同测试点可能同时有多条数据，每次只有一条数据是有效的
项目名称    测试名称    测试点    路由url   方法（get/post）    para参数       data域    返回数据    测试详细描述       是否有效  更新时间（标准时间）
博物官     首页测试    首页类型a  路由       get              none           none     data-a     测试a类型数据      是       xx
博物官     首页测试    首页类型b  路由       get              none           none     data-b     测试b类型数据      否       xx
...



问题2：路由url的形式多种多样，怎么可以统一处理路由呢？
每个路由对应处理函数，要想统一收口路由，有个办法，不设计所有其他路由函数，只处理404错误路由，但是返回想要的结果

