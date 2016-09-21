#!/bin/env python
#coding=utf-8
import json
import commands,time
from flask import abort
from flask import Flask
from flask import request
 
app = Flask(__name__)
def authinfo(post_data):
    if not post_data.has_key('host'):
        return json.dumps("You need to provide host.")
    elif not post_data.has_key('user'):
        return json.dumps("You need to provide user.")
    elif not post_data.has_key('password'):
        return json.dumps("You need to provide password.")
    else:
        return 'pass'
# 查看sel time
@app.route('/ipmi/api001/seltime/select', methods=['POST'])
def index_seltime_get():
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    result = commands.getoutput("/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s sel time get" % (post_data["host"], post_data["user"], post_data["password"]))
    return json.dumps(result)
# 设置sel time
@app.route('/ipmi/api001/seltime/set/', methods=['POST'])
def index_seltime_set():
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    if not post_data.has_key('timestamp'):
        return json.dumps("You need to provide timestamp.")
    if not post_data["timestamp"].isdigit():
        return json.dumps("You need to provide timestamp.")
     
    x = time.localtime(int(post_data["timestamp"]))
    x = time.strftime('%m/%d/%Y %H:%M:%S',x)
    result = commands.getoutput("/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s sel time set '%s'" % (post_data["host"], post_data["user"], post_data["password"], x))
    return json.dumps(result)
# 设备管理
@app.route('/ipmi/api001/power/<action>', methods=['POST'])
def index_power(action):
    method_list = ["status", "off", "soft", "on", "reset"]
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    while action in method_list:
        commands_str = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s power %s" % (post_data["host"], post_data["user"], post_data["password"], action)
        result = commands.getoutput(commands_str)
        break
    else: result = "This method is not supported."
    return json.dumps(result)
# 启动项管理
@app.route('/ipmi/api001/bootdev/<option>', methods=['POST'])
def index_bootdev(option):
    start_list = ["pxe", "disk", "cdrom"]
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    while option in start_list:
        commands_str = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s chassis bootdev %s" % (post_data["host"], post_data["user"], post_data["password"], option)
        result = commands.getoutput(commands_str)
        break
    else:
        result = "This option is not supported."
    return json.dumps(result)
# 查看BMC的LAN信息
@app.route('/ipmi/api001/lanprint/<int:id>', methods=['POST'])
def index_lanprint(id):
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    commands_str = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s lan print %d" % (post_data["host"], post_data["user"], post_data["password"], id)
    result = commands.getoutput(commands_str)
    return json.dumps(result)
# 查看ipmi服务器端当前活动的session会话
@app.route('/ipmi/api001/ActiveSession', methods=['POST'])
def index_ActiveSession():
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    commands_str = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s session info active" % (post_data["host"], post_data["user"], post_data["password"])
    result = commands.getoutput(commands_str)
    return json.dumps(result)
# 查看BMC的信息
@app.route('/ipmi/api001/BMCInfo', methods=['POST'])
def index_BMCInfo():
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    commands_str = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s mc info" % (post_data["host"], post_data["user"], post_data["password"])
    result = commands.getoutput(commands_str)
    return json.dumps(result)
# 传感器SDR 列表信息
@app.route('/ipmi/api001/SDRList', methods=['POST'])
def index_SDRList():
    post_data = request.json
    return_info = authinfo(post_data)
    if return_info != "pass":
        return return_info
    commands_str = "/usr/bin/ipmitool -I lanplus -H %s -U %s -P %s sdr elist full" % (post_data["host"], post_data["user"], post_data["password"])
    result = commands.getoutput(commands_str)
    return json.dumps(result)
if __name__ =="__main__":
     
    app.run(debug=True, host='10.0.0.60', port=80)<p>&nbsp;</p>
