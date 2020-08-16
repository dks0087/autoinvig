#!/usr/bin/env python
# coding: utf-8

# In[32]:


from flask import Flask, request, jsonify
import cv2, glob, sys, os
#from PIL import Image
#from flask_restful import Resource, Api
        
app = Flask(__name__)

@app.route('/cheat/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    path = request.args.get("path", None)
    
    p=os.path.split(path)[0]
    path1 = p +"/"+ "cheat" + "/"
    print(path1)
    
    try:
        os.mkdir(path1)
    except OSError:
        print ("Creation of the directory %s failed" % path1)
    else:
        print ("Successfully created the directory %s " % path1)
    
    # For debugging
    print(f"got path {path}")
    response = {}
    cheat_bool = 0
    cheating_attempts = 0
    a=[]
    compression_factor = [cv2.IMWRITE_PNG_COMPRESSION, 9]
    eye_cascade_path = "haarcascade_eye.xml"
    eye_cascade = cv2.CascadeClassifier(eye_cascade_path)
    for file in glob.glob(path):
        frame= cv2.imread(file)
        yuv = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
        bgr_frame = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=40.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        for (x, y, width, height) in eyes:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
            break
        if len(eyes) == 0:
            cheat_bool = 1
        else:
            gray_cropped_right = gray[eyes[0][1]: eyes[0][1] + eyes[0][3],
                                              eyes[0][0] + eyes[0][2] // 2: eyes[0][0] + eyes[0][2]]
            cv2.GaussianBlur(gray_cropped_right, (3, 3), 16)

        if cheat_bool == 1:
            cheating_attempts += 1
           # cheating_attempts.append
            b= os.path.splitext(os.path.basename(file))[0]
            a.append(b)
                   
            y = cv2.resize(frame, (128, 72), interpolation = cv2.INTER_AREA)
            cv2.imwrite(path1 + str(os.path.splitext(os.path.basename(file))[0]) + "_cheat"  + ".png", y, compression_factor)#working
          # Reset value of cheat_bool to catch further such instances - in case they happen
        cheat_bool = 0

    # Return the response in json format
    return jsonify(a)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('path')
    print(param)
    
@app.route('/')
def index():
    return "<h1>To test go to http://127.0.0.1:5000/cheat/?path=[yourdirectory]!!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)


# In[20]:


#print(os.path.splitext(os.path.basename(path))[0])


# In[ ]:




