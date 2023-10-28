import sys

import cv2
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow

np.set_printoptions(threshold=np.inf)


# 全局参数配置
class SystemConfiguration:
    def __init__(self):
        self.original_address = ""  # 当前项目根路径
        self.cache_address = ""  # 当前项目缓存路径（用于保存临时的文件）
        self.pending_image_address = ""  # 待处理图片路径（广义下的原图）
        self.embeded_image_address = ""  # 嵌入水印图片路径
        self.certification_image_address = ""  # 篡改认证图片路径
        self.origin_identified_image_address = ""  # 原图篡改区域标识图片路径
        self.restore_image_address = ""  # 恢复图片路径


configuration = SystemConfiguration()


def setSystemConfiguration(new_configuration):
    global configuration
    configuration = new_configuration


class Img(object):
    def __init__(self, data, part=False):
        # 原始图像数据(N, N, 3)
        self.data = data  # 单通道 N*N 像素值矩阵
        # 图像分块数据(N*N, 4, 4)
        self.data_ = Partition(self.data)  # 分块像素矩阵((N/4)*(N/4), 4, 4)
        # 密匙(质数)
        self.__kesei = 1003091
        # 一个较大的数(可以不为质数)，用于篡改认证
        self.__G = 33503

        # 像素矩阵各维度个数
        self.shape = data.shape

        self.b1 = None
        self.b2 = None
        self.Q1 = None
        self.Q2 = None
        if not part:
            # 计算块的均值
            self.mu = self.cal_mu()  # 计算4*4分块后的像素均值
            '''
                根据AMBTC算法计算得到图像的两个量化水平(M1, M2)和一个位图(b1)，用于生成水印和篡改修复
            '''
            self.b1 = self.cal_M1()
            self.Q1, self.Q2 = self.cal_Q()
            # 将两个量化水平转为16位二进制
            self.b2 = self.cal_M2()  # step3

            # 当前的M1和M2分别是表示

            # 对两个位图(b1, b2)进行置乱映射
            self.M1, self.M2 = self.Block_Mapping()
        else:
            self.Authentication_blocks = np.zeros(self.shape, dtype=np.uint8)

    def __len__(self):
        return len(self.data)

    def cal_mu(self):
        mu = np.zeros((self.data_.shape[0],), dtype=np.float64)
        for i in range(self.data_.shape[0]):
            mu[i] = np.mean(self.data_[i])

        return mu

    def cal_M1(self):
        b = np.zeros(self.data_.shape, dtype=np.uint8)

        for i in range(self.data_.shape[0]):
            for j in range(4):
                for k in range(4):
                    if self.data_[i, j, k] >= self.mu[i]:
                        b[i, j, k] = 1
                    else:
                        b[i, j, k] = 0

        return b

    def cal_M2(self):
        b = np.zeros(self.data_.shape, dtype=np.uint8)
        for i in range(self.data_.shape[0]):
            for j in range(8):
                t = self.Q1[i] // (1 << j) % 2
                b[i, j // 4, j % 4] = t
            for j in range(8):
                t = self.Q2[i] // (1 << j) % 2
                b[i, j // 4 + 2, j % 4] = t

        return b

    def cal_Q(self):
        Q1 = np.zeros((self.data_.shape[0],), dtype=np.int64)
        Q2 = np.zeros((self.data_.shape[0],), dtype=np.int64)
        for i in range(self.data_.shape[0]):
            sum1 = 0
            sum2 = 0
            t = 0
            for j in range(4):
                for k in range(4):
                    if self.b1[i, j, k] == 0:
                        t += 1
                        sum1 += self.data_[i, j, k]
                    else:
                        sum2 += self.data_[i, j, k]
            if t == 0:
                Q1[i] = 0
                Q2[i] = sum2 // 16
            elif t == 16:
                Q1[i] = sum1 // 16
                Q2[i] = 0
            else:
                Q1[i] = sum1 // t
                Q2[i] = sum2 // (16 - t)

        return Q1, Q2

    def Compress(self):
        new_data = np.zeros(self.data_.shape, dtype=np.uint8)
        for i in range(self.data_.shape[0]):
            for j in range(4):
                for k in range(4):
                    if self.b1[i, j, k] == 0:
                        new_data[i, j, k] = self.Q1[i]
                    else:
                        new_data[i, j, k] = self.Q2[i]

        return new_data

    # 生成映射序列，分块映射
    def Block_Mapping(self):
        B1 = Union(self.b1, self.shape)
        B2 = Union(self.b2, self.shape)

        M1 = Partition(B1, 64)
        M2 = Partition(B2, 64)

        mapping = np.zeros(M1.shape[0], dtype=np.int64)
        # generate [0,R) mapping sequence
        for i in range(M1.shape[0]):
            mapping[i] = (self.__kesei * (i + 1)) % M1.shape[0]

        for i in range(M1.shape[0]):
            M1[i], M1[mapping[i]] = M1[mapping[i]].copy(), M1[i].copy()

            M2[i], M2[mapping[i]] = M2[mapping[i]].copy(), M2[i].copy()

        return Union(M1, self.shape, 64), Union(M2, self.shape, 64)

    # 根据OPAP进行水印的嵌入
    def Embedding(self):  # 从低位起，第1、2位嵌入了M1,M2，第0位嵌入了检验和
        C = Partition(self.data, 4)
        M1 = Partition(self.M1, 4)
        M2 = Partition(self.M2, 4)

        N = C.shape[0]
        # 暂存LSB1
        B1 = np.zeros((N, 4, 4), dtype=np.uint8)

        for i in range(N):
            Pn = C[i].copy()
            Mn1 = M1[i].copy()
            Mn2 = M2[i].copy()

            # 取得图像原像素值后三位（低位）
            Pn_ = Pn // 2
            B1[i] = Pn % 2
            b2 = Pn_ % 2
            b3 = (Pn_ // 2) % 2

            for j in range(4):
                for k in range(4):
                    if b3[j, k] == 0 and b2[j, k] == 0 and Mn1[j, k] == 1:
                        Pn_[j, k] -= 1
                    elif b3[j, k] == 0 and b2[j, k] == 1 and Mn1[j, k] == 1:
                        Pn_[j, k] += 1
                    elif b3[j, k] == 1 and b2[j, k] == 0 and Mn1[j, k] == 0:
                        Pn_[j, k] -= 1
                    elif b3[j, k] == 1 and b2[j, k] == 1 and Mn1[j, k] == 0:
                        Pn_[j, k] += 1

            Pn__ = Pn_
            b2 = Pn__ % 2
            b3 = (Pn__ // 2) % 2

            for j in range(4):
                for k in range(4):
                    if b3[j, k] == 1 and b2[j, k] == 1 and Mn2[j, k] == 1:
                        Pn__[j, k] -= 1
                    elif b3[j, k] == 1 and b2[j, k] == 0 and Mn2[j, k] == 0:
                        Pn__[j, k] += 1
                    elif b3[j, k] == 0 and b2[j, k] == 1 and Mn2[j, k] == 0:
                        Pn__[j, k] -= 1
                    elif b3[j, k] == 0 and b2[j, k] == 0 and Mn2[j, k] == 1:
                        Pn__[j, k] += 1

            C[i] = Pn__ * 2 + B1[i]

        cn = np.arange(self.__G, self.__G + 16)
        Vsum = np.zeros((N,), dtype=np.int16)
        kn = np.zeros((N, 16), dtype=np.uint8)

        for i in range(N):
            Vsum[i] = np.sum(cn * C[i].reshape(-1)) % self.__G  # 灰度级数为什么取cn???
            for j in range(16):
                kn[i, j] = Vsum[i] // (1 << j) % 2

        for i in range(N):
            for j in range(4):
                for k in range(4):
                    if kn[i, j * 4 + k] != B1[i, j, k] and B1[i, j, k] == 0:
                        C[i, j, k] += 1
                    elif kn[i, j * 4 + k] != B1[i, j, k] and B1[i, j, k] == 1:
                        C[i, j, k] -= 1

        return C

    # 提取水印
    def Extracting(self):
        data_block = self.data_

        M1 = np.zeros((data_block.shape[0], 4, 4), dtype=np.uint8)
        M2 = np.zeros((data_block.shape[0], 4, 4), dtype=np.uint8)

        N = data_block.shape[0]

        for i in range(N):
            Pn = data_block[i]
            Pn_ = Pn // 2

            for j in range(4):
                for k in range(4):
                    M1[i, j, k] = Pn_[j, k] // 2 % 2
                    M2[i, j, k] = (Pn_[j, k] // 2 % 2) ^ (Pn_[j, k] % 2)

        M1 = Union(M1, self.shape, 4)
        M2 = Union(M2, self.shape, 4)

        M1 = Partition(M1, 64)
        M2 = Partition(M2, 64)

        mapping = np.zeros(M1.shape[0], dtype=np.int64)
        # generate [0,R) mapping sequence
        for i in range(M1.shape[0]):
            mapping[i] = (self.__kesei * (i + 1)) % M1.shape[0]

        for i in range(M1.shape[0] - 1, -1, -1):
            M1[i], M1[mapping[i]] = M1[mapping[i]].copy(), M1[i].copy()

            M2[i], M2[mapping[i]] = M2[mapping[i]].copy(), M2[i].copy()

        M1 = Union(M1, self.shape, 64)
        M2 = Union(M2, self.shape, 64)

        M1 = Partition(M1, 4)
        M2 = Partition(M2, 4)

        B = np.zeros(M1.shape, dtype=np.uint8)
        Q1 = np.zeros((M2.shape[0],), dtype=np.uint8)
        Q2 = np.zeros((M2.shape[0],), dtype=np.uint8)
        base = np.array([1, 2, 4, 8, 16, 32, 64, 128])

        NN = M2.shape[0]
        # [0,8) generater Q1, [8,16) generater Q2
        for i in range(NN):
            Q1[i] = np.matmul(base.T, M2[i, 0:2, 0:4].reshape(-1))
            Q2[i] = np.matmul(base.T, M2[i, 2:4, 0:4].reshape(-1))

        for i in range(NN):
            for j in range(4):
                for k in range(4):
                    if M1[i, j, k] == 0:
                        B[i, j, k] = Q1[i]
                    else:
                        B[i, j, k] = Q2[i]

        B = Union(B, self.shape)

        return B

    # 图像的篡改认证与重构
    def Authentication_Reconstruct(self):
        data_blocks = self.data_
        B = self.Extracting()
        B = Partition(B, 4)

        N = data_blocks.shape[0]
        row = self.shape[0] // 4

        cn = np.arange(self.__G, self.__G + 16)
        Vsum = np.zeros((N,), dtype=np.int16)
        R = np.zeros(self.data_.shape, dtype=np.uint8)

        for i in range(N):
            Pn = data_blocks[i]
            Bn = B[i]
            Psum = 0
            for j in range(4):
                for k in range(4):
                    Psum += (Pn[j, k] % 2) * (1 << (j * 4 + k))

            Vsum[i] = np.sum(cn * Pn.reshape(-1)) % self.__G

            if np.abs(Vsum[i] - Psum) <= 100:
                R[i] = Pn
            else:
                R[i] = Bn
                self.Authentication_blocks[i // row * 4:i // row * 4 + 4, (i % row) * 4:(i % row) * 4 + 4] = 255

        return R


# 图像分块(二维图像->三维分块)
# 原图像 N*N  => ((N*N)/(4*4),4,4)
def Partition(img, ratio=4, dtype=np.uint8):
    height, width = img.shape[:2]

    M = height // ratio
    N = width // ratio

    dst = np.zeros((M * N, ratio, ratio), dtype=dtype)

    for i in range(M):
        for j in range(N):
            y = int(ratio * i)
            x = int(ratio * j)
            patch = img[y:y + ratio, x:x + ratio]
            dst[i * M + j] = patch

    return dst


# 图像重构(三维分块->二维图像)
def Union(img, shape, radio=4):
    img_compress = np.zeros(shape, dtype=np.uint8)
    x = shape[1] // radio
    for i in range(img.shape[0]):
        yy = i // x
        xx = i % x
        img_compress[yy * radio:yy * radio + radio, xx * radio:xx * radio + radio] = img[i]

    return img_compress


# 保存重构图像
def save_image(img, shape, filename=None):
    img_compress = Union(img, shape)

    cv2.imwrite(filename, img_compress)


# 向目的地址图像中嵌入数字水印，返回Img对象
def embedWatermarkInImage(originImage):
    img = Img(originImage)
    new_img = img.Embedding()
    return new_img


# 读入图片(嵌入水印)
def imageInputEmbed(pending_image_address, processed_image_address, ):  # 待处理的图片路径、处理完成需要保存的文件路径
    img = np.array(cv2.imread(pending_image_address))

    # 使图像规范为 4x*4x 大小
    N = img.shape[0]
    if N % 4 != 0:
        x = N % 4
        img = img[:N-x, :N-x]

    flag = checkGray(img)

    if flag:
        imageBoundaryContraction(pending_image_address, "D:/img_update.png", False)
        img = np.array(cv2.imread("D:/img_update.png"))
        img_embed = Gray_Proc(img)
    else:
        imageBoundaryContraction(pending_image_address, "D:/img_update.png", True)
        img = np.array(cv2.imread("D:/img_update.png"))
        img_embed = RGB_Proc(img)

    cv2.imwrite(processed_image_address, img_embed)

    # cv2.imshow("embed_image", img_embed)
    # cv2.waitKey(0)


# 读入图片(重构图像)
def imageInputReconst(pending_image_address, certification_image_address, origin_identified_image_address, restore_image_address):  # 待处理的图片路径、篡改区域检测图、原图标识图、恢复后的图像文件路径
    img = np.array(cv2.imread(pending_image_address))
    flag = checkGray(img)
    if flag:
        authentication_blocks, identify_image, img_reconstruction = Gray_Proc(img, False)
    else:
        authentication_blocks, identify_image, img_reconstruction = RGB_Proc(img, False)

    # cv2.imshow("authentication_blocks", authentication_blocks)
    # cv2.imshow("origin_identify_image", identify_image)
    # cv2.imshow("img_reconstruction", img_reconstruction)
    # cv2.waitKey(0)
    if certification_image_address is not None:
        cv2.imwrite(certification_image_address, authentication_blocks)
    if origin_identified_image_address is not None:
        cv2.imwrite(origin_identified_image_address, identify_image)
    if restore_image_address is not None:
        cv2.imwrite(restore_image_address, img_reconstruction)


# 处理灰度图
def Gray_Proc(img, flag=True):
    if flag:
        # 如果是灰度图，那么三个通道的值是一样的，随便取一个进行计算
        img = Img(img[:, :, 0])
        new_img = img.Embedding()
        new_img = Union(new_img, img.shape)

        return new_img
    else:
        origin_img = img
        img = Img(img[:, :, 0], True)
        img_reconstruction = img.Authentication_Reconstruct()
        authentication_blocks = img.Authentication_blocks
        # cv.imshow("Authentication", img.Authentication_blocks)

        # 在原图上用白色线条标识被篡改区域
        identify_image = identifyTamperedAreas(origin_img[:, :, 0], img.Authentication_blocks, False)

        img_reconstruction = Union(img_reconstruction, img.shape)

        return authentication_blocks, identify_image, img_reconstruction


# 处理彩色图
def RGB_Proc(img, flag=True):
    if flag:
        # 如果是彩色图像，那么就在三个通道上分别进行水印的嵌入
        B, G, R = img[:, :, 0], img[:, :, 1], img[:, :, 2]  # 512 * 512

        img1, img2, img3 = Img(B), Img(G), Img(R)  # object
        new_img1, new_img2, new_img3 = img1.Embedding(), img2.Embedding(), img3.Embedding()
        new_img1, new_img2, new_img3 = Union(new_img1, img1.shape), Union(new_img2, img2.shape), Union(
            new_img3, img3.shape)
        # 合并三通道
        new_img = np.concatenate([np.expand_dims(new_img1, axis=-1), np.expand_dims(new_img2, axis=-1),
                                  np.expand_dims(new_img3, axis=-1)], axis=-1)

        # 测试变化
        BB = np.expand_dims(new_img1, axis=-1)[:, :, 0]
        GG = np.expand_dims(new_img2, axis=-1)[:, :, 0]
        RR = np.expand_dims(new_img3, axis=-1)[:, :, 0]

        return new_img
    else:

        B, G, R = img[:, :, 0], img[:, :, 1], img[:, :, 2]
        img1, img2, img3 = Img(B, True), Img(G, True), Img(R, True)
        img1_reconstruction, img2_reconstruction, img3_reconstruction = img1.Authentication_Reconstruct(), \
                                                                        img2.Authentication_Reconstruct(), \
                                                                        img3.Authentication_Reconstruct()
        authentication_blocks = img1.Authentication_blocks

        # 在原图上用红色线条标识被篡改区域
        identify_image = identifyTamperedAreas(img, img1.Authentication_blocks, True)

        img1_reconstruction, img2_reconstruction, img3_reconstruction = Union(img1_reconstruction, img1.shape), \
                                                                        Union(img2_reconstruction, img2.shape), \
                                                                        Union(img3_reconstruction, img3.shape)
        img_reconstruction = np.concatenate(
            [np.expand_dims(img1_reconstruction, axis=-1), np.expand_dims(img2_reconstruction, axis=-1),
             np.expand_dims(img3_reconstruction, axis=-1)], axis=-1)

        return authentication_blocks, identify_image, img_reconstruction


# 判断输入的图像是否为灰度图
def checkGray(chip):
    # chip_gray = cv2.cvtColor(chip,cv2.COLOR_BGR2GRAY)
    r, g, b = cv2.split(chip)
    r = r.astype(np.float32)
    g = g.astype(np.float32)
    b = b.astype(np.float32)
    s_w, s_h = r.shape[:2]
    x = (r + b + g) / 3

    area_s = s_w * s_h
    # x = chip_gray
    r_gray = abs(r - x)
    g_gray = abs(g - x)
    b_gray = abs(b - x)
    r_sum = np.sum(r_gray) / area_s
    g_sum = np.sum(g_gray) / area_s
    b_sum = np.sum(b_gray) / area_s
    gray_degree = (r_sum + g_sum + b_sum) / 3

    if gray_degree < 1:
        return True
    else:
        return False


# 使图片像素值调整至[4, 251]，参数分别为原图绝对路径、更新后保存的图片绝对路径、彩色图片标志（彩色图片为True，反之False）
def imageBoundaryContraction(origin_image_address, update_image_address, flag):
    if flag:
        image = cv2.imread(origin_image_address)
        b, g, r = cv2.split(image)
        for i in range(b.shape[0]):
            for j in range(b.shape[1]):
                # 三通道最小边界收缩
                if b[i][j] < 4:
                    b[i][j] = 4
                if g[i][j] < 4:
                    g[i][j] = 4
                if r[i][j] < 4:
                    r[i][j] = 4

                # 三通道最大边界收缩
                if b[i][j] > 251:
                    b[i][j] = 251
                if g[i][j] > 251:
                    g[i][j] = 251
                if r[i][j] > 251:
                    r[i][j] = 251

        new_image = cv2.merge([b, g, r])
        cv2.imwrite(update_image_address, new_image)
    else:
        img = np.array(cv2.imread(origin_image_address))
        new_image = img[:, :, 0]
        for i in range(new_image.shape[0]):
            for j in range(new_image.shape[1]):
                # 最小边界收缩
                if new_image[i][j] < 4:
                    new_image[i][j] = 4

                # 最大边界收缩
                if new_image[i][j] > 251:
                    new_image[i][j] = 251
        cv2.imwrite(update_image_address, new_image)


# 用线条在原图上标识被篡改区域（灰度图白色标识、RGB图红色标识），参数分别为原图像素数据（灰度[n,n],RGB[n,n,3]）、篡改图像认证（[n,n]）、彩色图片标志（彩色图片为True，反之False）
def identifyTamperedAreas(origin_image, authentication_blocks, flag):
    identified_image = origin_image

    cnt = 0
    if flag:  # 处理彩色图像
        for i in range(authentication_blocks.shape[0]):
            for j in range(authentication_blocks.shape[1]):
                if authentication_blocks[i][j] == 255:
                    cnt = cnt + 1
                    # 对篡改区域边缘进行标识
                    if i - 1 >= 0 and authentication_blocks[i - 1][j] != 255:  # 上
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i, j, 0] = 0  # B
                        identified_image[i, j, 1] = 0  # G
                        identified_image[i, j, 2] = 255  # R
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i - 1, j, 0] = 0  # B
                        identified_image[i - 1, j, 1] = 0  # G
                        identified_image[i - 1, j, 2] = 255  # R
                    if i + 1 < authentication_blocks.shape[0] and authentication_blocks[i + 1][j] != 255:  # 下
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i, j, 0] = 0  # B
                        identified_image[i, j, 1] = 0  # G
                        identified_image[i, j, 2] = 255  # R
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i + 1, j, 0] = 0  # B
                        identified_image[i + 1, j, 1] = 0  # G
                        identified_image[i + 1, j, 2] = 255  # R
                    if j - 1 >= 0 and authentication_blocks[i][j - 1] != 255:  # 左
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i, j, 0] = 0  # B
                        identified_image[i, j, 1] = 0  # G
                        identified_image[i, j, 2] = 255  # R
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i, j - 1, 0] = 0  # B
                        identified_image[i, j - 1, 1] = 0  # G
                        identified_image[i, j - 1, 2] = 255  # R
                    if j + 1 < authentication_blocks.shape[1] and authentication_blocks[i][j + 1] != 255:  # 右
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i, j, 0] = 0  # B
                        identified_image[i, j, 1] = 0  # G
                        identified_image[i, j, 2] = 255  # R
                        # 更新像素值，红色RGB值为[255, 0 ,0]
                        identified_image[i, j + 1, 0] = 0  # B
                        identified_image[i, j + 1, 1] = 0  # G
                        identified_image[i, j + 1, 2] = 255  # R
                    # # 对被篡改区域中心区域标识
                    # if authentication_blocks[i][j] == 255:
                    #     # 更新像素值，红色RGB值为[255, 0 ,0]
                    #     identified_image[i, j, 0] = 0  # B
                    #     identified_image[i, j, 1] = 0  # G
                    #     identified_image[i, j, 2] = 255  # R

    else:  # 处理灰色图像
        for i in range(authentication_blocks.shape[0]):
            for j in range(authentication_blocks.shape[1]):
                if authentication_blocks[i][j] == 255:
                    # 对篡改区域边缘进行标识
                    if i - 1 >= 0 and authentication_blocks[i - 1][j] != 255:  # 上
                        identified_image[i - 1, j] = 255
                        identified_image[i, j] = 255
                    if i + 1 < authentication_blocks.shape[0] and authentication_blocks[i + 1][j] != 255:  # 下
                        identified_image[i + 1, j] = 255
                        identified_image[i, j] = 255
                    if j - 1 >= 0 and authentication_blocks[i][j - 1] != 255:  # 左
                        identified_image[i, j - 1] = 255
                        identified_image[i, j] = 255
                    if j + 1 < authentication_blocks.shape[1] and authentication_blocks[i][j + 1] != 255:  # 右
                        identified_image[i, j + 1] = 255
                        identified_image[i, j] = 255

    radio = (cnt / (authentication_blocks.shape[0] * authentication_blocks.shape[1]))
    print("图像篡改比例为:" + str(radio))

    return identified_image


if __name__ == '__main__':

    # a = [1,2,3,4,5]
    # b = a // 2
    # print(b)



    # filename = '../image/original/lena.png'
    # save_address = "../image/embedded/lena_.png"
    # imageInputEmbed(filename, save_address)

    filename = '../image/tampered/boat_changed.png'
    save_address = "../image/restore/boat_restore.png"
    imageInputReconst(filename, None, None, save_address)