'''
Author: guanliyang 18622300031@163.com
Date: 2023-06-14 09:49:10
LastEditors: guanliyang 18622300031@163.com
LastEditTime: 2023-06-15 13:06:41
FilePath: \FAQ\server.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
#coding=utf-8
import http.client
import urllib
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse
from urllib import parse
from findAnswer import get_answer

def start_server():
    data = {'result': 'this is a test'}
    host = ('localhost', 8981)
    

    class Resquest(BaseHTTPRequestHandler):
        def do_GET(self):
            data={"Method:":self.command,
                  "Path:":self.path,
                  }
            url=urlparse("http://192.168.10.107:8981/"+self.path)
            params = parse.parse_qs(url.query)
            key = ''
            if 'key' in params.keys():
                key =params['key'][0]
            else:
                return
            
            response = ''
            if key != '':
                response = get_answer(key)
            data = {
                'result':response
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')

            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        def do_POST(self):
            length = int(self.headers['Content-Length'])
            post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            # You now have a dictionary of the post data
            data = {"Method:": self.command,
                    "Path:": self.path,
                    "Post Data":post_data}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())

        def do_HEAD(self):
            data = {"Method:": self.command,
                    "Path:": self.path,
                    "Header Content-type": self.headers.get('Content-type')}
            print(data)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(json.dumps(data).encode())
        def do_PUT(self):
            data = {"Method:": self.command,
                    "Path:": self.path,
                    "Header Content-type": self.headers.get('Content-type')}
            print(data)
            path = self.path
            content_length = int(self.headers.get('content-length'))
            content = self.rfile.read(content_length)
            #safe_mkdir(os.path.dirname(path))
            with open("D:/code/pyhttp/put_datas.txt", 'ab') as outfile:
                outfile.write(content)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()

if __name__ == '__main__':
    start_server()
    print("start server success...")
