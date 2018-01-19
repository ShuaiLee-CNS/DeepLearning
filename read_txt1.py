#encoding:utf-8
import os
import PIL.Image as Image
import re
import codecs
import numpy as np
from numpy import *

path  = 'E:\\2016.20_NEW\\DL\\python_T\\data'


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
                allfile_jpg.append(filepath)
            if filepath.endswith('.txt'):
                allfile_txt.append(filepath)
    return allfile_jpg, allfile_txt


def get_longitude_latitude(allfile_txt):
    # allfile_txt is the direction + the filename of txt
    # return latitude and longitude of each block

    wgs_lon_lat = []
    web_lon_lat = []
    for path1 in allfile_txt:
        f = codecs.open(path1, 'r', 'gbk')
        lines = f.readlines()
        left_top = []
        right_bottom = []
        for line in lines:
            if line.find(u"左上角") != -1:
                left_top.append(line[4:len(line)])
            if line.find(u"右下角") != -1:
                right_bottom.append(line[4:len(line)])
                # wgs_lon_lat
        left_top1 = left_top[1].split(",")
        right_bottom1 = right_bottom[1].split(",")
        a = [1, 1, 1, 1]
        a[0] = float(left_top1[0])
        a[1] = float(left_top1[1])
        a[2] = float(right_bottom1[0])
        a[3] = float(right_bottom1[1])
        wgs_lon_lat.append(a)

        # web_lon_lat
        left_top1 = left_top[0].split(",")
        right_bottom1 = right_bottom[0].split(",")
        a = [1, 1, 1, 1]
        a[0] = float(left_top1[0])
        a[1] = float(left_top1[1])
        a[2] = float(right_bottom1[0])
        a[3] = float(right_bottom1[1])
        web_lon_lat.append(a)
        f.close()
    return wgs_lon_lat, web_lon_lat


def determine_the_block(allfile_wgs_lat_lon, allfile_jpg, allfile_txt, point_lon_lat, block_length, width = 256):
    # allfile_wgs_lat_lon is the lon_lat of all blocks
    # allfile_jpg is a list of block_name include dir
    # allfile_txt is a list of block_txt include dir
    # point_lon_lat is the point of the input
    # return d include all block_name and dir in the extent
    a1 = mat(allfile_wgs_lat_lon)
    condition1 = (a1[:, 0] < point_lon_lat[0]) & (a1[:, 1] > point_lon_lat[1]) & (a1[:, 2] > point_lon_lat[0]) & (a1[:, 3] < point_lon_lat[1])
    condition2 = []
    for i in range(len(condition1)):
        if condition1[i]:
            condition2.append(i)

    d = type(allfile_jpg)(map(lambda j: allfile_jpg[j], condition2))
    d1 = type(allfile_txt)(map(lambda j: allfile_txt[j], condition2))
    e = type(a1)(map(lambda j: a1[j], condition2))

    c = [a.split("\\") for a in d]
    c1 = [a.split("\\") for a in d1]
    R_name = [n[-2] for n in c]
    C_jpg_name = [n[-1] for n in c]
    C_txt_name = [n[-1] for n in c1]
    R_name = str(R_name[0])
    C_jpg_name = str(C_jpg_name[0])
    R_number = int(R_name[1:])
    C_number = int(C_jpg_name[1:7])
    R_number_minus_1 = 'R0'+ str(R_number - 1)
    C_number_jpg_minus_1 = 'C' + str(C_number - 1) + '.jpg'
    C_number_txt_minus_1 = 'C' + str(C_number - 1) + '.txt'
    R_number_plus_1 = 'R0' + str(R_number + 1)
    C_number_jpg_plus_1 = 'C' + str(C_number + 1) + '.jpg'
    C_number_txt_plus_1 = 'C' + str(C_number + 1) + '.txt'

    row_number, clumn_number = find_row_clumn(e, point_lon_lat, width)
    block_length1 = int(ceil(block_length / 2))
    new_file_jpg_dir = []
    new_file_txt_dir = []
    if row_number < block_length1 and clumn_number < block_length1:
        R_increase1 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4]  + '\\' + R_number_minus_1  + '\\' + C_number_jpg_minus_1]
        R_increase2 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4]  + '\\' + R_number_minus_1  + '\\' + C_jpg_name]
        R_increase3 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4]  + '\\' + R_name  + '\\' + C_number_jpg_minus_1]
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(R_increase2)
        new_file_jpg_dir.append(R_increase3)
        new_file_jpg_dir.append(d)
        R_increase1 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4] + '\\' + R_number_minus_1 + '\\' + C_number_txt_minus_1]
        R_increase2 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4] + '\\' + R_number_minus_1 + '\\' + C_txt_name]
        R_increase3 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4] + '\\' + R_name + '\\' + C_number_txt_minus_1]
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(R_increase2)
        new_file_txt_dir.append(R_increase3)
        new_file_txt_dir.append(d1)
    if row_number < block_length1 and clumn_number > block_length1 & (clumn_number+block_length1)<= width:
        R_increase1 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4] + '\\' +  R_number_minus_1 + '\\' + C_jpg_name]
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(d)
        R_increase1 = [c[0][0] + '\\' + c[0][1] + '\\' + c[0][2] + '\\' + c[0][3] + '\\' + c[0][4] + '\\' + R_number_minus_1 + '\\' + C_txt_name]
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(d1)
    return new_file_jpg_dir, new_file_txt_dir


a1 = [10, 13, 14, 11]
b1 = [10.5, 11.5]


def find_row_clumn(a1,b1, width):
    lie = int(ceil((b1[0]-a1[0])/((a1[2]-a1[0])/width)))
    hang = int(ceil((-b1[1]+a1[1])/((a1[1]-a1[3])/width)))
    return hang, lie

# hang ,lie = find_common_type(a1,b1)

# block_length1 = int(ceil(block_length/2))
# new_file_fir = []


block_length = 30
point_lon_lat = [107.69, 34.9]
allfile_jpg, allfile_txt = dirlist(path, [], [])
allfile_wgs_lat_lon, web_lon_lat = get_longitude_latitude(allfile_txt)
determine_the_block(allfile_wgs_lat_lon, allfile_jpg, allfile_txt, point_lon_lat, block_length)

aaa = web_lon_lat[1]
lon_pixel = abs(aaa[0] - aaa[2])
lat_pixel = abs(aaa[1] - aaa[3])

aaa1 = web_lon_lat[800]
lon_pixel1 = abs(aaa1[0] - aaa1[2])
lat_pixel1 = abs(aaa1[1] - aaa1[3])
pixel1 = lon_pixel1/256
pixel2 = lat_pixel1/256


input_lat_lon_tmp = input('longtitude, latitude: ')
a = input_lat_lon_tmp.split(',')
a = [''.join(a1) for a1 in a]
input_lat_lon = [1, 1]
for aa in range(len(a)):
    input_lat_lon[aa] = float64(''.join(a[aa]))
# print(type(input_lat_lon[1]))


