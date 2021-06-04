# -*- codeing = utf-8 -*-
# @Time :2021/5/14 14:50
# @Author : 刘念卿
# @File : face_features_csv.py
# @Software : PyCharm
import cv2
import os
import dlib
from skimage import io
import csv
import numpy as np
import pandas as pd

#存储的脸部照片路径
path_faces_rd = "../data/faces_from_camera/"
#存储脸部特征路径
path_csv = "../data/csvs_from_camera/"
# 预测脸部
detector = dlib.get_frontal_face_detector()
# 预测脸部5点面部标志检测器将面部分为5个点，左眼2点、右眼2点、鼻子1点；这个模型更快，对于本项目来说
predictor = dlib.shape_predictor("../resource/shape_predictor_5_face_landmarks.dat")
# 深度残差网络，实现人脸识别
facerec = dlib.face_recognition_model_v1("../resource/dlib_face_recognition_resnet_model_v1.dat")
# 返回单张图像的128D特征
def return_128d_features(path_img):
    img = io.imread(path_img)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    dets = detector(img_gray, 1)
    print("检测的人脸图像：", path_img)
    # 因为有可能截下来的人脸再去检测，检测不出来人脸了
    # 所以要确保是 检测到人脸的人脸图像 拿去算特征
    if len(dets) != 0:
        shape = predictor(img_gray, dets[0])
        face_descriptor = facerec.compute_face_descriptor(img_gray, shape)#计算128D特征点，速度较慢，可使用gup加速，对于本项目来说十分重要
    else:
        face_descriptor = 0
        print("no face")
    # print(face_descriptor)
    return face_descriptor
# 将文件夹中照片特征提取出来，写入csv
# 输入input:
#   path_faces_personX:     图像文件夹的路径
#   path_csv:               要生成的csv路径
def write_into_csv(path_faces_personX, Path_csv):
    print(path_faces_personX)
    dir_pics = os.listdir(path_faces_personX)
    print('len',len(dir_pics))
    with open(Path_csv, "w", newline="") as Csvfile:
        Writer = csv.writer(Csvfile)
        for I in range(len(dir_pics)):
            print('I',I)
            # 调用return_128d_features()得到128d特征
            print("正在读的人脸图像：", path_faces_personX + "/" + dir_pics[I])
            features_128d = return_128d_features(path_faces_personX + "/" + dir_pics[I])
            #  print(features_128d)
            # 遇到没有检测出人脸的图片跳过
            if features_128d == 0:
                print(dir_pics[I]+'读取失败')
                I += 1
            else:
                Writer.writerow(features_128d)
# 读取 某人 所有的人脸图像的数据，写入 person_X.csv
faces = os.listdir(path_faces_rd)
for person in faces:
    print(path_csv + person + ".csv")
    write_into_csv(path_faces_rd + person, path_csv + person + ".csv")

# 从csv中读取数据，计算128d特征的均值
def compute_the_mean(Path_csv_rd):
    column_names = []
    # 128列特征
    for I in range(128):
        column_names.append("features_" + str(I + 1))
    # 利用pandas读取csv
    rd = pd.read_csv(Path_csv_rd, names=column_names)
    # 存放128维特征的均值
    Feature_mean = []
    for I in range(128):
        tmp_arr = rd["features_" + str(I + 1)]
        tmp_arr = np.array(tmp_arr)
        # 计算某一个特征的均值
        tmp_mean = np.mean(tmp_arr)
        Feature_mean.append(tmp_mean)
    return Feature_mean

# 存放所有特征均值的 CSV 的路径
path_csv_feature_all = "../data/features_all.csv"
if  os.path.exists(path_csv_feature_all):
    # 存放人脸特征的csv的路径
    path_csv_rd = "../data/csvs_from_camera/"
    #把所有的特征值写入一个总的.csv中
    with open(path_csv_feature_all, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        csv_rd = os.listdir(path_csv_rd)
        print("特征均值: ")
        for i in range(len(csv_rd)):
            feature_mean = compute_the_mean(path_csv_rd + csv_rd[i])
            # print(feature_mean)
            print(path_csv_rd + csv_rd[i])
            writer.writerow(feature_mean)
else:
    file=open(path_csv_feature_all, "w", newline="")
    file.close()