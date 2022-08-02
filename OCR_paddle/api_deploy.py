from bottle import run,template,route,request
import numpy as np
import cv2
import json
import base64
import sys
import os
from predict_onnx import Predictonnx

models = {}
root = 'models_api'
for file in os.listdir(root):
    s=os.path.splitext(file)
    if(s[1].lower() == '.onnx'):
        name = s[0]
        pred = Predictonnx(os.path.join(root,file),os.path.join(root,name+'.txt'))
        models.update({s[0]:pred})
        print('model:',name)

@route('/<name>',method='POST')
def index(name):
    if(name in models):
        data =request.body.read()
        img = np.frombuffer(data,np.uint8)
        img = cv2.imdecode(img,cv2.IMREAD_COLOR)
        info = models[name].predict(img)[0]
        return ','.join(list(map(str,info)))
    else:
        return 'model not exist'

if __name__ == '__main__':

    run(host='0.0.0.0', port=8080)