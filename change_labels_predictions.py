import os
import codecs
import pickle
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
            if filepath.endswith('.txt'):
                allfile_txt.append(filepath)
    return allfile_txt


dir_labels_files = "/home/DL/LP/LAST_result/labels"
dir_preditions_files = "/home/DL/LP/LAST_result/labels"
out_dir = "/home/DL/LP/LAST_result"
log = "/home/DL/LP/LAST_result/log1.txt"
logfile = open(log, 'w+')

labels_dir = dirlist(dir_labels_files, [])
predictions_dir = dirlist(dir_preditions_files, [])
labels_dir = natsort.natsorted(labels_dir)
predictions_dir = natsort.natsorted(predictions_dir)

predictions = []
labels = []
if len(labels_dir) == len(predictions_dir):
    for i in range(0, len(labels_dir)):
        print >> logfile, predictions_dir[i]
        print >> logfile, labels_dir[i]
        f1 = codecs.open(predictions_dir[i], 'r', 'gbk')
        f2 = codecs.open(labels_dir[i], 'r', 'gbk')
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        predictions.append(lines1)
        labels.append(lines2)
    print("Read OK!!")
else:
    print("Notice, different length!!!")

logfile.close()

f3 = open(out_dir + "/all_labels_predictions.plk", 'wb')
pickle.dump(predictions, f3)
pickle.dump(labels, f3)
f3.close()

predictions1 = predictions[1:10000]
labels1 = labels[1:10000]
f4 = open(out_dir + "/all_labels_predictions1.plk", 'wb')
pickle.dump(predictions1, f4)
pickle.dump(labels1, f4)
f4.close()