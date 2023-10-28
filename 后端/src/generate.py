import sys

import cv2 as cv
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow



np.set_printoptions(threshold=np.inf)


class Img(object):
    def __init__(self, data, part=False):
        # origin img data
        self.data = data
        # blocks(M*N, 4, 4)
        self.data_ = Partition(self.data)
        # Key(a prime number)
        self.__kesei = 1003091
        # a large number
        self.__G = 33503

        self.shape = data.shape

        self.b1 = None
        self.b2 = None
        self.Q1 = None
        self.Q2 = None
        if not part:
            # the mean of each block
            self.mu = self.cal_mu()
            self.b1 = self.cal_M1()
            self.Q1, self.Q2 = self.cal_Q()
            self.b2 = self.cal_M2()
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

    # watermark embed
    def Embedding(self):
        C = Partition(self.data, 4)
        M1 = Partition(self.M1, 4)
        M2 = Partition(self.M2, 4)

        N = C.shape[0]
        # save the 1LSB
        B1 = np.zeros((N, 4, 4), dtype=np.uint8)

        for i in range(N):
            Pn = C[i].copy()
            Mn1 = M1[i].copy()
            Mn2 = M2[i].copy()

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
            Vsum[i] = np.sum(cn * C[i].reshape(-1)) % self.__G
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

    # Watermark Extract
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

    # Watermark Authentication and Reconstruct
    def Authentication_Reconstruct(self):
        data_blocks = self.data_
        B = self.Extracting()
        B = Partition(B, 4)

        N = data_blocks.shape[0]
        row = self.shape[0] // 4

        cn = np.arange(self.__G, self.__G + 16)
        Vsum = np.zeros((N,), dtype=np.int16)
        R = np.zeros(self.data_.shape, dtype=np.uint8)

        # Max = -1

        print(N)
        for i in range(N):
            Pn = data_blocks[i]
            Bn = B[i]
            Psum = 0
            for j in range(4):
                for k in range(4):
                    Psum += (Pn[j, k] % 2) * (1 << (j * 4 + k))

            Vsum[i] = np.sum(cn * Pn.reshape(-1)) % self.__G

            # Max = np.max((Max, np.abs(Vsum[i] - Psum)))

            # 取n = sqrt(N)
            # 转成n*n之后

            # if Vsum[i] == Psum:
            if np.abs(Vsum[i] - Psum) <= 100:
                R[i] = Pn
            else:
                R[i] = Bn
                self.Authentication_blocks[i // row * 4:i // row * 4 + 4, (i % row) * 4:(i % row) * 4 + 4] = 255

        # print(Max)

        return R


# image2blocks
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


# blocks2image
def Union(img, shape, radio=4):
    img_compress = np.zeros(shape, dtype=np.uint8)
    x = shape[1] // radio
    for i in range(img.shape[0]):
        yy = i // x
        xx = i % x
        img_compress[yy * radio:yy * radio + radio, xx * radio:xx * radio + radio] = img[i]

    return img_compress


# image reconstruct
def show_compress(img, shape, filename=None):
    img_compress = np.zeros(shape, dtype=np.uint8)
    x = shape[1] // 4
    for i in range(img.shape[0]):
        yy = i // x
        xx = i % x
        img_compress[yy * 4:yy * 4 + 4, xx * 4:xx * 4 + 4] = img[i]

    cv.imshow("img", img_compress)
    cv.waitKey(0)
    cv.imwrite(filename, img_compress)

def save_image(img, shape, filename=None):
    img_compress = np.zeros(shape, dtype=np.uint8)
    x = shape[1] // 4
    for i in range(img.shape[0]):
        yy = i // x
        xx = i % x
        img_compress[yy * 4:yy * 4 + 4, xx * 4:xx * 4 + 4] = img[i]

    cv.imwrite(filename, img_compress)

def mapping(M1, kesei):
    mapping = np.zeros(M1.shape[0], dtype=np.int64)
    # generate [0,R) mapping sequence
    for i in range(M1.shape[0]):
        mapping[i] = (kesei * (i + 1)) % M1.shape[0]

    for i in range(M1.shape[0]):
        # t = M1[i].copy()
        # M1[i] = M1[mapping[i]].copy()
        # M1[mapping] = t.copy()
        M1[i], M1[mapping[i]] = M1[mapping[i]].copy(), M1[i].copy()

    return M1


def Imapping(M1, kesei):
    mapping = np.zeros(M1.shape[0], dtype=np.int64)
    # generate [0,R) mapping sequence
    for i in range(M1.shape[0]):
        mapping[i] = (kesei * (i + 1)) % M1.shape[0]

    for i in range(M1.shape[0] - 1, -1, -1):
        # t = M1[i].copy()
        # M1[i] = M1[mapping[i]].copy()
        # M1[mapping] = t.copy()
        M1[i], M1[mapping[i]] = M1[mapping[i]].copy(), M1[i].copy()

    return M1

# 向目的地址图像中嵌入数字水印，返回Img对象
def embedWatermarkInImage(originImageFilename):
    img = np.array(cv.imread(originImageFilename, 0))
    img = Img(img)
    new_img = img.Embedding()
    return new_img

# 传入Img对象与保存的文件路径，将图片保存
def saveImageByImg(img,saveFilename):
    save_image(img, img.shape, saveFilename)

if __name__ == '__main__':
    filename = '../image/original/boat_RGB.png'
    img = np.array(cv.imread(filename, 0))
    img = Img(img)
    new_img = img.Embedding()
    show_compress(new_img, img.shape, "../image/embedded/boat_.png")

    # img = np.array(cv.imread("../image/tampered/lena_changed.png", 0))
    # # img = np.array(cv.imread("../image/goldhill_changed3.png", 0))
    # img = Img(img, True)
    #
    # img_reconstruction = img.Authentication_Reconstruct()
    # cv.imshow("Authentication", img.Authentication_blocks)
    # show_compress(img_reconstruction, img.shape, "../image/reconstruction.png")
    # cv.waitKey(0)
