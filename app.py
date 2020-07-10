from flask import Flask,request,jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import Binary
import os
import face_recognition
from datetime import datetime
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
def get_key(val): 
    for key, value in my_dict.items(): 
         if val == value: 
             return key 
  
    return "key doesn't exist"
app=Flask(__name__)
CORS(app)

app.config["MONGO_URI"]="mongodb://localhost:27017/june9-2019_new"
app.config['DEFAULT_PARSERS'] = [
    'flask.ext.api.parsers.JSONParser',
    'flask.ext.api.parsers.URLEncodedParser',
    'flask.ext.api.parsers.MultiPartParser'
]
dict_obj = my_dictionary()
app.config['IMAGE_UPLOAD']="\images"

mongo = PyMongo(app)

@app.route("/",methods=["GET"])
def getData():
  employee_data=[]
  for emp in mongo.db.employee.find({},{"_id":0}):
    employee_data.append(emp)
  return jsonify(employee_data)

@app.route("/upload",methods=["POST"])
def uploadDate():
  now = datetime.now()
  user_new_faces=mongo.db.collection_new
  if request.files:
    image = request.files['uploadedImage']
    mongo.save_file(image.filename,image)
    user_one_face = face_recognition.load_image_file(image)
    user_new_faces.insert({'name':request.form["employeeName"] , 'ID':request.form["employeeId"] , 'Time':now})
    user_one_face_encoding = face_recognition.face_encodings(user_one_face)[0]
    dict_obj.add(request.form["employeeId"],user_one_face_encoding)
    print(dict_obj)
    return jsonify("IMAGE UPLAODED")
    

@app.route("/detect",methods=["POST"])
def face_detection_method():
  now = datetime.now()
  file = request.files['uploadedImage']
  face_locations = face_recognition.face_locations(file)
  print(face_locations)
  for face in face_locations:
    (x,y,w,h)=face
    actual_face=file[y:y+w, x:x+h]
    user_one_face = face_recognition.load_image_file(actual_face)
    user_one_face_encoding = face_recognition.face_encodings(user_one_face)[0]
    if user_one_face_encoding in dict_obj.values():
      print(get_key(user_one_face_encoding))

    
    

  

  


@app.route("/test_dict_object",methods=["GET"])
def testtt():
  return dict_obj

  
 


    
    

if __name__ =="__main__":
  app.run(debug=True)