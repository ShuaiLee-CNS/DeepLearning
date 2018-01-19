import web
import sys
import os
# import time
# import socket

# name1 = sys.argv[2]
name = ['/static/C101217.jpg', '/static/C101218.jpg']
print(name)
render = web.template.render("/home/LiShuai/programme/python_T/test/templates/")
urls = (
    '/', 'hello',
    '/image/', 'image'
)
'''
file_path = '/home/LiShuai/programme/python_T/labels_by_human'
pid = os.getpid()
hostname = socket.gethostname()
time1 = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))'''
class hello():
    global name
    # name = '/static/C101217.jpg'
    # def GET(self):
    #     return render.index9()
    #
    # def POST(self):
    #     data = web.input()
    #     # aa_host = data['host']
    #     # aa_pass = data['passwd']
    #     # os.popen('mkdir %s/%s_%s_%s_%d_%s' % (file_path, aa_host, aa_pass, hostname, pid, time1))
    #     return aa_host,aa_pass
    # def __init__(self, name):
    #     self.name = name
    def GET(self):
        # name = '/static/C101217.jpg'
        # for i in range(len(name)):
        return render.index8(name[0])
    # def POST(self, name):
    #     post_data = web.input()
    #     print(post_data)
    #     name = name[1:]
    #     print(name)
    # def POST(self):
    #     post_data = web.input()
    #     print(post_data)
    #     # raise render.index8(name)
    #     for i in range(len(name)):
    #         raise render.index8(name[i])
        # return post_data['crop']
class image():

    def POST(self):
        global name
        post_data = web.input()
        print(post_data['crop'])
        name = name[1:]
        print(name)
        raise web.seeother('/')



def main():
    # name = ['/static/C101217.jpg', '/static/C101218.jpg']
    print("main")
    app = web.application(urls, globals())
    app.run()
if __name__ == '__main__':
    print("if __name__")
    main()
