import web
import sys
# import os
# import time
# import socket

name = sys.argv[2]
# name = '/static/C101217.jpg'
render = web.template.render("/home/LiShuai/programme/python_T/test/templates/")
urls = ('/', 'hello')
app = web.application(urls, globals())
'''
file_path = '/home/LiShuai/programme/python_T/labels_by_human'
pid = os.getpid()
hostname = socket.gethostname()
time1 = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))'''
# name = '/static/C101217.jpg'
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
        return render.index8(name)


    def POST(self):
        post_data = web.input()
        print(post_data)
        return post_data['crop']

def main():
    # name = '/static/C101217.jpg'
    app.run()
if __name__ == '__main__':
     main()