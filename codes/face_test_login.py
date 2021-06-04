# -*- codeing = utf-8 -*-
# @Time :2021/5/13 11:12
# @Author : 刘念卿
# @File : test0.py
# @Software : PyCharm
#import ctypes
#import inspect
import copy
import os
import shutil
import threading
from tkinter.scrolledtext import ScrolledText
from PIL import  ImageDraw, ImageFont
import dlib         # 人脸识别的库dlib
import numpy as np  # 数据处理的库numpy
import cv2          # 图像处理的库OpenCv
import pandas as pd # 数据处理的库Pandas
from idna import unicode
from mttkinter import mtTkinter as tk
import tkinter
from tkinter.messagebox import showerror,showinfo
from PIL import Image, ImageTk
from codes.kill import kill

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('./resource/shape_predictor_68_face_landmarks.dat')
facerec = dlib.face_recognition_model_v1("./resource/dlib_face_recognition_resnet_model_v1.dat")
# 处理存放所有人脸特征的 CSV
path_features_known_csv = "./data/features_all.csv"
csv_rd = pd.read_csv(path_features_known_csv, header=None)
# 存储姓名
name_list = []
path_name = './data/faces_from_camera/'
name = os.listdir(path_name)
for i in range(len(name)):
    name_list.append(name[i])
# 用来存放所有录入人脸特征的数组
features_known_arr = []
# known faces
for i in range(csv_rd.shape[0]):
    features_someone_arr = []
    for j in range(0, len(csv_rd.loc[i, :])):
        features_someone_arr.append(csv_rd.loc[i, :][j])
    features_known_arr.append(features_someone_arr)
# print("Faces in Database：", len(features_known_arr))

def face_rec():
    # 计算两个向量间的欧式距离
    def return_euclidean_distance(feature_1, feature_2):
        feature_1 = np.array(feature_1)
        feature_2 = np.array(feature_2)
        dist = np.sqrt(np.sum(np.square(feature_1 - feature_2)))
        # print("e_distance: ", dist)

        if dist > 0.43:
            return "diff"
        else:
            return "same"
    # 中文转码
    def paint_chinese_opencv(im, chinese, pos, color):
        img_PIL = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
        font = ImageFont.truetype('../resource/simsun.ttc', 35)
        fillColor = color  # (255,0,0)
        position = pos  # (100,100)
        if not isinstance(chinese, unicode):
            chinese = chinese.decode('utf-8')
        draw = ImageDraw.Draw(img_PIL)
        draw.text(position, chinese, font=font, fill=fillColor)

        img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
        return img
    # 暂存所有人的名字
    name_li = copy.deepcopy(name_list)
    global flag_srart,flag_end,cap_flag
    #开始录屏标志，False 开始录制视频
    flag_srart=True
    #结束录屏标志，true 结束录屏
    flag_end=False
    cap_flag = False

    while cap.isOpened():
        ret, frame = cap.read()
        if flag_srart:
            # print('stat',flag_srart,flag_end)
            # 未签到人员
            for I in range(len(name_li)):
                if name_li[I] not in scr1.get(1.0, 'end'):
                    scr1.insert('insert', name_li[I] + '\n')

            frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 人脸数 dets
            faces = detector(frame1, 0)
            # 存储所有人脸的名字
            pos_namelist = []
            name_namelist = []
            # 检测到人脸
            if len(faces) != 0:
                # 获取当前捕获到的图像的所有人脸的特征，存储到 features_cap_arr
                features_cap_arr = []
                for I in range(len(faces)):
                    shape = predictor(frame, faces[I])
                    features_cap_arr.append(facerec.compute_face_descriptor(frame, shape))
                # 遍历捕获到的图像中所有的人脸
                for k in range(len(faces)):
                    # 让人名跟随在矩形框的下方
                    # 确定人名的位置坐标
                    # 先默认所有人不认识，是 unknown
                    name_namelist.append("unknown")
                    # 每个捕获人脸的名字坐标
                    pos_namelist.append(
                        tuple([faces[k].left(), int(faces[k].bottom() + (faces[k].bottom() - faces[k].top()) / 14)]))
                    # print('post_name',pos_namelist[0][0],pos_namelist[0][1])
                    # 对于某张人脸，遍历所有存储的人脸特征
                    for I in range(len(features_known_arr)):
                        # print("with person_", str(i+1), "the ", end='')
                        # 将某张人脸与存储的所有人脸数据进行比对
                        compare = return_euclidean_distance(features_cap_arr[k], features_known_arr[I])
                        if compare == "same":  # 找到了相似脸
                            name_namelist[k] = name_list[I]
                            #已签到人员
                            if name_list[I] not in scr2.get(1.0, 'end'):
                                name_li.remove(name_list[I])
                                scr2.insert('insert', name_list[I] + '\n')
                                scr1.delete(1.0, 'end')
                    # 矩形框
                    for kk, d in enumerate(faces):
                        # 绘制矩形框
                        cv2.rectangle(frame, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (0, 255, 255), 2)
                # 写人脸名字
                for I in range(len(faces)):
                    frame = paint_chinese_opencv(frame, name_namelist[I], pos_namelist[I], (255, 0, 0))
        else:
            output.write(frame)
        frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame2 = Image.fromarray(frame1)
        frame3 = ImageTk.PhotoImage(frame2)
        vidLabel.configure(image=frame3)
        vidLabel.image = frame3
        if flag_end:
            vidLabel.place_forget()
            break

    cap.release()
    output.release()
    tkinter.messagebox.showinfo('提示', '录制视频已保存！')

#成功登录系统之后
def Sign():
    global win_second
    win_second=tk.Tk()
    win_second.title("考试登录系统")
    win_second.resizable(False, False)  # 固定窗口大小
    windowWidth = 800  # 获得当前窗口宽
    windowHeight = 490  # 获得当前窗口高
    screenWidth, screenHeight = win_second.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (
        windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    win_second.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    win_second.wm_attributes('-topmost', 1)  # 窗口置顶
    global cap,vidLabel,scr1,scr2,output
    # # opencv中视频录制需要借助VideoWriter对象， 将从VideoCapture 中读入图片，不断地写入到VideoWrite的数据流中。
    # # 指定视频编解码方式为MJPG 需要解码器
    codec = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 5  # 指定写入帧率为5
    frameSize = (640, 480)  # 指定窗口大小
    # # 创建 VideoWriter对象
    output = cv2.VideoWriter('Video.avi', codec, fps, frameSize)
    vidLabel = tk.Label(win_second,
                             width=350,
                             height=400)
    vidLabel.place(x=50, y=70)
    lab1=tk.Label(win_second,
                  text='未签到人员:',
                  font=('楷体',15))
    lab2 = tk.Label(win_second,
                    text='已签到人员:',
                    font=('楷体:', 15))
    lab1.place(x=450,y=40)
    lab2.place(x=650,y=40)
    def _exit():
        if os.path.exists('./screencap/Video.avi'):
            os.remove('./screencap/Video.avi')
        if os.path.exists('Video.avi'):
            shutil.move('Video.avi','./screencap')
        cap.release()
        pi=os.getpid()
        kill(pid=pi)
    button=tk.Button(win_second,
                     text="退出",
                     font=('黑体',15),
                     command=_exit)
    button.place(x=5,y=5)
    def _end():
        button2.place_forget()
        button1.place(x=185, y=5)
        global flag_end,flag_srart
        flag_end=True
        flag_srart=True
        # print('2',flag_end,flag_srart)
    def _start():
        global button2
        button1.place_forget()
        button2 = tk.Button(win_second,
                           text="结束录制",
                           font=('黑体', 15),
                           command=_end)
        button2.place(x=185, y=5)
        global flag_end
        flag_end=False
        global flag_srart
        flag_srart =False
        # print('1',flag_end,flag_srart)

    button1 = tk.Button(win_second,
                       text="开始录制",
                       font=('黑体', 15),
                       command=_start)
    button1.place(x=185, y=5)
    scr1 = ScrolledText(win_second, width=12, height=30, font=("隶书", 15))  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
    scr2 = ScrolledText(win_second, width=12, height=30, font=("隶书", 15))  # 滚动文本框（宽，高（这里的高应该是以行数为单位），字体样式）
    scr1.place(x=450,y=70)
    scr2.place(x=650,y=70)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, 600)
    cap.set(4, 480)
    def closeWindow():
        tkinter.messagebox.showinfo(title='关闭错误', message='请点击退出按钮！')  # 错误消息框
        return
    win_second.protocol('WM_DELETE_WINDOW', closeWindow)

    videoThread = threading.Thread(target=face_rec, args=())
    videoThread.start()
    win_second.mainloop()
#登录界面
def main(account,password):
    windows = tk.Tk()
    windows.title("考试登录系统")
    windows.resizable(False, False)  # 固定窗口大小
    windowWidth = 800  # 获得当前窗口宽
    windowHeight = 490  # 获得当前窗口高
    screenWidth, screenHeight = windows.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (
        windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    windows.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    windows.wm_attributes('-topmost', 1)  # 窗口置顶
    def _next():
        windows.destroy()
        Sign()
    def e():
        windows.destroy()
        pid = os.getpid()
        kill(pid=pid)  # 结束当前进程

    # 退出系统
    def exit_sys():
        button2 = tk.Button(windows,
                                 text="退出系统",
                                 font=("楷体", 15),
                                 command=e,
                                 width="10",
                                 height="1",
                                 activeforeground="blue"
                                 )
        button2.place(x=675, y=440)
    def sign():
        if entry1.get()==account and entry2.get()==password:
            # 隐藏控件
            text_lab.place_forget()
            text1_lab.place_forget()
            lable1.place_forget()
            lable2.place_forget()
            entry1.place_forget()
            entry2.place_forget()
            button1.place_forget()
            lab1=tk.Label(windows,
                               text='请认真阅读以下内容：\n'
                                    '1.点击确认按钮后，此界面将会关闭。\n'
                                    '2.请确认摄像头是否已经打开\n'
                                    '3.人脸识别时尽量排队来，以增加识别率\n'
                                    '4.识别失败请检查身份证，注意光照因素\n'
                                    '5.请严格监考！',
                               font=("楷体",20),
                               justify='left',
                               anchor='nw'
                               )
            lab1.place(x=155,y=85)
            button2=tk.Button(windows,
                                   text='确认',
                                   font=('黑体',15),
                                   activeforeground="blue",
                                   command=_next
                                   )
            button2.place(x=345,y=345)
        else:
            tkinter.messagebox.showerror('错误', '账号或密码错误！\n请确认之后在输入\n或者联系管理员')
    canva= tk.Canvas(windows,
                          width=800,
                          height=490,
                          bg='gray')
    global img_main#不可少，少了就显示不出来图片
    im=Image.open("./background/bg_main.jpg")
    img_main=ImageTk.PhotoImage(im)
    canva.create_image(400, 242, image=img_main)
    canva.pack()
    text_lab=tk.Label(windows,
                           text=" 考 试 登 录 系 统 ",
                           font=("楷体",40),
                           anchor='center')
    text_lab.place(x=135,y=80)
    text1_lab=tk.Label(windows,
                            text="请监考人员登录",
                            font=("楷体",20),
                            anchor="center")
    text1_lab.place(x=285,y=160)
    lable1=tk.Label(windows,text="账号:",
                         font=("黑体",11),
                         anchor="center")
    lable2 = tk.Label(windows, text="密码:",
                           font=("黑体", 11),
                           anchor="center")
    lable1.place(x=265,y=220)
    lable2.place(x=265,y=270)
    entry1=tk.Entry(windows)
    entry2=tk.Entry(windows,show="*")
    entry1.pack()
    entry2.pack()
    entry1.place(x=330,y=220)
    entry2.place(x=330,y=270)
    button1=tk.Button(windows,
                           text="登录",
                           font="楷体",
                           width="10",
                           height="1",
                           activeforeground="red",
                           command=sign)
    button1.place(x=345,y=315)
    exit_sys()
    windows.mainloop()

# if __name__ == '__main__':
#     main("root",'123456')
    # Sign()