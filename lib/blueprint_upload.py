# -*- coding: utf-8 -*-
from flask import Blueprint, request
from lib.snow_id import *
import os
from lib.ini_info import upload_host

host_domain = upload_host()

upload = Blueprint('upload', __name__, url_prefix="/upload")


@upload.route('/', methods=['GET', 'POST', 'UPLOAD'])
def uploads__():
    try:
        worker = IdWorker(1, 4, 0)
        uid = worker.get_id()
        file_obj = request.files['file']
        if file_obj is None:
            return 9001
        filename = file_obj.filename.split('.')
        filename[0] = uid
        filenamet = str(filename[0]) + '.' + filename[1]
        file_type = str(file_obj.headers['Content-Type']).split('/')
        if 'video' in file_type:
            file_obj.save("static/video/" + filenamet)
        else:
            file_obj.save("static/" + filenamet)
        return [host_domain + filenamet]
    except Exception as a:
        return "文件上传失败"


# @upload.route('/del', methods=['GET', 'POST'])
# def del_uploads__():
#     url = "/static/1.jpg"
def del_uploads__(url):
    url_list = url.split('/')
    try:
        # 找到文件名
        for x in url_list:
            if x.find('.') != -1:
                # 删除他
                os.remove(os.getcwd() + "/static/" + x)
        return "文件删除成功"
    except Exception as e:
        return f"文件删除失败 ==> {e}"

    pass
