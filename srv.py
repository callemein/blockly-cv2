from io import StringIO
import sys, socket, threading, time, datetime, os
from multiprocessing import Process, Queue
import cv2
import numpy as np

global gThreads
global qQueue

qQueue = Queue()
gThreads = []

class MyThread( threading.Thread ):
    def __init__(self, code):
        super(MyThread, self).__init__()
        self._stop_event = threading.Event()
        self.code = code
        
    def run( self ):
        try:
            exec( compile(self.code, "lala", "exec") )
        except Exception as e:
            print(str(e))
           
    def stop(self):
        print(self.exec_ptr)
        self._stop_event.set()
        exit(0)

    def stopped(self):
        return self._stop_event.is_set()
        

def RunProgram(queue):
    code = queue.get()
    try:
        exec( compile(code, "lala", "exec") )
    except Exception as e:
        print(str(e))
        
    return 0

def postdata(environ):
    request_body_size = int(environ['CONTENT_LENGTH'])
    return environ['wsgi.input'].read(request_body_size)

def save(ext,environ):
    try:
        lr = postdata(environ).split("\n")
        name = lr[0]
        code = "\n".join(lr[1:])
        try: os.mkdir("prj/"+name);
        except: pass
        f = open("prj/"+name +"/code"+ext, "wb")
        f.write(code)
        f.close()
        return "saved ok."

    except Exception as e:
        #print(str(e))
        return str(e)

def load(environ):
    code = ""
    try:
        name = postdata(environ)
        f = open("prj/"+name +"/code.xml", "rb")
        code = f.read()
        f.close()

    except IOError as e:
        #print(str(e))
        return str(e)

    return code

def application(environ, start_response):
    url = environ['PATH_INFO'];
    data = ""
    if url == "/":
        url = "/Blockly.html"
    if url.startswith('/code'):
        sys.stdout = sys.stderr = mystdout = StringIO()
        try:          
            qQueue.put(postdata(environ))
            new_thread = Process(target=RunProgram, args=(qQueue,))
            gThreads.append(new_thread)
            new_thread.start()
            
            #exec( compile( postdata(environ), "blockly", "exec" ) )
            data = mystdout.getvalue()
        except Exception as e:
            #print(str(e))
            data = str(e)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    elif url.startswith('/stop'):
        print('Stopping Threads')
        for t in gThreads:
            t.terminate()
    elif url.startswith('/save_code'):
        data = save(".py",environ)
    elif url.startswith('/save_xml'):
        data = save(".xml",environ)
    elif url.startswith('/load'):
        print('Loading ...')
        print(environ)
        data = load(environ)
    else: # load html/js/resources
        try:
            print("Sending - " + str(url))
            f = open(url[1:])
            data = f.read()
            f.close()        
        except: pass
    start_response( "200 OK", [ ("Content-Type", "text/html"), ("Content-Length", str(len(data))) ] )
    return iter([data])
    
from wsgiref.simple_server import make_server
httpd = make_server( '0.0.0.0', int(os.environ.get("PORT", 9000)), application )
while True: httpd.handle_request()
