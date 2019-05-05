import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'pymodules')))
from googleapiclient.discovery import build
import pymongo
import json
from bson.objectid import ObjectId

uri = "mongodb://touchecosmos:ai8DvhOqzvpDsk0otnjmO6475SCIDzfzrykNqy5Jie5BtujcDcZCtUfontWqkCTmksCT7521s3as0OUlYLCghQ==@touchecosmos.documents.azure.com:10255/?ssl=true&replicaSet=globaldb"
client = pymongo.MongoClient(uri)
db=client['testdb']
coll=db["Testcoll"]
my_api_key = "AIzaSyARKOEUmrOaeQLrQcbmkz6-q3hghbeA0JY"
my_cse_id = "017294505077652159379:o6a_52asc2u"
num = 5

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, sort="date", **kwargs).execute()
    return res['items']

db_info=coll.find_one({"_id":ObjectId(sys.argv[1])})
search_input=db_info["input"]

searchStr=''
output_result=''
searchStr = searchStr + search_input

results = google_search(
    searchStr, my_api_key, my_cse_id, num=num)

if len(results) > 0:
    output_result=output_result + results[0]['title'] + " Link: " + results[0]['link']
else:
    output_result='Nothing found'

print(output_result)
coll.update_one({"_id":ObjectId(sys.argv[1])},{"$set":{"ouput": output_result}});
