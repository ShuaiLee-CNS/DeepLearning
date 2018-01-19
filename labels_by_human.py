import os
import socket
import pickle
import random
import time
import web
from numpy import *
import PIL.Image as Image

file_path = '/home/LiShuai/programme/python_T/labels_by_human'
pid = os.getpid()
hostname = socket.gethostname()
time1 = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
file_host_path = '%s/_%s_%d_%s' % (file_path, hostname, pid, time1)

#read jpg txt
f2 = open(file_path + '/', 'allfile_jpg_txt.pkl', 'rb')
allfile_jpg = pickle.load(f2)
allfile_txt = pickle.load(f2)

#create random number
want_numbers = 1000
random_number = random.sample(range(len(allfile_jpg)), want_numbers)


# for ii in range(0, want_numbers + 1):
#     os.popen('cp %s %s/static/' % (allfile_jpg[random_number[0]], file_path))'''
'''
file_path = '/home/LiShuai/programme/python_T/labels_by_human'

pid = os.getpid()
hostname = socket.gethostname()
time1 = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
file_host_path = '%s/%s_%d_%s' % (file_path, hostname, pid, time1)
os.popen('mkdir %s' % file_host_path)
os.popen('mkdir %s/static' % file_host_path)
os.popen('mkdir %s/img' % file_host_path)
os.popen('mkdir %s/labels' % file_host_path)
os.popen('mkdir %s/lat_log' % file_host_path)
os.popen('mkdir %s/predictions' % file_host_path)
os.popen('mkdir %s/logs' % file_host_path)
print(file_host_path)

os.popen('cp %s/allfile_jpg_latlog.pkl %s/' % (file_path, file_host_path))
os.popen('cp %s/labels_by_human.py %s/' % (file_path, file_host_path))

f2 = open(file_host_path + '/allfile_jpg_latlog.pkl', 'rb')
allfile_jpg = pickle.load(f2)
allfile_latlog = pickle.load(f2)

#templates directory
render = web.template.render('/home/LiShuai/programme/python_T/test/templates/')

urls = ('/(.*)', 'signin')
# app = web.application(urls, globals())

'''
class signin:
    def GET(self):
        return render.index9()

    def POST(self):
        data = web.input()
        aa_host = data['host']
        aa_pass = data['passwd']
        # create host directory
        os.popen('mkdir %s/%s_%s_%s_%d_%s' % (file_path, aa_host, aa_pass, hostname, pid, time1))
        os.popen('mkdir %s/%s_%s_%s_%d_%s/static' % (file_path, aa_host, aa_pass, hostname, pid, time1))
        os.popen('mkdir %s/%s_%s_%s_%d_%s/static' % (file_path, aa_host, aa_pass, hostname, pid, time1))
        os.popen('cp %s/allfile_jpg_txt.pkl %s/%s_%s_%s_%d_%s' % (file_path, file_path, aa_host, aa_pass, hostname, pid, time1))
        raise web.seeother('/begin ')'''

app = web.application(urls, globals())
app.run()
class signin:
    def GET(self, name):
        # name = "/static/C101217.jpg"
        return render.index9()

    def POST(self, name):
        post_data = web.input()
        # labels = post_data['crop']
        # print(labels)
        want_numbers = int(post_data['want_numbers'])
        random_number = random.sample(range(len(allfile_jpg)), want_numbers)
        for ii in range(0, want_numbers+1):
            os.popen('cp %s %s/static/' % (allfile_jpg[random_number[ii]], file_host_path))
            aa_jpg1 = allfile_jpg[random_number[ii]].splt('/')
            aa_jpg2 = aa_jpg1[-1]
            name2 = '/static/%s' % aa_jpg2
            raise render.index8('%s' % name2)
            post_data1 = web.input()
            labels = post_data1['crop']

            region = (113, 113, 142, 142)
            img_block = Image.open(allfile_jpg[random_number[0]], 'r')
            block_Img = img_block.crop(region)
            name1 = "%010d" % ii
            block_Img.save(file_host_path + "/img/%s_%d_%s.jpg" % (hostname, pid, name1))
            log_lat = allfile_latlog[random_number[ii]]
            log_lat_mat = mat(log_lat)
            log_lat1 = [(log_lat_mat[0] + log_lat_mat[2]) / 2, (log_lat_mat[1] + log_lat_mat[3]) / 2]

            # save lat_log
            # point_lon_lat = str(log_lat1)
            # point_lon_lat = point_lon_lat.replace("[", "")
            # point_lon_lat = point_lon_lat.replace("]", "")
            point_lon_lat = log_lat1.replace(", ", ",")
            lat_log_files = open(file_host_path + "/lat_log/%s_%d_lat_log.txt" % (hostname, pid), "a")
            if ii == 1:
                lat_log_files.write(point_lon_lat)
            else:
                lat_log_files.write("\n%s" % point_lon_lat)
            lat_log_files.close()

            #save labels
            # labels = str(label1)
            # labels = labels.replace("[", "")
            # labels = labels.replace("]", "")
            # labels = labels.replace(", ", "\n")
            f = open(file_host_path + "/labels/%s_%d_labels.txt" % (hostname, pid), "a")
            f.write("%s\n" % labels)


def main():
    '''file_path = '/home/LiShuai/programme/python_T/labels_by_human'

    pid = os.getpid()
    hostname = socket.gethostname()
    time1 = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
    file_host_path = '%s/%s_%d_%s' % (file_path, hostname, pid, time1)
    os.popen('mkdir %s' % file_host_path)
    os.popen('mkdir %s/static' % file_host_path)
    os.popen('mkdir %s/img' % file_host_path)
    os.popen('mkdir %s/labels' % file_host_path)
    os.popen('mkdir %s/lat_log' % file_host_path)
    os.popen('mkdir %s/predictions' % file_host_path)
    os.popen('mkdir %s/logs' % file_host_path)
    print(file_host_path)

    os.popen('cp %s/allfile_jpg_latlog.pkl %s/' % (file_path, file_host_path))
    os.popen('cp %s/labels_by_human.py %s/' % (file_path, file_host_path))

    f2 = open(file_host_path + '/allfile_jpg_latlog.pkl', 'rb')
    allfile_jpg = pickle.load(f2)
    allfile_latlog = pickle.load(f2)'''

    app = web.application(urls, globals())
    app.run()
# # if __name__ == "__main__":
# #     app = web.application(urls, globals())
# #     app.run()
if __name__ == "__main__":
    main()