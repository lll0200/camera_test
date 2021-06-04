# -*- codeing = utf-8 -*-
# @Time :2021/5/14 9:06
# @Author : 刘念卿
# @File : get_face_image.py
# @Software : PyCharm
import threading
import time

import dlib         # 人脸识别的库 Dlib
import numpy as np  # 数据处理的库 Numpy
import cv2          # 图像处理的库 OpenCv
import os
import shutil
import tkinter as tk
import tkinter.messagebox
from PIL import Image, ImageTk
from kill import kill

# Dlib 预测器
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('../resource/shape_predictor_68_face_landmarks.dat')
# 人脸保存路径
path_make_dir = "../data/faces_from_camera/"
# 人脸数据保存路径
path_csv = "../data/csvs_from_camera/"

#窗口背景
def bg(win):
    canva= tk.Canvas(win,
                     bg='gray')

    global img_main#不可少，少了就显示不出来图片
    im=Image.open("../background/d.jpg")
    img_main=ImageTk.PhotoImage(im)
    canva.create_image(200, 120, image=img_main)
    canva.pack()

def exit_sys():
    cap_flag = False
    pid = os.getpid()
    kill(pid=pid)  # 结束当前进程

def exit_sys_button(w):
    button2=tk.Button(w,
                     text="退出",
                     bg="red",
                     font=("黑体",15),
                     command=exit_sys
                     )
    button2.place(x=325,y=200)
def video():
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    person_name = entry.get()
    #print('name',person_name)
    # 创建 cv2 摄像头对象
    # cap.set(propId, value)
    # 设置视频参数，propId 设置的视频参数，value 设置的参数值
    cap.set(3, 480)
    # 截图 screenshoot 的计数器
    # cnt_ss = 0
    # 人脸截图的计数器
    cnt_p = 0
    # 存储人脸的文件夹
    current_face_dir = '0'
    num=0
    cap_flag=cap.isOpened()
    # 成功打开摄像头
    while cap_flag:
        # a=time.time()
        flag, im_rd = cap.read()
        # 每帧数据延时 1ms，延时为 0 读取的是静态帧
        cv2.waitKey(1)
        num+=1#帧数  每帧延时1ms秒
        # 取灰度
        img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)
        # 人脸数 rects
        rects = detector(img_gray, 0)
        # 待会要写的字体
        font = cv2.FONT_HERSHEY_COMPLEX
        #保存的人脸路径
        current_face_dir = path_make_dir + person_name
        #print(current_face_dir)

        if num==1:#首先需要判断原有信息是否存在，存在则删除，否则新建
            # 如果新建的文件夹存在，则删除存在的文件夹
            for dirs in (os.listdir(path_make_dir)):
                if current_face_dir == path_make_dir + dirs:
                    shutil.rmtree(current_face_dir)  # shutil.rmtree() #递归地删除文件 如果存在以下树结构
                    print("删除旧的文件夹:", current_face_dir)
            os.makedirs(current_face_dir)
            print("新建的人脸文件夹: ", current_face_dir)

        if len(rects) != 0:
            # 检测到人脸，矩形框
            for k, d in enumerate(rects):
                # 计算矩形框大小
                height = d.bottom() - d.top()
                width = d.right() - d.left()
                cv2.rectangle(im_rd, tuple([d.left(), d.top()]), tuple([d.right(), d.bottom()]), (255, 0, 255), 2)

                # 根据人脸大小生成空的图像
                im_blank = np.zeros((height, width, 3), np.uint8)
                #没十帧保存一次图象
                if num%10==0:
                    cnt_p += 1
                    if cnt_p== 10:
                        cap_flag=False
                    for ii in range(height):
                        for jj in range(width):
                            im_blank[ii][jj] = im_rd[d.top() + ii][d.left() + jj]
                    cv2.imencode('.jpg', im_blank)[1].tofile(current_face_dir + '/' +person_name+ '_'+str(cnt_p) + '.jpg')
                    print("写入本地：", current_face_dir + '/' + person_name+'_'+str(cnt_p) + '.jpg' + "采集成功")
                    # b = time.time()
                    # print('sads',cnt_p + b - a)


        # 显示人脸数
        cv2.putText(im_rd, "Faces: " + str(len(rects)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

        cv2.imshow("camera", im_rd)
    entry.delete(0,"end")
    # 释放摄像头
    cap.release()
    # 删除建立的窗口
    cv2.destroyAllWindows()

def start():
    global  windows
    windows.destroy()
    second=tk.Tk()
    second.title("登记")
    second.resizable(False, False)  # 固定窗口大小
    secondWidth = 400  # 获得当前窗口宽
    secondHeight = 245  # 获得当前窗口高
    screeWidth, screeHeight = second.maxsize()  # 获得屏幕宽和高
    geometryParam_second = '%dx%d+%d+%d' % (
        secondWidth, secondHeight, (screeWidth - secondWidth) / 2, (screeHeight - secondHeight) / 2)
    second.geometry(geometryParam_second)  # 设置窗口大小及偏移坐标
    second.wm_attributes('-topmost', 1)  # 窗口置顶

    def judge_name():
        for _char in entry.get():
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
            return True

    def ok():
        a = judge_name()
        if not a:
            tk.messagebox.showwarning('错误', '请确认姓名为全中文')
        else:
            print(entry.get() + "的信息正在采集..." + '请根据提示进行操作')
            video()

    bg(second)
    lab1 = tk.Label(second,
                    text="请输入姓名：")
    lab1.place(x=100, y=29)
    global entry
    entry = tk.Entry(second,
                     font="黑体")
    entry.place(x=100, y=50)

    button3 = tk.Button(second,
                        text="ok",
                        font=("黑体", 15),
                        command=ok,
                        bg="blue"
                        )
    button3.place(x=155, y=100)
    exit_sys_button(second)
    second.mainloop()
def main():
    global windows
    windows=tk.Tk()
    windows.title("登记")
    windows.resizable(False, False)  # 固定窗口大小
    windowWidth = 400  # 获得当前窗口宽
    windowHeight = 245  # 获得当前窗口高
    screenWidth, screenHeight = windows.maxsize()  # 获得屏幕宽和高
    geometryParam = '%dx%d+%d+%d' % (
        windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
    windows.geometry(geometryParam)  # 设置窗口大小及偏移坐标
    windows.wm_attributes('-topmost', 1)  # 窗口置顶

    # 清除旧的数据
    def pre_clear():
        #print("sds",type(entry.get()))
        if os.path.exists(path_make_dir):
            folders_rd = os.listdir(path_make_dir)
            for i in range(len(folders_rd)):
                shutil.rmtree(path_make_dir + folders_rd[i])
            print('清除人脸数据成功！')
        else:
            os.makedirs(path_make_dir)
            print('文件创建成功！')
        if os.path.exists(path_csv):
            csv_rd = os.listdir(path_csv)
            for i in range(len(csv_rd)):
                os.remove(path_csv + csv_rd[i])
            print('清楚人脸图象成功！')
        else:
            os.makedirs(path_csv)
            print('文件创建成功！')

    bg(windows)
    button1=tk.Button(windows,
                     text="开始",
                     bg="blue",
                     font=("黑体",15),
                     command=start
                     )
    button1.place(x=55,y=100)
    button=tk.Button(windows,
                     text="清空旧数据",
                     bg="blue",
                     font=("黑体",15),
                     command=pre_clear
                     )
    button.place(x=225,y=100)
    exit_sys_button(windows)
    windows.mainloop()
if __name__ == '__main__':
    main()