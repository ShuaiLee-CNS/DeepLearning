import pickle

dir_path = '/home/LiShuai/programme/python_T/labels_by_human/allfile_jpg_latlog.pkl'
f2 = open(dir_path, 'rb')
allfile_jpg = pickle.load(f2)
# allfile_txt = pickle.load(f2)
allfile_wgs_lat_lon = pickle.load(f2)
f2.close()

allfile_jpg = allfile_jpg[1:100]
# allfile_txt = allfile_txt[1:100]
allfile_wgs_lat_lon = allfile_wgs_lat_lon[1:100]


f1 = open('/home/LiShuai/programme/python_T/labels_by_human/allfile_jpg_latlog1.pkl', 'wb')
pickle.dump(allfile_jpg, f1)
print(allfile_jpg)
pickle.dump(allfile_wgs_lat_lon, f1)
print(allfile_wgs_lat_lon)
f1.close()
print("Congratulations!!")