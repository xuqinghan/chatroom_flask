2016.5.25 发现这个奇葩bug
socketio必须安装eventlet 否则无法发送接收 Unicode字符，包括用户名


2016.2.15
server在Flask-SocketIO-Chat上修改而成：去掉验证用户身份部分


client用plhwin 的 客户端 改成flask模板 加入录音按钮 放在flask templates文件夹下。素材放在static文件夹下