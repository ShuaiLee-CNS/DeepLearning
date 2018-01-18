import os
import socket
import pickle
import time
import PIL.Image as Image
import numpy as np
from numpy import *
import random

file_path = "/home/LiShuai/programme/python_T/labels_by_human"
want_numbers = 10


pid = os.getpid()
hostname = socket.gethostname()
time1 = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
file_host_path = '%s/%s_%d_%s' % (file_path, hostname, pid, time1)
os.popen('mkdir %s' % file_host_path)
os.popen('mkdir %s/static/' % file_host_path)
os.popen('mkdir %s/img/' % file_host_path)
os.popen('mkdir %s/labels/' % file_host_path)
os.popen('mkdir %s/lat_log/' % file_host_path)
os.popen('mkdir %s/predictions/' % file_host_path)
os.popen('mkdir %s/logs/' % file_host_path)
os.popen('mkdir %s/templates/' % file_host_path)

os.popen('cp %s/allfile_jpg_latlog1.pkl %s/' % (file_path, file_host_path))
os.popen('cp %s/labels_by_human1.py %s' % (file_path, file_host_path))
os.popen('cp /home/LiShuai/programme/python_T/test/templates/* %s/templates/' % file_host_path)
# os.popen('cp %s/labels_by_human.py %s/' % (file_path, file_host_path))

os.chdir(file_host_path)
# import labels_by_human as lbh

f2 = open(file_host_path + '/allfile_jpg_latlog1.pkl', 'rb')
allfile_jpg = pickle.load(f2)
allfile_latlog = pickle.load(f2)

len_jpg = len(allfile_jpg)
random_number = random.sample(range(len_jpg), want_numbers)
name = []
for ii in range(0, want_numbers):
    name1 = "%010d" % (ii+1)
    print(name1)
    # random_number = random.randint(0, len_jpg)
    os.popen('cp %s %s/static/%s.jpg' % (allfile_jpg[random_number[ii]], file_host_path, name1))
    aa_jpg1 = allfile_jpg[random_number[ii]].split('/')
    aa_jpg2 = aa_jpg1[-1]
    name11 = '/static/%s.jpg' % name1
    name.append(name11)
    # os.popen('python %s/test_web.py 12345 %s' % (file_host_path, name))

    region = (113, 113, 142, 142)
    img_block = Image.open(allfile_jpg[random_number[ii]], 'r')
    block_Img = img_block.crop(region)
    block_Img.save(file_host_path + "/img/%s_%d_%s.jpg" % (hostname, pid, name1))
    log_lat = allfile_latlog[random_number[ii]]
    log_lat_mat = mat(log_lat)
    # print(log_lat_mat[0,0])
    # print(type(log_lat_mat[0, 0]))
    log_lat1 = [(log_lat_mat[0, 0] + log_lat_mat[0, 2])/2, (log_lat_mat[0, 1] + log_lat_mat[0, 3])/2]


    #save lat_log
    point_lon_lat = str(log_lat1)
    point_lon_lat = point_lon_lat.replace("[", "")
    point_lon_lat = point_lon_lat.replace("]", "")
    point_lon_lat = point_lon_lat.replace(", ", ",")
    lat_log_files = open(file_host_path + "/lat_log/%s_%d_lat_log.txt" % (hostname, pid), "a")
    lat_log_files.write("%s\n" % point_lon_lat)
    # if ii == 1:
    #     lat_log_files.write(point_lon_lat)
    # else:
    #     lat_log_files.write("\n%s" % point_lon_lat)
    lat_log_files.close()

    '''labels = str(label1)
    labels = labels.replace("[", "")
    labels = labels.replace("]", "")
    # labels = labels.replace(", ", "\n")
    f = open(file_host_path + "/labels/%s_%d_labels.txt" % (hostname, pid), "a")
    f.write("%s\n" % labels)'''
    # if ii == 1:
    #     f.write(labels)
    # else:
    #     f.write("\n%s" % labels)
    # f.close()

    #remove jpg
    # os.popen('rm %s/name' % file_host_path)
    # random_jpg = [allfile_jpg[n] for n in random_number]
f1 = open('%s/jpg_file_directory.pkl' % file_host_path, 'wb')
pickle.dump(name, f1)
f1.close()
os.popen('python %s/labels_by_human1.py 12345 %s %s %d' % (file_host_path, file_host_path, hostname, pid))