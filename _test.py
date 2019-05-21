import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'pymodules')))
from googleapiclient.discovery import build
import pymongo
import json
from bson.objectid import ObjectId
import base64
import io
from PIL import Image
from google.cloud import vision
from io import BytesIO

uri = "mongodb://touchecosmos:ai8DvhOqzvpDsk0otnjmO6475SCIDzfzrykNqy5Jie5BtujcDcZCtUfontWqkCTmksCT7521s3as0OUlYLCghQ==@touchecosmos.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)
db=client['testdb']
coll=db["Testcoll"]
my_api_key = "AIzaSyARKOEUmrOaeQLrQcbmkz6-q3hghbeA0JY"
my_cse_id = "017294505077652159379:o6a_52asc2u"
num = 5
output_result=''
search_str=''

def process_image():
    imagedata=base64.b64decode(db_info["attachment"])
    filename='temp.jpg'
    with open(filename, 'wb') as f:
        f.write(imagedata)

def detect_text():
    client = vision.ImageAnnotatorClient()
    with io.open('temp.jpg', 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    total_text = ''
    for text in texts:
        details = text.description
        if " " in details:
            continue
        total_text += ' ' + details
    return total_text


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    if 'items' in res:
        return res['items']
    else:
        return {}

db_info=coll.find_one({"_id":ObjectId(sys.argv[1])})
input_text=db_info["input"]

if not input_text:
    process_image()
    search_str = detect_text()
else:
    search_str = search_str + input_text

results = google_search(
    search_str, my_api_key, my_cse_id, num=num)

#for i in range(0,len(results)):
#    print(results[i]['title'] + " Link: " + results[i]['link'])

if len(results) > 0:
    output_result=output_result + results[0]['title'] + " Link: " + results[0]['link']
else:
    output_result='Nothing found'

print(output_result)
coll.update_one({"_id":ObjectId(sys.argv[1])},{"$set":{"ouput": output_result}});
