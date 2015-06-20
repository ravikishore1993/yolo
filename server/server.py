#!/usr/bin/python

"""
Save this file as server.py
>>> python server.py 0.0.0.0 8001
serving on 0.0.0.0:8001

or simply

>>> python server.py
Serving on localhost:8000
"""

import SimpleHTTPServer
import SocketServer
import logging
import cgi
import os
import random
import sys
from pydub import AudioSegment
from subprocess import call

if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8000
    I = ""

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)
        self.protocol_version='HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        form = open('form.html','r')
        self.wfile.write(form.read())


    def do_POST(self):
        logging.warning("======= POST STARTED =======")
        logging.warning(self.headers)
        self.protocol_version='HTTP/1.1'
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        logging.warning("======= POST VALUES =======")
        logging.warning("\n")
        upload = form['upload']
        if not upload.file: 
            logging.warning("Upload not found in POST request")
            self.wfile.write("No file uploaded")
            return
        absolutefilepath = os.path.join('/tmp',str(random.randint(1,1000))+upload.filename)    
        fout = file(absolutefilepath,'wb')
        while 1:
            chunk = upload.file.read(10000)
            if not chunk: break
            fout.write(chunk)
        fout.close()
        self.wfile.write("File Uploaded Successfully at "+ absolutefilepath)
        logging.warning("File Uploaded Successfully at "+ absolutefilepath)
        print(form.getvalue('result'))
        result = form.getvalue('result')
        filetype = upload.filename.split('.')[-1]
        print filetype
        sound = AudioSegment.from_file(absolutefilepath,filetype)
        sound.export(absolutefilepath.replace(filetype,'wav'), format="wav")
        absolutefilepath = absolutefilepath.replace(filetype,'wav')
        print os.popen('yaafe.py -r 44100 -p Metadata=False -c features '+absolutefilepath).read()
        if result=='false':
            print('##############################')
            pass
        else :
            if result=='true':
                print('((((((((((((((((((((((((((((((')

                pass
            else  :
                print('))))))))))))))))))))))))))))))')

                pass      
            
Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "@rochacbruno Python http server version 0.1 (for testing purposes only)"
print "Serving at: http://%(interface)s:%(port)s" % dict(interface=I or "localhost", port=PORT)
httpd.serve_forever()
