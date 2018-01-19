#encoding:utf-8
import os
import PIL.Image as Image
import re
import codecs
import numpy as np
from numpy import *
import random
import sys
import socket
from libtiff import TIFF
import tifffile as tifff


log_path = '/home/LiShuai/programme/python_T/log.txt'
logfile = open(log_path, 'w+')


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


def image_joint(new_file_jpg_dir, width=256, height=256):
    # new_file_jpg_dir is the directory of the total file
    # row_dir is the Rows of the extents include,
    # clumn_file is the Clumns of the extents include,
    # width is the width of one image,
    # height is the height of one image,
    # return a new_img of all image include by the extents.
    global logfile
    c = [a.split("/") for a in new_file_jpg_dir]
    print >> logfile, "In function image_joint \nc = %s\nnew_file_jpg_dir = %s" % (c, new_file_jpg_dir)

    d1 = [n[-2] for n in c]
    d2 = [n[-1] for n in c]
    dir_path1 = ''
    for iii in range(len(c[0])-2):
        if iii == 0:
            dir_path1 = dir_path1 + str(c[0][iii])
        else:
            dir_path1 = dir_path1 + '/' + str(c[0][iii])
    # dir_path1 = c[0][0] + '/' + c[0][1] + '/' + c[0][2] + '/' + c[0][3] + '/' + c[0][4]
    # print(new_file_jpg_dir)

    # extract the Rows
    # print(dir_path1)
    res1 = {}
    for i in d1:
        res1[i] = res1.get(i, 0) + 1
    row_dir = sorted([k1 for k1 in res1.keys()])

    # extract the Clumns
    res2 = {}
    for i in d2:
        res2[i] = res2.get(i, 0) + 1
    clumn_file = sorted([k2 for k2 in res2.keys()])
    print >> logfile, "clumn_file = %s" %clumn_file

    # joint
    new_img = Image.new('RGB', (width * len(clumn_file), height * len(row_dir)))
    y = 0
    for rows in row_dir:
        path1 = os.path.join(dir_path1, rows)
        # print(rows, path1)
        new_img1 = Image.new('RGB', (width * len(clumn_file), height), 255)
        x = 0
        for clumns in range(len(clumn_file)):
            clumn_name = clumn_file[clumns]
            path_dir = os.path.join(path1, clumn_name)
            if clumns == 0:
                img_block = Image.open(path_dir, 'r')
            else:
                clumn_name1 = clumn_file[clumns-1]
                clumn_name_number = int(clumn_name[1:7])
                clumn_name_number1 = int(clumn_name1[1:7])
                panduan = clumn_name_number - clumn_name_number1
                print >> logfile, "clumn_name_number = %s \n, clumn_name_number1 = %s\n" % (clumn_name_number, clumn_name_number1)
                if panduan == 1:
                    img_block = Image.open(path_dir, 'r')
                else:
                    img_block = Image.new('RGB', (width, height), 255)
            new_img1.paste(img_block, (x, 0))
            x += width
        new_img.paste(new_img1, (0, y))
        y += height
    new_img.save('/home/LiShuai/programme/python_T/aaaa.jpg')
    return new_img


def get_longitude_latitude(allfile_txt):
    # allfile_txt is the direction + the filename of txt
    # return latitude and longitude of each block
    wgs_lon_lat = []
    web_lon_lat = []
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
        f.close()
    return wgs_lon_lat


def determine_the_block(allfile_wgs_lat_lon, allfile_jpg, allfile_txt, point_lon_lat, block_length, width, new_file_jpg_dir, new_file_txt_dir):
    # allfile_wgs_lat_lon is the lon_lat of all blocks
    # allfile_jpg is a list of block_name include dir
    # allfile_txt is a list of block_txt include dir
    # point_lon_lat is the point of the input
	# block_length is the size of frame of input
    # return d include all block_name and dir in the extent new_file_jpg_dir, new_file_txt_dir
    global logfile
    a1 = mat(allfile_wgs_lat_lon)
    condition1 = (a1[:, 0] < point_lon_lat[0]) & (a1[:, 1] > point_lon_lat[1]) & (a1[:, 2] > point_lon_lat[0]) & (a1[:, 3] < point_lon_lat[1])
    condition2 = []
    for i in range(len(condition1)):
        if condition1[i]:
            condition2.append(i)

    d_0 = type(allfile_jpg)(map(lambda j: allfile_jpg[j], condition2))
    d_1 = type(allfile_txt)(map(lambda j: allfile_txt[j], condition2))
    e = type(allfile_wgs_lat_lon)(map(lambda j: allfile_wgs_lat_lon[j], condition2))
    e = mat(e)
    print >> logfile, "In function determine_the_block \nd_0 = %s,\td_1 = %s" % (d_0, d_1)

    c = [a.split("/") for a in d_0]
    c1 = [a.split("/") for a in d_1]
    d = ''
    d1 = ''
    print >> logfile, "c = %s,\tc1 = %s" % (c, c1)
    for iii in range(len(c[0])-1):
        if iii == 0:
            d = d + str(c[0][iii])
            d1 = d1 + str(c1[0][iii])
        else:
            d = d + '/' + str(c[0][iii])
            d1 = d1 + '/' + str(c1[0][iii])
    # d = c[0][0] + '/' + c[0][1] + '/' + c[0][2] + '/' + c[0][3] + '/' + c[0][4]  + '/' + c[0][5] + '/' + c[0][6]
    # d1 = c1[0][0] + '/' + c1[0][1] + '/' + c1[0][2] + '/' + c1[0][3] + '/' + c1[0][4] + '/' + c1[0][5] + '/' + c1[0][6]
    print >> logfile,"d = %s,\td1 = %s"%(d, d1)

    R_name = [n[-2] for n in c]
    C_jpg_name = [n[-1] for n in c]
    C_txt_name = [n[-1] for n in c1]
    R_name = str(R_name[0])
    C_jpg_name = str(C_jpg_name[0])
    C_txt_name = str(C_txt_name[0])
    R_number = int(R_name[1:])
    C_number = int(C_jpg_name[1:7])
    R_number_minus_1 = 'R0'+ str(R_number - 1)
    C_number_jpg_minus_1 = 'C' + str(C_number - 1) + '.jpg'
    C_number_txt_minus_1 = 'C' + str(C_number - 1) + '.txt'
    R_number_plus_1 = 'R0' + str(R_number + 1)
    C_number_jpg_plus_1 = 'C' + str(C_number + 1) + '.jpg'
    C_number_txt_plus_1 = 'C' + str(C_number + 1) + '.txt'

    c_str = ''
    for iii in range(len(c[0]) - 2):
        if iii == 0:
            c_str = c_str + str(c[0][iii])
        else:
            c_str = c_str + '/' + str(c[0][iii])
    print >> logfile, "c_str = %s"%c_str
    d = d + '/' + C_jpg_name
    d1 = d1 +  '/' + C_txt_name

    row_number, clumn_number = find_row_clumn(e , point_lon_lat, width)
    print >> logfile, "row_number = %s \t, clumn_number = %s\n" % (row_number, clumn_number)
    block_length1 = int(ceil(block_length / 2))
    if row_number < block_length1 and clumn_number < block_length1:
        R_increase1 = c_str  + '/' + R_number_minus_1  + '/' + C_number_jpg_minus_1
        R_increase2 = c_str  + '/' + R_number_minus_1  + '/' + C_jpg_name
        R_increase3 = c_str  + '/' + R_name  + '/' + C_number_jpg_minus_1
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(R_increase2)
        new_file_jpg_dir.append(R_increase3)
        new_file_jpg_dir.append(d)
        R_increase1 = c_str + '/' + R_number_minus_1 + '/' + C_number_txt_minus_1
        R_increase2 = c_str + '/' + R_number_minus_1 + '/' + C_txt_name
        R_increase3 = c_str + '/' + R_name + '/' + C_number_txt_minus_1
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(R_increase2)
        new_file_txt_dir.append(R_increase3)
        new_file_txt_dir.append(d1)
    if row_number < block_length1 and clumn_number >= block_length1 and (clumn_number + block_length1)<= width:
        R_increase1 = c_str + '/' +  R_number_minus_1 + '/' + C_jpg_name
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(d)
        R_increase1 = c_str + '/' + R_number_minus_1 + '/' + C_txt_name
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(d1)
    if row_number < block_length1 and (clumn_number + block_length1)> width:
        R_increase1 = c_str  + '/' + R_number_minus_1  + '/' + C_jpg_name
        R_increase2 = c_str  + '/' + R_number_minus_1  + '/' + C_number_jpg_plus_1
        R_increase3 = c_str  + '/' + R_name  + '/' + C_number_jpg_plus_1
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(R_increase2)
        new_file_jpg_dir.append(d)
        new_file_jpg_dir.append(R_increase3)
        R_increase1 = c_str + '/' + R_number_minus_1 + '/' + C_txt_name
        R_increase2 = c_str + '/' + R_number_minus_1 + '/' + C_number_txt_plus_1
        R_increase3 = c_str + '/' + R_name + '/' + C_number_txt_plus_1
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(R_increase2)
        new_file_txt_dir.append(d1)
        new_file_txt_dir.append(R_increase3)
    if row_number >= block_length1 and (row_number + block_length1) <= width and clumn_number < block_length1:
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_jpg_minus_1
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(d)
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_txt_minus_1
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(d1)
    if row_number >= block_length1 and (row_number + block_length1) <= width and clumn_number >= block_length1 and (clumn_number + block_length1)<= width:
        new_file_jpg_dir.append(d)
        new_file_txt_dir.append(d1)
    if row_number >= block_length1 and (row_number + block_length1) <= width and (clumn_number + block_length1) > width:
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_jpg_plus_1
        new_file_jpg_dir.append(d)
        new_file_jpg_dir.append(R_increase1)
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_txt_plus_1
        new_file_txt_dir.append(d1)
        new_file_txt_dir.append(R_increase1)
    if (row_number + block_length1) > width and clumn_number < block_length1:
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_jpg_minus_1
        R_increase2 = c_str + '/' +  R_number_plus_1 + '/' + C_number_jpg_minus_1
        R_increase3 = c_str + '/' +  R_number_plus_1 + '/' + C_jpg_name
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(d)
        new_file_jpg_dir.append(R_increase2)
        new_file_jpg_dir.append(R_increase3)
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_txt_minus_1
        R_increase2 = c_str + '/' +  R_number_plus_1 + '/' + C_number_txt_minus_1
        R_increase3 = c_str + '/' +  R_number_plus_1 + '/' + C_txt_name
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(d1)
        new_file_txt_dir.append(R_increase2)
        new_file_txt_dir.append(R_increase2)
        new_file_txt_dir.append(R_increase3)
    if (row_number + block_length1) > width and clumn_number >= block_length1 and (clumn_number + block_length1)<= width:
        R_increase1 = c_str + '/' +  R_number_plus_1 + '/' + C_jpg_name
        new_file_jpg_dir.append(d)
        new_file_jpg_dir.append(R_increase1)
        R_increase1 = c_str + '/' +  R_number_plus_1 + '/' + C_txt_name
        new_file_txt_dir.append(d1)
        new_file_txt_dir.append(R_increase1)
    if (row_number + block_length1) > width and (clumn_number + block_length1) > width:
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_jpg_plus_1
        R_increase2 = c_str + '/' +  R_number_plus_1 + '/' + C_jpg_name
        R_increase3 = c_str + '/' +  R_number_plus_1 + '/' + C_number_jpg_minus_1
        new_file_jpg_dir.append(d)
        new_file_jpg_dir.append(R_increase1)
        new_file_jpg_dir.append(R_increase2)
        new_file_jpg_dir.append(R_increase3)
        R_increase1 = c_str + '/' +  R_name + '/' + C_number_txt_plus_1
        R_increase2 = c_str + '/' +  R_number_plus_1 + '/' + C_txt_name
        R_increase3 = c_str + '/' +  R_number_plus_1 + '/' + C_number_txt_minus_1
        new_file_txt_dir.append(d1)
        new_file_txt_dir.append(R_increase1)
        new_file_txt_dir.append(R_increase2)
        new_file_txt_dir.append(R_increase3)
    # print('In function determine_the_block \n', 'new_file_jpg_dir = %l \n'%new_file_jpg_dir, file=logfile)
    return new_file_jpg_dir, new_file_txt_dir


def get_point_veg_type(veg_type, input_point):
    # print(input_point)
    # a = input_point.split(',')
    # a = [''.join(a1) for a1 in a]
    # input_lat_lon = [1, 1]
    # for aa in range(len(a)):
    #     input_lat_lon[aa] = float64(''.join(a[aa]))
    # img = TIFF.open(path_veg, mode='r')
    # img_new = img.read_image()
    # m,n = img_new.shape
    # img = tifff.imread(path_veg)
    img = veg_type
    m, n = img.shape
    take_clumn = input_point[0] - 96.9979281575203
    take_row = 42.0020786144249 - input_point[1]
    mm = img[int(math.ceil(take_row * m/(42.0020786144249-32.9999952810916)))][int(math.ceil(take_clumn * m/(42.0020786144249-32.9999952810916)))]
    # mm = img_new[int(math.ceil(take_row * n/360))][int(math.ceil(take_clumn*n/360))]
    # print(int(math.ceil(take_row * n/360)),int(math.ceil(take_clumn*n/360)))
    # print(img_new[2000][1000])
    # print(mm)
    # example: the code of cropland is 13
    if mm == 10:
        nn = 1
    else:
        nn = 0
    return nn


def find_row_clumn(a1,b1, width=256):
	# a1 is the lat_lon of the block
	# b1 is the lat_lon of the input point
	#return the location of the point in the block
    a1 = mat(a1)
    lie = int(ceil((b1[0]-a1[0, 0])/((a1[0, 2]-a1[0, 0])/width)))
    hang = int(ceil((-b1[1]+a1[0, 1])/((a1[0, 1]-a1[0, 3])/width)))
    return hang, lie	


def pick_the_block_from_new_image(new_jpg, new_file_txt_dir, point_lon_lat, block_length, width=256):
    ''' new_img is the new img  joint by the block include,
		new_file_txt_dir is the latitude and longitude of the block include,
		point_lon_lat is the point of the input'''
    global logfile
    wgs_lon_lat = get_longitude_latitude(new_file_txt_dir)
    a1 = mat(wgs_lon_lat)
    # row = row_number
    # clumn = clumn_number
    # print(a1)
    # new_img_extent = [np.nanmin(a1[:, 0]), np.nanmax(a1[:, 1]), np.nanmin(a1[:, 2]), np.nanmax(a1[:, 3])]
    new_img_extent = [a1[0, 0], a1[0, 1], a1[0, 2], a1[0, 3]]
    row, clumn = find_row_clumn(new_img_extent, point_lon_lat, width)
    print >> logfile, "In function pick_the_block_from_new_image \nrow = %s \t, clumn = %s" % (row, clumn)

    block_length1 = int(ceil(block_length / 2))
    print >> logfile, "block_length1 = %s" %block_length1
    region = (clumn - block_length1, row - block_length1, clumn + block_length1 - 1, row + block_length1 - 1)
    print >> logfile, region
    cropImg = new_jpg.crop(region)
    return cropImg


def new_block_img_label(file_path, point_lon_lat, block_length, veg_type):
	#output new block and label.
    allfile_jpg, allfile_txt = dirlist(file_path, [], [])
    allfile_wgs_lat_lon = get_longitude_latitude(allfile_txt)

    new_jpg_dir, new_txt_dir = determine_the_block(allfile_wgs_lat_lon, allfile_jpg, allfile_txt, point_lon_lat, block_length, 256, [], [])
    new_jpg = image_joint(new_jpg_dir)

    block_Img = pick_the_block_from_new_image(new_jpg, new_txt_dir, point_lon_lat, block_length)
    label = get_point_veg_type(veg_type, point_lon_lat)
    return block_Img, label	


def main_function(file_path, path_veg, saveToPath, block_length, number_block):
    '''the directory of all files'''
    ''' meantion to change. '''
    block_length = block_length
    number_block = number_block
    file_path = file_path
    path_veg = path_veg
    saveToPath = saveToPath
    # file_path = sys.argv[1]
    # path_veg = sys.argv[2]
    # saveToPath = sys.argv[3]

    veg_type = tifff.imread(path_veg)
    label = []
    pid = os.getpid()
    hostname = socket.gethostname()
    point_lon_lat1 = []
    for i in range(1, number_block + 1):
        name = "%010d" % i
        point_lon_lat2 = [random.uniform(107.75, 109.695), random.uniform(34.9027, 34.905)]
        point_lon_lat1.append(point_lon_lat2)
        block_Img, label1 = new_block_img_label(file_path, point_lon_lat2, block_length, veg_type)
        block_Img.save(saveToPath + "/img/%s_%d_%s.jpg"%(hostname, pid, name))
        label.append(label1)
        print("Completed : %d" % i)

    point_lon_lat = str(point_lon_lat1)
    point_lon_lat = point_lon_lat.replace("[","")
    point_lon_lat = point_lon_lat.replace("]","")+"\n"
    point_lon_lat = point_lon_lat.replace(", ","\n")
    lat_log_files = open(saveToPath + "/lat_log/%s_%d_lat_log.txt"%(hostname, pid), "w")
    lat_log_files.write(point_lon_lat)
    lat_log_files.close()

    pre = str(label)
    pre = pre.replace("[","")
    pre = pre.replace("]","")+"\n"
    pre = pre.replace(", ","\n")
    f = open(saveToPath + "/labels/%s_%d_labels.txt"%(hostname, pid),"w")
    f.write(pre)
    f.close()
    print("Congratulations!!")
