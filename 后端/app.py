from datetime import *
import os
import random
import uuid
import shutil
from urllib.parse import quote

import numpy as np
from flask import Flask, jsonify, request, make_response, send_file
from flask_cors import CORS, cross_origin
from gevent import pywsgi
import cv2 as cv
from src.generate import Img, save_image
from src.generate_update import SystemConfiguration, setSystemConfiguration, imageInputReconst, imageInputEmbed
from time import sleep

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# 文件工作路径
original_address = "D:"  # 当前项目根路径
cache_address = ""  # 当前项目缓存路径（用于保存临时的文件）
pending_image_address = ""  # 待处理图片路径（广义下的原图）
embeded_image_address = ""  # 嵌入水印图片路径
certification_image_address = ""  # 篡改认证图片路径
origin_identified_image_address = ""  # 原图标识篡改区域图片路径
restore_image_address = ""  # 恢复图片路径


# 嵌入水印
@app.route('/EmbedWatermark', methods=['post'])
def EmbedWatermark():
    print("执行“嵌入水印”业务功能！")
    file_obj = request.files['file']  # Flask中获取文件
    # 读取文件名及文件类型并转化成新的唯一的目标文件名
    fname, fextension = os.path.splitext(str(file_obj.filename))
    targetFile = str(fname.encode('unicode-escape').decode().replace('\\u', '') + getRandomList() + fextension)

    # 检验是否成功收到图片，有则将收到的图片保存进缓存区
    if file_obj is None:
        # 表示没有发送文件
        return "未上传文件"
    else:
        update_save_file = pending_image_address.replace('.png', fextension)
        file_obj.save(update_save_file)

    # 执行水印自嵌入
    imageInputEmbed(update_save_file, cache_address + "/" + targetFile)

    # 给出结束提示
    print("完成图像水印自嵌入！")
    return targetFile


# 区域检测
@app.route('/AreaDetection', methods=['post'])
def AreaDetection():
    print("执行“区域检测”业务功能！")
    file_obj = request.files['file']  # Flask中获取文件
    # 读取文件名及文件类型并转化成新的唯一的目标文件名
    fname, fextension = os.path.splitext(str(file_obj.filename))
    targetFile1 = str(fname.encode('unicode-escape').decode().replace('\\u', '') + getRandomList() + fextension)
    targetFile2 = str(fname.encode('unicode-escape').decode().replace('\\u', '') + getRandomList() + fextension)
    # 防止两个图片文件名重复
    while targetFile1 == targetFile2:
        targetFile2 = str(fname.encode('unicode-escape').decode().replace('\\u', '') + getRandomList() + fextension)

    # 检验是否成功收到图片，有则将收到的图片保存进缓存区
    if file_obj is None:
        # 表示没有发送文件
        return "未上传文件"
    else:
        update_save_file = pending_image_address.replace('.png', fextension)
        file_obj.save(update_save_file)

    # 执行图像的篡改区域认证
    imageInputReconst(update_save_file, cache_address + '/' + targetFile1, cache_address + '/' + targetFile2, None)

    # 给出结束提示
    print("完成图像的篡改区域认证！")

    # 返回篡改区域认证图像绝对路径
    return jsonify([targetFile1, targetFile2])


# 修复图片
@app.route('/RestorePicture', methods=['post'])
def RestorePicture():
    print("执行“修复图片”业务功能！")
    file_obj = request.files['file']  # Flask中获取文件
    # 读取文件名及文件类型并转化成新的唯一的目标文件名
    fname, fextension = os.path.splitext(str(file_obj.filename))
    targetFile = str(fname.encode('unicode-escape').decode().replace('\\u', '') + getRandomList() + fextension)

    # 检验是否成功收到图片，有则将收到的图片保存进缓存区
    if file_obj is None:
        # 表示没有发送文件
        return "未上传文件"
    else:
        update_save_file = pending_image_address.replace('.png', fextension)
        file_obj.save(update_save_file)

    # 执行图像的篡改区域认证
    imageInputReconst(update_save_file, None, None, cache_address + '/' + targetFile)

    # 给出结束提示
    print("完成图像的修复！")

    sleep(3)
    # 返回修复后的图像绝对路径
    return jsonify(targetFile)


# 取得图片
@app.route('/getTargetImage', methods=['GET'])
def getTargetImage():
    print("执行“取得图片”业务功能！")
    imgID = request.args["image_file"]
    if imgID == None:
        print("图片不存在!")
        return None

    # 读取文件名及文件类型
    fname, fextension = os.path.splitext(str(imgID))

    image_data = open(cache_address + '/' + imgID, "rb").read()
    response = make_response(image_data)
    response.headers['Content-Type'] = fextension  # 返回的内容类型必须修改
    return response


# 生成随机序列
def getRandomList():
    nowTime = datetime.now().strftime("%Y%m%d%H%M%S")  # 生成当前的时间
    randomNum = random.randint(0, 100)  # 生成随机数n,其中0<=n<=100
    if randomNum <= 10:
        randomNum = str(0) + str(randomNum)
    uniqueNum = str(nowTime) + str(randomNum)
    return str(uniqueNum)


# 添加图片
@app.route('/addpicture/<picturetype>', methods=['GET', 'POST'])
def addpicture(picturetype):
    # 获取图片文件 name = upload
    img = request.files.get('file')

    # 定义一个图片存放的位置 存放在static下面
    path = ""
    if (picturetype == "原图"):
        path = "D:/2023-2-6/image/original/"
    if (picturetype == "水印"):
        path = "D:/2023-2-6/image/watermark/"
    if (picturetype == "待认证恢复图片"):
        path = "D:/2023-2-6/image/tampered/"
    # 图片名称
    imgName = img.filename

    # 图片path和名称组成图片的保存路径
    file_path = path + imgName
    print("添加图片:" + file_path)
    # 保存图片
    img.save(file_path)
    return jsonify('success')


if __name__ == '__main__':
    # 系统初始配置（创建缓存目录）
    original_address = str(os.getcwd())
    original_address = original_address.replace('\\','/')

    cache_address = original_address + "/cache"
    cache_folder = os.path.exists(cache_address)
    if cache_folder:  # 删除缓存文件夹
        shutil.rmtree(cache_address)
    os.mkdir(cache_address)

    # 系统初始配置（初始化参数）
    pending_image_address = cache_address + "/pending_image.png"  # 待处理图片路径（广义下的原图）
    embeded_image_address = cache_address + "/embeded_image.png"  # 嵌入水印图片路径
    certification_image_address = cache_address + "/certification_image.png"  # 篡改认证图片路径
    origin_identified_image_address = cache_address + "/identified_image.png"  # 原图篡改区域标识图片路径
    restore_image_address = cache_address + "/restore_image.png"  # 恢复图片路径

    # 更新配置
    configuration = SystemConfiguration()
    configuration.original_address = original_address
    configuration.cache_address = cache_address
    configuration.pending_image_address = pending_image_address
    configuration.embeded_image_address = embeded_image_address
    configuration.certification_image_address = certification_image_address
    configuration.origin_identified_image_address = origin_identified_image_address
    configuration.restore_image_address = restore_image_address
    setSystemConfiguration(configuration)

    print("服务器已启动！")
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()
