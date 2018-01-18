import os
import pickle
import fnmatch
import natsort

def dirlist(dir_path, allfile_txt):
    '''dir_path is dir of allfiles,
		allfile_jpg is a list of the jpg dir,
		allfile_txt is a list of the txt dir,
		allfile_jpg,allfile_txt is [] begin, and end with fulldata.'''

    filelist = os.listdir(dir_path)
    for filename in filelist:
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile_txt)
        else:
            if filepath.endswith('.jpg'):
                allfile_txt.append(filepath)
    return allfile_txt

dir_files = "/home/DL/LP/LAST_result/img"
out_path = "/home/DL/LP/LAST_result"
log = "/home/DL/LP/LAST_result/log2.txt"
logfile = open(log, 'w+')
# out_path_img_dir = "/home/DL/LP/LAST_result/all_img_dir.plk"

image_files = dirlist(dir_files, [])
image_files = natsort.natsorted(image_files)
# image_files = str(image_files)
# image_files = image_files.replace("],[", "\n")
# image_files = image_files.replace("[", "")
# image_files = image_files.replace("]", "")
# image_files = image_files.replace(", ", "\n")
# logfile.write(image_files)
new_path = []
for i in range(0, len(image_files)):
    name = "%010d" % (i+1)
    one_jpg = image_files[i]
    print >> logfile, one_jpg.split('/')[-1]
    os.popen('cp %s %s/rename_img/%s.jpg' % (one_jpg, out_path, name))
    new_path1 = '%s/rename_img/%s.jpg' % (out_path, name)
    new_path.append(new_path1)
logfile.close()
f1 = open(out_path + "/all_img_dir.plk", 'wb')
pickle.dump(new_path, f1)
f1.close()

new_path1 = new_path[1:10000]
f2 = open(out_path + "/all_img_dir1.plk", 'wb')
pickle.dump(new_path1, f2)
f2.close()
print("Congratulations!!!")