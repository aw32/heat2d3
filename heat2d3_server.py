#!/usr/bin/python3
# small server to serve heat2d3 conversion and output as svg

import subprocess
import time
import os
from flask import Flask
from flask import request
from flask import Markup
app = Flask(__name__)

PORT = 1112

licenses = "<a href=\"https://d3js.org/\">D3.js</a> by <a href=\"static/d3-license.txt\">Mike Bostock</a> <a href=\"http://marvl.infotech.monash.edu/webcola/\">cola.js</a> by <a href=\"static/cola-license.txt\">Tim Dwyer</a>"

templateHtml = None

with open('template.html', 'r') as template:
    templateHtml = template.read()

@app.route('/')
def main():
    return ("<html><head><title>heat2d3</title></head><body>"
            "<form method=\"POST\" action=\"convert\">"
            "Enter json or yaml text:<br/>"
            "<textarea name=\"text\"></textarea><br/>"
            "<input type=\"submit\"/>"
            "</form>"
            "</body></html>")

@app.route('/convert',methods=['POST'])
def convert():
    if "text" not in request.form:
        return "<html><head><title>heat2dot</title></head><body>Text not found</body></html>",403
    
    infile = "/tmp/inheat2d3_"+str(time.time())

    with open(infile,"w") as intextfile:
        intextfile.write(request.form["text"])
    
    error_messages = None
    js = None

    try:
        d3_out = subprocess.run(["cat "+infile+" | ./heat2d3.py "],shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        js = d3_out.stdout.decode("UTF-8")
        error_messages = d3_out.stderr.decode("UTF-8")

        d3_out = subprocess.run(["cat "+infile+" | ./heat2d3.py > "+dotfile],shell=True,stderr=subprocess.PIPE)

        if d3_out.returncode != 0:
        
            return Markup("<html><head><title>heat2d3</title></head><body>Failure<br/><pre>")+Markup.escape(d3_out.stderr.decode("UTF-8"))+Markup("</pre></body></html>")
    except Exception as e:
        print(e)
    finally:
        try:
            os.remove(infile)
        except:
            pass
        try:
            #os.remove(dotfile)
            pass
        except:
            pass
    
    if error_messages != None and js == None:
        return Markup("<html><head><title>heat2dot</title></head><body>Failure<br/><pre>")+Markup.escape(error_messages)+Markup("</pre></body></html>")
    elif js != None:
        if error_messages == None:
            return (Markup("<html><head><title>heat2d3</title></head>")+
                    Markup(js)+
                    Markup(templateHtml)+
                    Markup(licenses+"</body></html>"))
        else:
            return (Markup("<html><head><title>heat2dot</title></head>")+
                    Markup(js)+
                    Markup(templateHtml)+
                    Markup("<br/><pre>")+
                    Markup.escape(error_messages)+
                    Markup("</pre>"+licenses+"</body></html>"))
    else:
        return "<html><head><title>heat2d3</title></head><body>Something went horribly wrong.</body></html>"

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=PORT)

