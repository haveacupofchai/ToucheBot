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
cloud_vision_client = vision.ImageAnnotatorClient()

def process_image():
    imagedata=base64.b64decode(db_info["attachment"])
    return imagedata

def reverse_image_search(imagedata):
    image = vision.types.Image(content=imagedata)
    web_detection = cloud_vision_client.web_detection(image=image).web_detection

    if web_detection.pages_with_matching_images:
        print('\n{} Pages with matching images retrieved fin'.format(
            len(web_detection.pages_with_matching_images)))

        for page in web_detection.pages_with_matching_images:
            print('Url   : {}'.format(page.url))

    if len(web_detection.pages_with_matching_images) > 0:
        return web_detection.pages_with_matching_images[0].url

    return ''

def detect_text(imagedata):
    image = vision.types.Image(content=imagedata)
    response = cloud_vision_client.text_detection(image=image)
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
    imagedata = process_image()
    output_result = reverse_image_search(imagedata)
    if output_result == '':
        search_str = detect_text(imagedata)
else:
    search_str = search_str + input_text

if search_str != '':
    results = google_search(
        search_str, my_api_key, my_cse_id, num=num)

#for i in range(0,len(results)):
#    print(results[i]['title'] + " Link: " + results[i]['link'])

if output_result == '':
    if len(results) > 0:
        output_result=output_result + results[0]['title'] + " Link: " + results[0]['link']
    else:
        output_result='Nothing found'

print(output_result)
coll.update_one({"_id":ObjectId(sys.argv[1])},{"$set":{"output": output_result}});
