#encoding:utf-8
import os
import PIL.Image as Image
import re
import codecs
import numpy as np
from numpy import *
import random
import socket
# from libtiff import TIFF
# import cProfile as pickle
import pickle


file_path = '/home/DL/LP/L18'

def dirlist(dir_path, allfile_jpg, allfile_txt):
    '''dir_path is dir of allfiles,
		allfile_jpg is a list of the jpg dir,
		allfile_txt is a list of the txt dir,
		allfile_jpg,allfile_txt is [] begin, and end with fulldata.'''

    filelist = os.listdir(dir_path)
    for filename in filelist:
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile_jpg, allfile_txt)
        else:
            if filepath.endswith('.jpg'):
                # print(filepath)
                c = filepath.split("/")
                C_jpg_name = c[-1]
                C_number = C_jpg_name.split('.')
                C_number_txt = C_number[0] + '.txt'
                filepath1 = ''
                for iii in range(len(c) - 1):
                    if iii == 0:
                        filepath1 = filepath1 + c[iii]
                    else:
                        filepath1 = filepath1 + '/' + c[iii]
                filepath1 = filepath1 + '/' + C_number_txt
                allfile_jpg.append(filepath)
                allfile_txt.append(filepath1)
            # if filepath.endswith('.txt'):
            #     allfile_txt.append(filepath)
    return allfile_jpg, allfile_txt


def get_longitude_latitude(allfile_txt):
    # allfile_txt is the direction + the filename of txt
    # return latitude and longitude of each block
    wgs_lon_lat = []
    # web_lon_lat = []
    for path1 in allfile_txt:
        if os.path.exists(path1):
            f = codecs.open(path1, 'r', 'gbk')
            lines = f.readlines()
            left_top = []
            right_bottom = []
            for line in lines:
                if line.find(u"左上角") != -1:
                    left_top.append(line[4:len(line)])
                if line.find(u"右下角") != -1:
                    right_bottom.append(line[4:len(line)])
            f.close()
		    #wgs_lon_lat
            # print(path1)
            # print(left_top)
            left_top1 = left_top[1].split(",")
            right_bottom1 = right_bottom[1].split(",")
            a = [1, 1, 1, 1]
            a[0] = float(left_top1[0])
            a[1] = float(left_top1[1])
            a[2] = float(right_bottom1[0])
            a[3] = float(right_bottom1[1])
        else:
            a = [np.nan, np.nan, np.nan, np.nan]
        wgs_lon_lat.append(a)
        #     #web_lon_lat
        # left_top1 = left_top[0].split(",")
        # right_bottom1 = right_bottom[0].split(",")
        # a = [1, 1, 1, 1]
        # a[0] = float(left_top1[0])
        # a[1] = float(left_top1[1])
        # a[2] = float(right_bottom1[0])
        # a[3] = float(right_bottom1[1])
        # web_lon_lat.append(a)

    # print("wgs get ok!")
    return wgs_lon_lat

allfile_jpg, allfile_txt = dirlist(file_path, [], [])
allfile_wgs_lat_lon = get_longitude_latitude(allfile_txt)

f1 = open('/home/LiShuai/programme/python_T/Result/jpg_txt_file_directory.pkl', 'wb')
pickle.dump(allfile_jpg, f1)
print("allfile_jpg ok!")
pickle.dump(allfile_txt, f1)
print("allfile_txt ok!")
pickle.dump(allfile_wgs_lat_lon, f1)
print("allfile_wgs_lat_lon ok!")
f1.close()
print("Congratulations!!")

# f2 = open('E:\\2016.20_NEW\\DL\\python_T\\try\\test1\\111.pkl', 'rb')
# allfile_jpg1 = pickle.load(f2)
# allfile_txt1 = pickle.load(f2)
# f2.close()
# print(allfile_jpg1, allfile_txt1)