import os
import uuid
import shutil

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent import pywsgi
import cv2 as cv
from src.generate import Img, save_image
from src.generate_update import SystemConfiguration, setSystemConfiguration, imageInputReconst, imageInputEmbed
from time import sleep

# 文件工作路径
original_address = "D:/2023-2-6/flask/Digital_Watermark_Embedding_And_Tampering_Repair_System"  # 当前项目根路径
cache_address = ""  # 当前项目缓存路径（用于保存临时的文件）
pending_image_address = ""  # 待处理图片路径（广义下的原图）
embeded_image_address = ""  # 嵌入水印图片路径
certification_image_address = ""  # 篡改认证图片路径
origin_identified_image_address = ""  # 原图标识篡改区域图片路径
restore_image_address = ""  # 恢复图片路径

#修复图片
def RestorePicture(target_image_address):
    # 将待处理图片复制一份进缓存区
    shutil.copyfile(target_image_address, pending_image_address)

    # 执行图像的篡改区域认证
    imageInputReconst(pending_image_address, restore_image_address)

    # 给出结束提示
    print("完成图像的修复！")
    sleep(3)

    # 返回修复后的图像绝对路径
    return jsonify(restore_image_address.split('/')[-1])

#区域检测
def AreaDetection(target_image_address):  # !!!绝对路径
    # 将待处理图片复制一份进缓存区
    shutil.copyfile(target_image_address, pending_image_address)

    # 执行图像的篡改区域认证
    imageInputReconst(pending_image_address, restore_image_address)

    # 给出结束提示
    print("完成图像的篡改区域认证！")

    sleep(3)
    # 返回篡改区域认证图像绝对路径
    return jsonify([certification_image_address.split('/')[-1], origin_identified_image_address.split('/')[-1]])

#嵌入水印
def EmbedWatermark(target_image_address):  # !!!绝对路径
    # 将待处理图片复制一份进缓存区
    shutil.copyfile(target_image_address, pending_image_address)

    # 执行水印自嵌入
    imageInputEmbed(pending_image_address, embeded_image_address)

    # 给出结束提示
    print("完成图像水印自嵌入！")

    # 返回嵌入水印后的图像绝对路径
    return jsonify(embeded_image_address.split('/')[-1])

#添加图片
def addpicture(picturetype):
    # 获取图片文件 name = upload
    img = request.files.get('file')

    # 定义一个图片存放的位置 存放在static下面
    path = ""
    if(picturetype=="原图"):
        path="D:/2023-2-6/image/original/"
    if (picturetype == "水印"):
        path = "D:/2023-2-6/image/watermark/"
    if (picturetype == "待认证恢复图片"):
        path = "D:/2023-2-6/image/tampered/"
    # 图片名称
    imgName = img.filename

    # 图片path和名称组成图片的保存路径
    file_path = path + imgName
    print("添加图片:"+file_path)
    # 保存图片
    img.save(file_path)
    return jsonify('success')

if __name__ == '__main__':
    # 系统初始配置（创建缓存目录）
    # original_address = str(os.getcwd())
    # original_address = original_address.replace('\\','/')

    cache_address = original_address + "/cache"
    # cache_folder = os.path.exists(cache_address)
    # if cache_folder:  # 删除缓存文件夹
    #     shutil.rmtree(cache_address)
    # os.mkdir(cache_address)

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

    # 本地执行业务功能
    # 嵌入水印
    embeded_image_address = EmbedWatermark(pending_image_address)

    # 本地确定目标检测文件
    pending_image_address = "D:/2023-2-6/flask/Digital_Watermark_Embedding_And_Tampering_Repair_System/image/tampered/Lena_changed.png"

    # 篡改区域认证
    certification_image_address, origin_identified_image_address = AreaDetection(pending_image_address)
    # 图像修复
    restore_image_address = RestorePicture(pending_image_address)
