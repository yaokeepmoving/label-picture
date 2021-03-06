# -*- coding: utf-8 -*-
'''
################# Label Picture ###################
## 使用方法：        
                     |先安装 pyqtgragh：pip install pyqtgraph
                     |修改 initialpath 到自己存储图片的路径
                     |修改 CLASSES 为自己的类别，运行label_picture.py
                     |先选择起始图片，再选择输出到的txt文档
                     |鼠标左键单击按下开始绘制图框，
                     |松开绘制完成，右键单击确认图框位置，
                     |输入标签编号，完成一个目标信息记录。
                     |w:   上一张图片 
                     |s:   下一张图片 
                     |a:   重新选择图片                      
## 作者：yulongpo
## 日期：2017/03/03
## 版本：LabelPic 0.1.3
'''

import cv2
import os
#import matplotlib.pyplot as plt
import copy
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui
import tkFileDialog as TFD

#class labal_picture(object):
#    def __init__(self, ):
key = cv2.waitKey(1) & 0xff   
 
'''起始路径'''    
initialpath = 'E:\\matlab\\data_gen\\im_data'#'G:/python/region_grasp'

ix, iy = -1, -1
x_end, y_end = 0, 0
im_row, im_col = 0, 0
drawing = False
#writing = False
output_info = ''

'''标签编号'''
CLASSES = ['__background__',
           'label1', 'label2', 'label3']
           
pg.mkQApp()

def select_img_path(initalpath = initialpath):
    '''选择被标签的图片'''
    filename = TFD.askopenfilename(initialdir = initialpath)
    filename_len = len(filename)
    for i in range(1, len(filename)):
        if filename[-i] == '/':
            path = filename[:filename_len - i + 1] #图片所在路径
            im_name = filename[filename_len -i + 1:] #图片名字
            break
    return path, im_name
    
def select_output_file(initalpath = initialpath):
    '''选择输出txt文件'''
    filename = TFD.askopenfilename(initialdir = initialpath)
    return filename
    
def get_pic_names(path):
    pic_names = []
    for _, __, ___ in os.walk(path):
        for item in ___:
            a = len(item)
            if item[a-3:] in ['jpg', 'JPG', 'PNG', 'png']:
                pic_names.append(item)
    return pic_names
        
def label_pic(event, x, y, flags, param):
    global key, index, file_path, pic_name, ix, iy, drawing
    global output_info, im_row, im_col
#    mode = True
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y      
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON or flags == 33:
        if drawing == True:
#            if mode == True:
            im = copy.deepcopy(img)
            im_row, im_col = im.shape[:2]
            cv2.rectangle(im, (ix, iy), (x, y), (0, 0, 255), 2)
#            cv2.namedWindow(os.path.join(file_path, all_pic_names[index]))
            cv2.imshow(os.path.join(file_path, all_pic_names[index]), im)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing == False
        x_end, y_end = x, y
        if ix == x:
            im = copy.deepcopy(img)
            cv2.imshow(os.path.join(file_path, all_pic_names[index]), im)
            print '!!! MOUSE NOT MOVED!!!'
        else:
            print all_pic_names[index], max(0, min(ix, x_end)), max(0, min(iy, y_end)),\
                    min(im_col, max(ix, x_end)), min(im_row, max(iy, y_end_end))
    if event == cv2.EVENT_RBUTTONDOWN and ix != x_end:
        label, ok = QtGui.QInputDialog.getInt(None, '输入标签', '标签编号')
        if ok:
            output_info = all_pic_names[index] +  ' ' + CLASSES[label] + ' ' + \
            str(max(0, min(ix, x_end))) + ' ' + str(max(0, min(iy, y_end))) + ' ' \
            + str(min(im_col, max(ix, x_end))) + ' '\
            + str(min(im_row, max(iy, y_end))) + '\n' #防止坐标位置越界！！！
            print('--OK!--[ {:s} ]--'.format(CLASSES[label]))
            output.write(output_info)
            if not os.path.exists(os.path.join(label_img_path, all_pic_names[index])):
                shutil.copyfile(os.path.join(file_path, all_pic_names[index]),
                              os.path.join(label_img_path, all_pic_names[index]))
            
            
if __name__ == '__main__':
     
    print '################# Label Picture ###################\n',\
    u'##  使用方法：\n',\
    u'\t\t|修改 initialpath 到自己存储图片的路径\n',\
    u'\t\t|修改CLASSES为自己的类别，运行label_picture.py\n',\
    u'\t\t|先选择起始图片，再选择输出到的txt文档\n',\
    u'\t\t|鼠标左键单击按下开始绘制图框，\n',\
    u'\t\t|松开绘制完成，右键单击确认图框位置，\n',\
    u'\t\t|输入标签编号，完成一个目标信息记录。\n',\
    u'\t\t|w:   上一张图片\n',\
    u'\t\t|s:   下一张图片\n',\
    u'\t\t|a:   重新选择图片\n', \
    u'\t\t|ESC: 退出\n', '## LabelPic 0.1.3\n' 
    file_path, pic_name = select_img_path()
    output_txt = select_output_file()
    output = open(output_txt, 'a')
#    print file_path
#    print get_pic_names(file_path)
    all_pic_names = get_pic_names(file_path)
#    print all_pic_names
    index = all_pic_names.index(pic_name)
#    print index
    w_cnt, s_cnt = 0, 0
#    img = cv2.imread('stuff.jpg')
    img = cv2.imread(os.path.join(file_path, pic_name))
    cv2.namedWindow(os.path.join(file_path, pic_name))
    cv2.imshow(os.path.join(file_path, pic_name), img)
    cv2.setMouseCallback(os.path.join(file_path, pic_name), label_pic)
    while(1):
        key = cv2.waitKey(1) & 0xff
        if key == 27:
            print u'退出'
            output.close()
            cv2.destroyAllWindows()
            break
        elif key == ord('w'):
            index = index - 1 if index > 1 else 0
            cv2.destroyAllWindows()
            cv2.namedWindow(os.path.join(file_path, all_pic_names[index]))
            cv2.setMouseCallback(os.path.join(file_path, all_pic_names[index]), label_pic)
            if index == 0:
                w_cnt += 1
            else:
                w_cnt = 0
            img = cv2.imread(os.path.join(file_path, all_pic_names[index]))
            cv2.imshow(os.path.join(file_path, all_pic_names[index]), img)
            print u'上一张'
        elif key == ord('s'):
            index = index + 1 if index < len(all_pic_names) - 1 \
            else len(all_pic_names) - 1
                    
            cv2.destroyAllWindows()
            cv2.namedWindow(os.path.join(file_path, all_pic_names[index]))
            cv2.setMouseCallback(os.path.join(file_path, all_pic_names[index]), label_pic)
            if index == len(all_pic_names) - 1:
                s_cnt += 1
            else:
                s_cnt == 0
            img = cv2.imread(os.path.join(file_path, all_pic_names[index]))
            cv2.imshow(os.path.join(file_path, all_pic_names[index]), img)
            print u'下一张'
        elif key == ord('a'):
            print u'重新选择'
            file_path, pic_name = select_img_path()
            all_pic_names = get_pic_names(file_path)
            index = all_pic_names.index(pic_name)
            cv2.destroyAllWindows()
            cv2.namedWindow(os.path.join(file_path, pic_name))
            cv2.setMouseCallback(os.path.join(file_path, pic_name), label_pic)
            img = cv2.imread(os.path.join(file_path, pic_name))
            cv2.imshow(os.path.join(file_path, pic_name), img)
            
        if w_cnt > 1:
            print 'This is the First PIC!'
            w_cnt = 1
        if s_cnt > 1:
            print 'This is the Last PIC!'
            s_cnt = 1
