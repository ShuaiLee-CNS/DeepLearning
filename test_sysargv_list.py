import os

name = ['/static/0000000001.jpg', '/static/0000000002.jpg', '/static/0000000003.jpg', '/static/0000000004.jpg', '/static/0000000005.jpg', '/static/0000000006.jpg', '/static/0000000007.jpg', '/static/0000000008.jpg', '/static/0000000009.jpg', '/static/0000000010.jpg']


# name1 = ''.join(name)
name1 = str(name)
eval(name1)
print(name1)
# name1.replace('.jpg/st', '.jpg,st')
name2 = name1.split(",")
print(name2[1])
# list_name = list(name1)
# print(list_name)
# os.popen('python ')